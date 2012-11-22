# -*- coding: iso-8859-15 -*-
# Copyright (C) 2008, 2009 Rafael Cantos Villanueva
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


import xml.dom.minidom as MD

from dbr_i18n import _          #For i18n support

class Book:
  """
  This class handles DTB manipulation
  """


  def __init__(self, file, ncc_pos=0, audio_index=0):
    """
    Initializes book object which can access all DAISY elements
    file: The ncc.html or main ncc file.
    ncc_pos: Position in the list of ncc entries from We should start reading.
    audio_index: Index of the audio track We should begin to play
    """
    self.ncc = [] #Contains all the valid DAISY entries in ncc.
    self.next_ncc_pos = self.ncc_pos = ncc_pos #Points to the next ncc entry to play
    self.audio_index = audio_index 
    self.tree = MD.parse(file)
    self.book_title = self.getBookTitle()
    self.book_path = file
#Possible class values for an entry in ncc
    self._valid_ncc_class=['title', 'chapter', 'section', 'sub-section', 'jacket', 'front', 'title-page', 'copyright-page', 'acknowledgement', 'prolog', 'introduction', 'dedication', 'foreword', 'preface', 'print-toc', 'part', 'minor-head', 'bibliography', 'glosary', 'appendix', 'index', 'index-category']
    self.getTree()
    self.getAudioTracks(self.ncc[self.ncc_pos])


  def getBookTitle(self):
    """
    Returns the book's title
    """
    book_title = ''
    meta = self.tree.getElementsByTagName('meta')
    for i in range(len(meta)):
      if meta[i].hasAttribute('name'):
        if meta[i].attributes['name'].value == 'dc:title':
          book_title = meta[i].attributes['content'].value
          break
    return book_title

  def getNumberOfPages(self):
    """
    Returns the total number of pages in the book
    """
    meta = self.tree.getElementsByTagName('meta')
    for i in range(len(meta)):
      if meta[i].hasAttribute('name'):
        if (meta[i].attributes['name'].value == 'ncc:pageNormal') or (meta[i].attributes['name'].value == 'ncc:page-normal'):
          number_of_pages = meta[i].attributes['content'].value
          break
    return number_of_pages


  def getExactPosition(self):
    """
    Returns  current playing and book position for saving a bookmark
    """
    info = []
    info.append(self.book_title)
    info.append(self.book_path)
    info.append(self.ncc_pos)
    info.append(self.audio_index-1)
    return info


  def getNcc(self):
    """
    Returns the table of contents from the book's ncc
    """
    return self.ncc


  def getNccPosition(self):
    """
    Returhns the current toc position
    """
    return self.ncc_pos


  def getCurrentNode(self):
    """
    Returns the current playing book node
    """
    return self.ncc[self.ncc_pos]


  def getSubTree(self, nodelist, list):
    """
    Gets a subtree of ncc's content
    """
    for x in nodelist:
      if len(x.childNodes) > 1:
        list = self.getSubTree(x.childNodes, list)
      elif len(x.childNodes) == 1 and x.hasAttribute('class'):
        at = x.attributes['class']
        if (at.value in self._valid_ncc_class) or x.tagName == u'span':
          list.append(x)
        elif not x.hasAttribute('class'):
          list.append(x)
    return list

  def getTree(self):
    """
    Gets book's ncc content
    """
    list = []
    nodes = self.tree.getElementsByTagName('body')
    size = len(nodes)
    if size >= 1:
      list = self.getSubTree(nodes, list)
      self.ncc = list

  def getChapters(self):
    """
    Returns list of chapter and their position in the ncc
    """
    i = 0
    chapters = []
    chapters_pos = []
    for i in range(len(self.ncc)):
      if self.ncc[i].hasAttribute('class'):
        classval = self.ncc[i].attributes['class'].value
        if classval == 'chapter':
          chapter_name = self.ncc[i].childNodes[0].firstChild.toprettyxml()
          chapters.append(chapter_name)
          chapters_pos.append(i)
    return chapters, chapters_pos

  def nextOrPriorChapter(self, pos):
    """
    Changes to the next or prior chapter
    pos: Wether is next or prior chapter
    """
    found = False
    new_ncc_pos = self.ncc_pos
    while (not found) and (new_ncc_pos > 0) and (new_ncc_pos < len(self.ncc)):
      new_ncc_pos = new_ncc_pos + pos
      if new_ncc_pos < len(self.ncc):
        if self.ncc[new_ncc_pos].hasAttribute('class'):
          classval = self.ncc[new_ncc_pos].attributes['class'].value
          if classval == 'chapter':
            found = True
          self.next_ncc_pos = self.ncc_pos = new_ncc_pos
          self.audio_index = 0
    return found

  def nextOrPriorPage(self, pos):
    """
    Changes next or prior page
    pos: Wether is next or prior page
    """
    found = False
    new_ncc_pos = self.ncc_pos
    while (not found) and (new_ncc_pos > 0) and (new_ncc_pos < len(self.ncc)):
      new_ncc_pos = new_ncc_pos + pos
      if new_ncc_pos < len(self.ncc):
        if self.ncc[new_ncc_pos].hasAttribute('class'):
          classval = self.ncc[new_ncc_pos].attributes['class'].value
          if classval == 'page-normal':
            self.ncc_pos=new_ncc_pos
            found = True
    return found

  def setReadPosition(self, ncc_pos, audio_index):
    """
    Sets current reading position in ncc and audio
    """
    self.ncc_pos = self.next_ncc_pos = ncc_pos
    self.audio_index = audio_index
    self.getAudioTracks(self.ncc[self.ncc_pos])

  def goToPage(self, page):
    """
    Go to a specified page 
    """
    page = int(page)
    number_of_pages = self.getNumberOfPages()
    number_of_pages = int(number_of_pages)
    i = 0
    found = False
    realized = 0 
    if (page >= 0) and (page <= number_of_pages):
      while (i < len(self.ncc)) and (not found):
        if self.ncc[i].hasAttribute('class'):
          classval = self.ncc[i].attributes['class'].value
          if classval == "page-normal":
            num = self.ncc[i].childNodes[0].firstChild
            if page == int(num.toprettyxml()):
              found = True
        i = i + 1
    return found, i


  def nextOrPriorText(self, pos):
    """
    Set to next or prior chunk of text
    pos: Wether to search forward or backward
    """
    found = 0
    realized = 0
    new_booknodes_pos = self.pos_booknodes
    while (found == 0) and (new_booknodes_pos > 0) and (new_booknodes_pos < len(self.booknodes)):
      new_booknodes_pos = new_booknodes_pos + pos
      if new_booknodes_pos < len(self.booknodes):
        if self.booknodes[new_booknodes_pos].hasAttribute('class'):
          classval = self.booknodes[new_booknodes_pos].attributes['class'].value
          if classval == 'group':
            found = 1
            realized = 1
    if found == 1:
      self.updateTocPosition(new_booknodes_pos)
    return realized


  def getAudioTrack(self):
    """
    Gets an audio track and its begin and end playing time
    """
    print "antes ncc pos es " + str(self.ncc_pos) + "y next ncc pos es " + str(self.next_ncc_pos)
    if self.next_ncc_pos == (self.ncc_pos + 1):
      self.ncc_pos = self.next_ncc_pos
    if self.audio_index == -1:
      self.audio_index = 0
    file = self.m[self.audio_index][0]
    pos_begin = self.m[self.audio_index][1]
    pos_end = self.m[self.audio_index][2]
    if (self.audio_index < (len(self.m)-1)) and (self.audio_index >= 0):
      self.audio_index = self.audio_index + 1
    else:
      if self.ncc_pos < (len(self.ncc)-1):
        self.next_ncc_pos = self.next_ncc_pos + 1
        self.audio_index = 0
        self.getAudioTracks(self.ncc[self.next_ncc_pos])
      else:
        self.next_ncc_pos = self.ncc_pos = 0
        self.audio_index = 0
    print "despues ncc pos es " + str(self.ncc_pos) + "y next ncc pos es " + str(self.next_ncc_pos)
    return file, pos_begin, pos_end


  def getAudioTracks(self, node):
    """
    Gets all audio tracks of node
    node: node which audio tracks are going to be gotten
    """
    m = []
    self.path = self.book_path.split("ncc.html")
    a = node.getElementsByTagName('a')
    val = a[0].attributes['href']
    uri = val.value.split("#")
