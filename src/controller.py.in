# -*- coding: iso-8859-15 -*-


import pygtk
pygtk.require('2.0')
import gtk
import os
import book
import pygst
pygst.require("0.10")
import gst

from dbr_i18n import _          #For i18n support

class Controller:
  """
  Callbacks functions for the view, player, book and settings
  """ 

  def setView(self, v):
    self.v = v


  def __init__(self, p, sets):
    """
    Controller object initialization
    """
    self.p = p
    self.b = None
    self.sets = sets


  def getConfiguration(self):
    """
    Gets configuration, if not exists create it
    """
    ncc = []
    configuration = self.sets.getConfiguration()
    if configuration[0] != None:
      self.p.changeVolume(configuration[4]-1)
      if os.path.exists(configuration[1]):
        self.b = book.Book(configuration[1], (configuration[2]), (configuration[3]))
        if configuration[0] == self.b.getBookTitle():
          ncc = self.b.getNcc()
        else:
          self.b = None
      else:
        self.b = None
    else:
      pass
    return ncc, configuration[2]


  def destroy(self, widget):
    """
    Destroy window
    """
    return True


  def loadLatestBook(self):
    """
    Load the last played book
    """
    self.b.setReadPosition(self.b.ncc_pos,self.b.audio_index-1)
    self.syncViewAudio()

  def openBook(self, w):
    """
    Handle opening a book 
    """
    if self.p.getState() == "Playing":
      self.p.playPause()
    selection = gtk.FileChooserDialog(_("Open book"), None, gtk.FILE_CHOOSER_ACTION_OPEN, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
    selection.set_default_response(gtk.RESPONSE_OK)

    # Filter all ncc.html filenames
    filter = gtk.FileFilter()
    path = os.path.abspath("ncc")
    selection.set_filename(path)
    # Configure file extension and filter name
    filter.set_name(_("Daisy 2.0/2.02 book (*.html)"))
    filter.add_pattern("*.html")
    selection.add_filter(filter)

    response = selection.run()
    if response == gtk.RESPONSE_OK:
      try:
        # Open the book
        filename = selection.get_filename()
        self.b = book.Book(filename)
        
      except IOError:
        self.showMessage(_("Failed to open"), _(" The book can not be opened"))
    elif response == gtk.RESPONSE_CANCEL:
      self.showMessage(_("Canceled selection"), _("No book has been selected"))
      if self.p.getState() == "Paused":
        self.p.playPause()
    selection.destroy()
    ncc = self.b.getNcc()
    if len(ncc) > 1:
      return ncc

  def change_play_pause_toolbutton(self, state):
    if state == "Paused":
      self.v.view_play_icon()
    else:
      self.v.view_pause_icon()

  def openRecentBookCallback(self, w, data):
    """
    Open a recently opened book
    """
    play = False
    if self.p.getState() == "Playing":
      play = True
      self.p.playPause()
    books = self.sets.getBooks()
    if books != []:
      book_titles = []
      for i in range(len(books)):
        book_titles.append(books[i][0])
      book_index = self.showCombobox(_("Recently opened books"), _("Choose the book which you want to open"), book_titles)
      if book_index != None:
        aux_book = book.Book(books[book_index][1])
        if aux_book.getBookTitle() == books[book_index][0]:
          self.p.stop()
          self.v.clearModel()
          self.b = aux_book
          self.v.displayBook(self.b.getNcc())
          self.syncViewAudio()
        else:
          self.showMessage(_("Warning"), _("Specified book doesn't match with the book currently in that path"))
      else:
        self.showMessage("Warning", _("You have not selected any book"))
    else:
      self.showMessage(_("Warning"), _("There are no saved books"))
    if (self.p.getState() == "Paused") and play:
      self.p.playPause()


  def closeBookCallback(self, w, data):
    """
    Close book callback
    """
    if self.bookOpened():
      self.p.stop()
      self.b = None
      self.v.clearModel()


  def closeApplication(self):
    """
    Closes the application saving the reading position and configuration
    """
    if self.bookOpened():
      self.p.stop()
      configuration = self.b.getExactPosition()
      volume = self.p.getVolume()
      configuration.append(volume)
      self.sets.saveConfiguration(configuration)


  def displayBookInfoCallback(self, w, data):
    """
    Displays general book information
    """
    play = False
    if self.bookOpened():
      if self.p.getState() == "Playing":
        play = True
        self.p.playPause()
      info = self.b.getBookInfo()
      self.showMessage(_("Book information"), info)
      if self.p.getState() == "Paused" and play:
        self.p.playPause()
    else:
      self.showMessage(_("Warning"), _("There are currently nno playing book"))


  def displayBookTranslationCallback(self, w, data):
    """
    Displays book translation information
    """
    play = False
    if self.bookOpened():
      if self.p.getState() == "Playing":
        play = True
        self.p.playPause()
      info = self.b.getBookTranslationInfo()
      self.showMessage(_("Book translation information"), info)
      if self.p.getState() == "Paused" and play:
        self.p.playPause()
    else:
      self.showMessage(_("Warning"), _("There are currently no playing book"))


  def displayCurrentPlayingTimeCallback(self, w, data):
    """
    Displays playing time in hh:mm:ss format
    """
    play = False
    if self.bookOpened():
      if self.p.getState() == "Playing":
        play = True
        self.p.playPause()
      pos = self.p.getCurrentNs()
      pos = pos / 1000000000
      seconds, aux = self.b.getPlayingTime()
      t = seconds +(pos - aux)
      duration = self.b.getFormatedTime(t)
      self.showMessage(_("Elapsed playback time"), duration)
      if self.p.getState() == "Paused" and play:
        self.p.playPause()
    else:
      self.showMessage(_("Warning"), _("Tehre are currently no playing book"))


  def displayBookDurationCallback(self, w, data):
    """
    Display current book duration in hh:mm:ss format
    """
    play = False
    if self.bookOpened():
      if self.p.getState() == "Playing":
        play = True
        self.p.playPause()
      duration = self.b.getBookDuration()
      duration_formated = self.b.getFormatedTime(duration)
      self.showMessage(_("Total book's playback time"), duration_formated)
      if self.p.getState() == "Paused" and play:
        self.p.playPause()
    else:
      self.showMessage(_("Warning"), _("Tehre are currently no playing book"))


  def syncViewAudio(self, play=True):
    """
    This function syncs the book view with the audio when playing forwards or user press a navigation option
    """
    cursor_pos = self.v.treeview.get_cursor()
    if cursor_pos[0] != None:
      aux = list(cursor_pos)
      listed = list(aux[0])
      if self.b.getNccPosition() != listed[0]:
        self.v.updateView(self.b.getNccPosition())
      elif play:
        file, pos_begin, pos_end = self.b.getAudioTrack()
        self.p.play(file, pos_begin, pos_end)
    else:
      self.v.treeview.set_cursor(self.b.getNccPosition(),None)

  def syncAudioView(self, ncc_pos):
    """
    Synchronizes the audio with the view of the book toc when user press a navigation command or uses the mouse
    """
    self.p.stop()
    self.b.setReadPosition(ncc_pos,0)
    file, pos_begin, pos_end = self.b.getAudioTrack()
    self.p.play(file, pos_begin, pos_end)


  def stopCallback(self, w, data):
    """
    Stops the playback and checks if there is any opened book
    """
    if self.bookOpened():
      self.p.stop()
      self.syncViewAudio(False)
    else:
      self.showMessage(_("Warning"), _("Tehre are currently no playing book"))


  def bookOpened(self):
    """
    Checks if there's an opened book
    """
    if self.b == None:
      return False
    else:
      return True

  def displayBookTitle(self):
    return self.b.getBookTitle()

  def switchStateCallback(self, w, data):
    """
    Switch between play and pause
    """
    if self.bookOpened():
      self.p.playPause()
    else:
      self.showMessage(_("Warning"), _("There are currently no playing book"))


  def displayChaptersCallback(self, w, data):
    """
    Displays the chapters list
    """
    play = False
    if self.bookOpened():
      if self.p.getState() == "Playing":
        play = True
        self.p.playPause()
      chapters, chapters_pos = self.b.getChapters()
      if chapters != []:
        chapter_pos = self.showCombobox(_("Goo to chapter"), _("Select which chapter do you want to go"), chapters)
        if chapter_pos != None:
          self.p.stop()
          self.syncViewAudio() #here?
        else:
          self.showMessage(_("Warning"), _("You have not selected any chapter"))
      else:
        self.showMessage(_("Error"), _("Don't exist any chapter in the book"))
      if self.p.getState() == "Paused" and play:
        self.p.playPause()
    else:
      self.showMessage(_("Warning"), _("There are currently no playing book"))


  def goToNextChapterCallback(self, w, data):
    """
    Goto next chapter
    """
    if self.bookOpened():
      switch = self.b.nextOrPriorChapter(1)
      if switch == 1:
        self.p.stop()
        self.b.setReadPosition(self.b.ncc_pos,0)
        self.syncViewAudio()
    else:
      self.showMessage(_("Warning"), _("There are currently no playing book"))


  def goToPriorChapterCallback(self, w, data):
    """
    Goto prior chapter
    """
    if self.bookOpened():
      switch = self.b.nextOrPriorChapter(-1)
      if switch == 1:
        self.p.stop()
        self.b.setReadPosition(self.b.ncc_pos,0)
        self.syncViewAudio()
    else:
      self.showMessage(_("Warning"), _("There are currently no playing book"))


  def goToNextPageCallback(self, w, data):
    """
    Goto to the next page entered by user
    """
    if self.bookOpened():
      switch = self.b.nextOrPriorPage(1)
      if switch:
        self.p.stop()
        self.b.setReadPosition(self.b.getNccPosition(),0)
        self.syncViewAudio()


  def goToPriorPageCallback(self, w, data):
    """
    Goto prior page
    """
    if self.bookOpened():
      switch = self.b.nextOrPriorPage(-1)
      if switch:
        self.p.stop()
        self.b.setReadPosition(self.b.getNccPosition(),0)
        self.syncViewAudio()


  def goToPriorTextCallback(self, w, data):
    """
    Goto prior text
    """
    if self.bookOpened():
      self.p.stop()
      self.b.nextOrPriorParagraph(-1)
      self.b.setReadPosition(self.b.getNccPosition(),self.b.audio_index)
      self.syncViewAudio()

  def goToNextTextCallback(self, w, data):
    """
    Goto next text group
    """
    if self.bookOpened():
      self.p.stop()
      self.syncViewAudio()

  def goToPageCallback(self, w, data):
    """
    Goto a specified page user entered
    """
    play = False
    if self.bookOpened():
      if self.p.getState() == "Playing":
        play = True
        self.p.playPause()
      page = self.showEntryText(_("Go to page"), _("Enter the page which you want to go"), 4)
      if page.isdigit():
        switch, pos = self.b.goToPage(page)
        if switch == 1:
          self.p.stop()
          self.b.setReadPosition(pos-1,0)
          self.syncViewAudio()
        else:
          self.showMessage(_("Warning"), _("Page out of range"))
      else:
        self.showMessage(_("Error"), _("You have not entered a number"))
      if self.p.getState() == "Paused" and play:
        self.p.playPause()
    else:
      self.showMessage(_("Warning"), _("Tehre are currently no playing book"))


  def upVolumeCallback(self, w, data):
    """
    Change up the volume
    """
    if self.bookOpened():
      self.p.changeVolume(1)
    else:
      self.showMessage(_("Warning"), _("There are currently no playing book"))


  def downVolumeCallback(self, w, data):
    """
    Change down the volume
    """
    if self.bookOpened():
      self.p.changeVolume(-1)
    else:
      self.showMessage(_("Warning"), _("There are currently no playing book"))


  def toggleMuteCallback(self, w, data):
    """
    Toggles the mute
    """
    if self.bookOpened():
      self.p.mute()
    else:
      self.showMessage(_("Warning"), _("There are currently no playing book"))


  def createBookmarkCallback(self, w, data):
    """
    Creates a bookmark for the current playing book
    """
    play = False
    if self.bookOpened():
      if self.p.getState() == "Playing":
        play = True
        self.p.playPause()
      bookmark_name = self.showEntryText(_("Set bookmark"), _("Enter the bookmark name"), 50)
      if bookmark_name != '':
        bookmark = self.b.getExactPosition()
        bookmark.append(bookmark_name)
        self.sets.createBookmark(bookmark)
      else:
        self.showMessage(_("Error"), _("You have not entered a bookmark name"))
      if self.p.getState() == "Paused" and play:
        self.p.playPause()
    else:
      self.showMessage(_("Warning"), _("There are currently no playing book"))


  def displayBookmarksCallback(self, w, data):
    """
    Displays a list of bookmarks 
    """
    play = False
    if self.bookOpened():
      book_title = self.b.getBookTitle()
      bookmarks = self.sets.getBookmarksForBook(book_title)
      if self.p.getState() == "Playing":
        play = True
        self.p.playPause()
      if bookmarks != []:
        bookmarks_names = []
        for i in range(len(bookmarks)):
          bookmarks_names.append(bookmarks[i][0])
        bookmark_index = self.showCombobox(_("Bookmark list"), _("Choose the bookmark which you want to go"), bookmarks_names)
        if bookmark_index != None:
          self.p.stop()
          self.b.setReadPosition(bookmarks[bookmark_index][1], bookmarks[bookmark_index][2])
          self.syncViewAudio()
        else:
          self.showMessage(_("Warning"), _("You have not selected any bookmark"))
      else:
        self.showMessage(_("Warning"), _("There are not bookmarks for this book"))
      if self.p.getState() == "Paused" and play:
        self.p.playPause()
    else:
      self.showMessage(_("Warning"), _("Tehre are currently no playing book"))


  def deleteBookmarkCallback(self, w, data):
    """
    Prompts for deletion of bookmark
    """
    play = False
    if self.bookOpened():
      book_title = self.b.getBookTitle()
      bookmarks = self.sets.getBookmarksForBook(book_title)
      if self.p.getState() == "Playing":
        play = True
        self.p.playPause()
      if bookmarks != []:
        bookmarks_names = []
        for i in range(len(bookmarks)):
          bookmarks_names.append(bookmarks[i][0])
        bookmark_index = self.showCombobox(_("Bookmarks deletion"), _("Choose the bookmark which you want to delete"), bookmarks_names)
        if bookmark_index != None:
          self.sets.deleteBookmark(book_title, bookmark_index)
        else:
          self.showMessage(_("Warning"), _("You have not selected any bookmark"))
      else:
        self.showMessage(_("Warning"), _("Don't exist bookmarks for this book"))
      if self.p.getState() == "Paused" and play:
        self.p.playPause()
    else:
      self.showMessage(_("Warning"), _("Tehre are currently no playing book"))


  def showMessage(self, title, msg):
    """
    Shows a message
    msg: Message to present
    title: Title of the message
    """
    msg_window = gtk.Dialog(title, None, 0, (gtk.STOCK_OK, gtk.RESPONSE_OK))

    msg_window_label = gtk.Label(msg)
    msg_window.vbox.pack_start(msg_window_label, True, True, 0)
    msg_window_label.show()
    response = msg_window.run()
    msg_window.destroy()


  def showEntryText(self, title, entry_label, size):
    """
    Shows an entry dialog and gets text entered
  title: Title for the dialog
    entry_label: Text label for the entry
    size: Size for the entry
    """
    dialog = gtk.Dialog(title, None, 0, (gtk.STOCK_OK, gtk.RESPONSE_OK, gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
    label = gtk.Label(entry_label)
    label.show()
    dialog.vbox.pack_start(label)
    entry = gtk.Entry()
    entry.set_max_length(size)
    entry.select_region(0, len(entry.get_text()))
    entry.show()
    dialog.vbox.pack_start(entry, False)
    response = dialog.run()
    if response == gtk.RESPONSE_OK:
      text = entry.get_text()
    else:
      text = ''
    dialog.destroy()
    return text


  def showCombobox(self, title, label_text, choices):
    """
    Shows a combobox and gets selected choice
    """
    dialog = gtk.Dialog(title, None, 0, (gtk.STOCK_OK, gtk.RESPONSE_OK, gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
    label = gtk.Label(label_text)
    label.show()
    dialog.vbox.pack_start(label)
    combobox = gtk.combo_box_new_text()
    for x in choices:
      combobox.append_text(x)
    combobox.set_active(0)
    combobox.show()
    dialog.vbox.pack_start(combobox, False)
    response = dialog.run()
    if response == gtk.RESPONSE_OK:
      selected_choice = combobox.get_active()
    else:
      selected_choice = None
    dialog.destroy()
    return selected_choice


  def displayHelpCallback(self, w, data):
    """
    Displays help screen
    """
    play = False
    if self.bookOpened():
      if self.p.getState() == "Playing":
        play = True
        self.p.playPause()
    if os.path.exists("docs/ayuda.html"):
      os.system("firefox docs/ayuda.html")
    else:
      self.showMessage(_("Warning!"), _("The help file can not be found"))
    if self.bookOpened():
      if self.p.getState() == "Paused" and play:
        self.p.playPause()


  def close_about_dialog_callback(self, w, data):

    if self.bookOpened():
      if self.p.getState() == "Paused":
        self.p.playPause()

    if data==gtk.RESPONSE_CANCEL:
      w.destroy()

  def display_about_dialog_callback(self, w, data):
    """
    This method is used for displaying "About DBR" notice
    """
    play = False
    program_name="DBR"
    authors=['Rafael Cantos Villanueva', \
            'Francisco Javier Dorado Martínez']
    translations=_("This program has been translated by:\n\nJuan C. Buño\n")
    license=_("This program is under GNU/General Public License version 3. See accompanying COPYING file for more details.") 
    version="@VERSION@"
    copyright="Copyright 2008 RafaelCantos Villanueva"
    website="http://dbr.sourceforge.net"

    ADlg=gtk.AboutDialog()

    if self.bookOpened():
      if self.p.getState() == "Playing":
        play = True
        self.p.playPause()


    ADlg.set_program_name(program_name)
    ADlg.set_version(version)
    ADlg.set_copyright(copyright)
    ADlg.set_authors(authors)
    ADlg.set_translator_credits(translations)
    ADlg.set_license(license)
    ADlg.set_website(website)

    ADlg.connect("response", self.close_about_dialog_callback)
    ADlg.show()

  def displayLicenseCallback(self, w, data):
    """
    Display license notice
    """
    play = False
    if self.bookOpened():
      if self.p.getState() == "Playing":
        play = True
        self.p.playPause()
    if os.path.exists("docs/licencia.html"):
      os.system("firefox docs/licencia.html")
    else:
      self.showMessage(_("Warning!"), _("The help file can not be found"))
    if self.bookOpened():
      if self.p.getState() == "Paused" and play:
        self.p.playPause()
