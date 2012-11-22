# -*- coding: iso-8859-15 -*-


import pygtk
pygtk.require('2.0')
import gtk
import controller, book, player
import xml.dom.minidom as MD

from dbr_i18n import _          #For i18n support

class View:
  """
  This class handles GUI for DBR
  """

  def newWindow(self):
    """
    Creates the main window for the application
    """
    window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    window.connect("destroy", self.destroyApplication)
    # Translators: this string the main DBR window title
    window.set_title(_("Daisy Book Reader"))
    window.set_border_width(1)
    window.set_default_size(640, 480)
    return window


  def mainMenu(self, window):
    """
    Creates the main menubar
    """
    accel_group = gtk.AccelGroup()
    # initialize main factory.
    # Param1: Type of menu.
    # Param2: path for the menu.
    # Param3: Reference to  AccelGroup.
    item_factory = gtk.ItemFactory(gtk.MenuBar, "<main>", accel_group)

    # Build menu items.
    item_factory.create_items(self.menu_items)
    # Add AccelGroup to the window.
    window.add_accel_group(accel_group)

    # We need a reference for item_factory to avoid destroying it.
    self.item_factory = item_factory
    # Return main menubar.
    return item_factory.get_widget("<main>")


  def __init__(self, controller):
    """
    Initialization for view object
    """
    self.c = controller
    self.c.setView(self)


    self.menu_items = (
      ("/" +  _("_File"), "<alt>F", None, 0, "<Branch>"),
      ("/" + _("File") + "/" + _("_Open book"), "<control>O", self.openBookCallback, 0, None),
      ("/" + _("File") + "/" + _("_Find book"), "<control>F", self.c.openRecentBookCallback, 0, None),
      ("/" + _("File") + "/" + _("_Close book"), "<control>F4", self.c.closeBookCallback, 0, None),
      ("/" + _("File") + "/" + _("_Quit"), "<control>Q", self.closeApplication, 0, None),

      ("/" + _("_Control"), "<alt>C", None, 0, "<Branch>"),
      ("/" + _("Control") + "/" + _("_Play-Pause"), "<control>space", self.c.switchStateCallback, 0, None),
      ("/" + _("Control") + "/" + _("_Mute"), "<control>M", self.c.toggleMuteCallback, 0, None),
      ("/" + _("Control") + "/" + _("_Stop"), "<control>S", self.c.stopCallback, 0, None),
      ("/" + _("Control") + "/" + _("_Volume"), "<alt>V", None, 0, "<Branch>"),
      ("/" + _("Control") + "/" + _("Volume") + "/" + _("Increase volume"), "<control>V", self.c.upVolumeCallback, 0, None),
      ("/" + _("Control") + "/" + _("Volume") + "/" + _("Decrease volume"), "<control><shift>V", self.c.downVolumeCallback, 0, None),

      ("/" + _("_Navigation"), "<alt>N", None, 0, "<Branch>"),
      ("/" + _("Navigation") + "/" + _("Previous chapter"), "<control><shift>L", self.c.goToPriorChapterCallback, 0, None),
      ("/" + _("Navigation") + "/" + _("Next chapter"), "<control>L", self.c.goToNextChapterCallback, 0, None),
      ("/" + _("Navigation") + "/" + _("Previous page"), "<control><shift>N", self.c.goToPriorPageCallback, 0, None),
      ("/" + _("Navigation") + "/" + _("Next page"), "<control>N", self.c.goToNextPageCallback, 0, None),
      ("/" + _("Navigation") + "/" + _("Previous paragraph"), "<control><shift>P", self.c.goToPriorTextCallback, 0, None),
      ("/" + _("Navigation") + "/" + _("Next paragraph"), "<control>P", self.c.goToNextTextCallback, 0, None),
      ("/" + _("_Go to"), "<control>G", None, 0, "<Branch>"),
      ("/" + _("_Go to") + "/" + _("Chapter"), None, self.c.displayChaptersCallback, 0, None),
      ("/" + _("_Go to") + "/" + _("Page"), None, self.c.goToPageCallback, 0, None),
      ("/" + _("_Bookmarks"), "<alt>B", None, 0, "<Branch>"),
      ("/" + _("Bookmarks") + "/" + _("_Set bookmark"), "<control>K", self.c.createBookmarkCallback, 0, None),
      ("/" + _("Bookmarks") + "/" + _("_Delete bookmarks"), "<control>D", self.c.deleteBookmarkCallback, 0, None),
      ("/" + _("Bookmarks") + "/" + _("_List bookmarks"), "<control>B", self.c.displayBookmarksCallback, 0, None),
      ("/" + _("_Info"), "<alt>I", None, 0, "<Branch>"),
      ("/" + _("Info") + "/" + _("_Book info"), "<control>O", self.c.displayBookInfoCallback, 0, None),
      ("/" + _("Info") + "/" + _("Book _translation information"), "<control>N", self.c.displayBookTranslationCallback, 0, None),
      ("/" + _("Info") + "/" + _("Playback _duration"), "<control>X", self.c.displayCurrentPlayingTimeCallback, 0, None),
      ("/" + _("Info") + "/" + _("Total play _duration"), "<control>W", self.c.displayBookDurationCallback, 0, None),
      ("/" + _("_Help"), "<alt>H", None, 0, "<Branch>"),
      ("/" + _("Help") + "/" + _("_User help"), "<control>u", self.c.displayHelpCallback, 0, None),
      ("/" + _("Help") + "/" + _("_About DBR"), "<control>Y", self.c.display_about_dialog_callback, 0, None),
      ("/" + _("Help") + "/" + _("_License"), "<control>J", self.c.displayLicenseCallback, 0, None)
      )

    self.window = self.newWindow()


    main_box = gtk.VBox(False, 1)
    main_box.set_border_width(1)
    main_box.show()

    menubar = self.mainMenu(self.window)

    main_box.pack_start(menubar, False, True, 0)
    menubar.show()


    #Create toolbar
    self.toolbar = gtk.Toolbar()
    self.toolbar.set_orientation(gtk.ORIENTATION_HORIZONTAL)
    self.toolbar.set_style(gtk.TOOLBAR_BOTH)
    self.toolbar.set_border_width(5)
    
    # Options for toolbar: open...
    toolbar_item = gtk.ToolButton(_("Open"))
    toolbar_item.set_stock_id(gtk.STOCK_OPEN)
    toolbar_item.connect("clicked", self.openBookCallback, toolbar_item)
    toolbar_item.show()
    self.toolbar.insert(toolbar_item, -1)

    self.toolbar_item2 = gtk.ToggleToolButton(gtk.STOCK_MEDIA_PLAY)
    #self.toolbar_item2.set_stock_id(gtk.STOCK_MEDIA_PAUSE)
    self.toolbar_item2.set_active(False)

    self.toolbar_item2.connect("clicked", self.c.switchStateCallback, self.toolbar_item2)
    self.toolbar_item2.show()
    self.toolbar.insert(self.toolbar_item2, -1)
    
    toolbar_item3 = gtk.ToolButton(_("Stop"))
    toolbar_item3.set_stock_id(gtk.STOCK_MEDIA_STOP)
    toolbar_item3.connect("clicked", self.c.stopCallback, toolbar_item3)
    toolbar_item3.show()
    self.toolbar.insert(toolbar_item3, -1)

    
    toolbar_item6 = gtk.ToolButton(_("Next Chapter"))
    toolbar_item6.set_stock_id(gtk.STOCK_MEDIA_REWIND)
    toolbar_item6.connect("clicked", self.c.goToNextChapterCallback, toolbar_item6)
    toolbar_item6.show()
    self.toolbar.insert(toolbar_item6, -1)
    
    toolbar_item4 = gtk.ToolButton(_("Previous Chapter"))
    toolbar_item4.set_stock_id(gtk.STOCK_MEDIA_FORWARD)
    toolbar_item4.connect("clicked", self.c.goToPriorChapterCallback, toolbar_item4)
    toolbar_item4.show()
    self.toolbar.insert(toolbar_item4, -1)

    iconw = gtk.Image() # icon widget
    iconw.set_from_file("@prefix@/share/icons/gnome/32x32/actions/bookmarks.png")

    toolbar_item5 = gtk.ToolButton(iconw,_("Set Bookmark"))
    #toolbar_item5.set_stock_id(gtk.STOCK_INDEX)
    toolbar_item5.connect("clicked", self.c.createBookmarkCallback, toolbar_item5)
    toolbar_item5.show()
    self.toolbar.insert(toolbar_item5, -1)

    main_box.pack_start(self.toolbar, False, True, 0)
    self.toolbar.show()


    # Creates a  TreeStore with a text column.
    self.treestore = gtk.TreeStore(str)

    # Creation of TreeView using the treestore
    self.treeview = gtk.TreeView(self.treestore)

    # Creation of the TreeViewColumn for displaying data
    self.tvcolumn = gtk.TreeViewColumn(_("Table of contents"))

    # Add the column to the treeview
    self.treeview.append_column(self.tvcolumn)

    # Create a CellRendererText  for displaying data
    self.cell = gtk.CellRendererText()

    # Add the cell to the column and let expand it
    self.tvcolumn.pack_start(self.cell, True)

    # Include "text" attribute to the column 0 - return text
    # from the column into tree.
    self.tvcolumn.add_attribute(self.cell, 'text', 0)


    # Make it searchable
    self.treeview.set_search_column(0)
    self.treeselection = self.treeview.get_selection()

    self.cursorChanged = self.treeview.connect("cursor-changed", self.updateAudio)


    book_window = gtk.ScrolledWindow()
    book_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    book_window.show()
    book_window.add_with_viewport(self.treeview)


    self.treeview.show_all()

    general_box = gtk.VBox(False, 1)
    general_box.set_border_width(1)
    self.window.add(general_box)
    general_box.show()
    general_box.pack_start(main_box, False, True, 0)
    general_box.pack_start(book_window, True, True, 0)


    self.window.show_all()
    list, toc_position = self.c.getConfiguration()
    if len(list) > 0:
      self.displayBook(list)
      self.updateView(toc_position)
      self.c.loadLatestBook()
    
    self.treeview.grab_focus()

  def view_play_icon(self):
    """
    Changes play icon at toolbar
    """
    self.toolbar_item2.set_active(False)
    #self.toolbar_item2.show()

  def view_pause_icon(self):
    """
    Changes play buton at toolbar to pause
    """
    self.toolbar_item2.set_active(True)
    #self.toolbar_item2.show()
    
  def openBookCallback(self, w, data):
    """
    Displays the book when open book menu item is selected
    """
    list = self.c.openBook(w)
    self.displayBook(list)
    self.c.syncViewAudio()


  def displayBook(self, list):
    """
    Displays book when starting application
    """
    self.clearModel()
    l = []
    for x in range(len(list)):
      y = list[x].childNodes
      z = y[0].firstChild.toprettyxml()
      l.append(y[0])
      iter = self.treestore.append(None, ['%s' % z])
    title = self.c.displayBookTitle()
    # Translators: this string the DBR application window title when the user opening a daisy book. %s variable containing the opened daisy book title
    self.window.set_title(_("Daisy Book Reader - %s") %(title))


  def clearModel(self):
    """
    Clears the tree model 
    """
    self.treestore.clear()
    self.window.set_title(_("Daisy Book Reader"))



  def updateView(self, n):
    """
    Updates the cursor view of the treeview
    """
    t = (n)
    self.treeview.handler_block(self.cursorChanged)
    self.treeview.set_cursor_on_cell(t, self.tvcolumn, self.cell)
    self.treeview.handler_unblock(self.cursorChanged)
    self.c.syncViewAudio()

  def updateAudio(self, data):
    """
    Updates the audio when user moves cursor
    """
    cursor_pos = self.treeview.get_cursor()
    aux = list(cursor_pos)
    print aux
    listed = list(aux[0])
    self.c.syncAudioView(listed[0])


  def closeApplication(self, w, data):
    """
    Closes the application from menu
    """
    self.c.closeApplication()
    gtk.main_quit()


  def destroyApplication(self, widget):
    """
    Closes application when destroy signal is emmited
    """
    self.c.closeApplication()
    gtk.main_quit()