#    print "SMIL file: " + uri[0] #dbg
    full_path = self.path[0] + uri[0]
#    print "Full path to the file is: " + full_path #dbg
    smil = MD.parse(full_path) #Parse the smil file
    seq = smil.getElementsByTagName('seq')
    par = seq[0].getElementsByTagName('par')
    if len(par) > 0:
      for i in range(len(par)):
        text = par[i].getElementsByTagName('text')
        if (par[i].hasAttribute('id') and par[i].getAttribute('id') == uri[1]) or (text[0].hasAttribute('id') and text[0].getAttribute('id') == uri[1]):
          audio = par[i].getElementsByTagName('audio')
          for j in range(len(audio)):
            if audio[j].hasAttribute('clip-begin'):
              audio_path = self.path[0] + audio[j].attributes['src'].value
              l = []
              l.append(audio_path)
              begin = self.getNanoseconds(audio[j].attributes['clip-begin'].value)
              l.append(begin)
              end = self.getNanoseconds(audio[j].attributes['clip-end'].value)
              l.append(end)
#            print "Audio track " + str(j)+ "\n" + "Audio file is: " + str(l[0]) + "Begins at " + str(l[1]) + " and ends at " + str(l[2]) #dbg
              m.append(l)
    else:
      print "no hay pares"
      audio = seq[0].getElementsByTagName('audio')
      for j in range(len(audio)):
        if audio[j].hasAttribute('clip-begin'):
          audio_path = self.path[0] + audio[j].attributes['src'].value
          l = []
          l.append(audio_path)
          begin = self.getNanoseconds(audio[j].attributes['clip-begin'].value)
          l.append(begin)
          end = self.getNanoseconds(audio[j].attributes['clip-end'].value)
          l.append(end)
          m.append(l)
#          print "Audio track " + str(j) + "\n" + "Audio file is: " + str(l[0]) + "Begins at " + str(l[1]) + " and ends at " + str(l[2]) #dbg
    self.m = m


  def getNanoseconds(self, audio):
    """
    Returns time in nanoseconds of a given string value
    """
    aux = audio.split("=")
    time = aux[1].split("s")
    aux = float(time[0]) * 1000000000
    ns = int(aux)
    return ns


  def getBookInfo(self):
    """
    Returns general book information    """
    l = []
    info = ''
    separator = ''
    v = ['ncc:sourceTitle', 'dc:title', 'dc:creator', 'ncc:sourceEdition', 'ncc:sourceDate', 'ncc:sourcePublisher', 'ncc:sourceRights']
    data = self.tree.getElementsByTagName('meta')
    for i in range(len(v)):
      for x in data:
        if x.hasAttribute('name'):
          at = x.attributes['name']
          if at.value == v[i]:
            l.append(x.attributes['content'].value)
            l.append("\n")
    info = separator.join(l)
    return info


  def getBookTranslationInfo(self):
    """
    Returns book translation information
    """
    l = []
    info = ''
    separator = ''
    v = ['ncc:sourceTitle', 'dc:title', 'dc:publisher', 'dc:identifier', 'ncc:producer', 'ncc:narrator', 'dc:date', 'dc:format', 'ncc:totalTime', 'ncc:totaltime']
    data = self.tree.getElementsByTagName('meta')
    for i in range(len(v)):
      for x in data:
        if x.hasAttribute('name'):
          at = x.attributes['name']
          if at.value == v[i]:
            l.append(x.attributes['content'].value)
            l.append("\n")
    info = separator.join(l)
    return info


  def getPlayingTime(self):
    """
    Returns current playing time in seconds
    """
    audio_index = self.audio_index
    node = self.ncc_pos
    duration = 0
    i = 0
    while i <= node:
      href = self.ncc[i].firstChild.attributes['href'].value
      smil = href.split("#")
      full_path = self.path[0] + smil[0]
      file = MD.parse(full_path)
      if i < node:
        seq = file.getElementsByTagName('seq')
        par = seq[0].getElementsByTagName('par')
        j = 0
        for j in range(len(par)):
          text = par[j].getElementsByTagName('text')
          at = text[0].attributes['id'].value
          if at == smil[1]:
            audio = par[j].getElementsByTagName('audio')
            k = 0
            for k in range(len(audio)):
              if audio[k].hasAttribute('clip-begin'):
                begin = self.getNanoseconds(audio[k].attributes['clip-begin'].value)
                end = self.getNanoseconds(audio[k].attributes['clip-end'].value)
                aux = end - begin
                duration = duration + aux
              k = k + 1
          j = j + 1 
      elif i == node:
        seq = file.getElementsByTagName('seq')
        par = seq[0].getElementsByTagName('par')
        j = 0
        for j in range(len(par)):
          text = par[j].getElementsByTagName('text')
          at = text[0].attributes['id'].value
          if at == smil[1]:
            audio = par[j].getElementsByTagName('audio')
            k = 0
            while k < audio_index:
              if audio[k].hasAttribute('clip-begin'):
                begin = self.obtener_tiempo(audio[k].attributes['clip-begin'].value)
                end = self.getNanoseconds(audio[k].attributes['clip-end'].value)
                aux = end - begin
                duration = duration + aux
              k = k + 1
            aux = audio[k].attributes['clip-begin'].value
            begin = self.getNanoseconds(aux)
            aux = begin / 1000000000
            aux = int(aux)
          j = j + 1
      i = i + 1
    seconds = duration / 1000000000
    return seconds, aux


  def getBookDuration(self):
    """
    Returns time duration of the book
    """
    i = 0
    found = 0
    meta = self.tree.getElementsByTagName('meta')
    while (i < len(meta)) and (found == 0):
      if meta[i].hasAttribute('name'):
        if (meta[i].attributes['name'].value == 'ncc:totalTime') or (meta[i].attributes['name'].value == 'ncc:totaltime'):
          book_duration = meta[i].attributes['content'].value
          found = 1
      i = i + 1
    aux = book_duration.split(":")
    book_duration = int(aux[0]) * 3600
    book_duration = book_duration + int(aux[1]) * 60
    book_duration = book_duration + int(aux[2])
    return float(book_duration)


  def getFormatedTime(self, time_int):
    """
    Get time in hh:mm:ss format
    """
    time_str = ""
    time_int = int(time_int)
    if time_int >= 3600:
      _hours = time_int / 3600
      time_int = time_int - (_hours * 3600)
      time_str = str(_hours) + ":"
    if time_int >= 600:
      _mins = time_int / 60
      time_int = time_int - (_mins * 60)
      time_str = time_str + str(_mins) + ":"
    elif time_int >= 60:
      _mins = time_int /60
      time_int = time_int - (_mins * 60)
      time_str = time_str + "0" + str(_mins) + ":"
    else:
      time_str = time_str + "00:"
    if time_int > 9:
      time_str = time_str + str(time_int)
    else:
      time_str = time_str + "0" + str(time_int)
    return time_str
