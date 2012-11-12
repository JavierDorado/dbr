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


  def __init__(self, file, pos_begin=0, pos_booknodes=0, audio_pos=0):
    """
    Initializes book object which can access all DAISY elements
    """
    self.toc = [] #Contains all the valid DAISY entries in ncc.
    self.booknodes = [] #Contains list of nodes in ncc.
    self.next_toc_pos = self.toc_pos = pos_booknodes
    self.next_booknodes_pos = self.pos_booknodes = pos_booknodes
    self.audio_pos = audio_pos
    self.tree = MD.parse(file)
    self.book_name = self.getBookName()
    self.book_path = file
    self.getTree()
    self.getAudioTracks(self.booknodes[self.pos_booknodes])

  def getBookName(self):
    """
    Returns the book's name
    """
    book_name = ''
    meta = self.tree.getElementsByTagName('meta')
    found = 0
    i = 0
    while found == 0 and i < len(meta): #fjdm: Need to change this structure 
      if meta[i].hasAttribute('name'):
        if meta[i].attributes['name'].value == 'dc:title':
          book_name = meta[i].attributes['content'].value
          found = 1
      i = i+1
    return book_name


  def getNumberOfPages(self):
    """
    Returns the total number of pages in the book
    """
    meta = self.tree.getElementsByTagName('meta')
    found = 0
    i = 0
    while (found == 0) and (i < len(meta)): #fjdm: change this structure 
      if meta[i].hasAttribute('name'):
        if (meta[i].attributes['name'].value == 'ncc:pageNormal') or (meta[i].attributes['name'].value == 'ncc:page-normal'):
          number_of_pages = meta[i].attributes['content'].value
          found = 1
      i = i+1
    return number_of_pages


  def getExactPosition(self):
    """
    Returns  current playing and book position for saving a bookmark
    """
    info = []
    info.append(self.book_name)
    info.append(self.book_path)
    info.append(self.toc_pos)
    info.append(self.pos_booknodes)
    info.append(self.audio_pos-1)
    return info


  def getToc(self):
    """
    Returns the table of contents from the book's ncc
    """
    return self.toc


  def getTocPosition(self):
    """
    Returhns the current toc position
    """
    return self.toc_pos


  def getCurrentNode(self):
    """
    Returns the current playing book node
    """
    return self.booknodes[self.pos_booknodes]


  def getSubTree(self, nodelist, list, list1):
    """
    Gets a subtree of ncc's content
    """
    for x in nodelist:
      if len(x.childNodes) > 1:
        list, list1 = self.getSubTree(x.childNodes, list, list1)
      elif len(x.childNodes) == 1:
        list1.append(x)
        if x.hasAttribute('class'):
          at = x.attributes['class']
#fjdm: need to change following
          if ((at.value == 'title') or (at.value == 'chapter') or (at.value == 'section') or (at.value == 'sub-section') or(at.value == 'jacket') or (at.value == 'front') or (at.value == 'title-page') or (at.value == 'copyright-page') or (at.value == 'acknowledgement') or (at.value == 'prolog') or (at.value == 'introduction') or (at.value == 'dedication') or (at.value == 'foreword') or (at.value == 'preface') or (at.value == 'print-toc') or (at.value == 'part') or (at.value == 'minor-head') or (at.value == 'bibliography') or (at.value == 'glosary') or (at.value == 'appendix') or (at.value == 'index') or (at.value == 'index-category')):
            list.append(x)
        elif not x.hasAttribute('class'):
          list.append(x)
    return list, list1


  def getTree(self):
    """
    Gets book's toc and booknodes
    """
    list = []
    list1 = []
    nodes = self.tree.getElementsByTagName('body')
    size = len(nodes)
    # Si existe el arbol, se muestra
    if size >= 1:
      list, list1 = self.getSubTree(nodes, list, list1)
      self.toc = list
      self.booknodes = listado


  def getChapters(self):
    """
    Returns list of chapter and their position in the booknodes
    """
    i = 0
    chapters = []
    chapters_pos = []
    while (i < len(self.toc)): #fjdm: change this
      if self.toc[i].hasAttribute('class'):
        classval = self.toc[i].attributes['class'].value
        if classval == 'chapter':
          chapter_name = self.toc[i].childNodes[0].firstChild.toprettyxml()
          chapters.append(chapter_name)
          chapters_pos.append(i)
      i = i + 1
    return chapters, chapters_pos

  def nextOrPriorChapter(self, pos):
    """
    Changes to the next or prior chapter
    pos: Wether is next or prior chapter
    """
    found = 0
    realized = 0
    new_toc_pos = self.toc_pos
    while (found == 0) and (new_toc_pos > 0) and (new_toc_pos < len(self.toc)):
      new_toc_pos = new_toc_pos + pos
      if new_toc_pos < len(self.toc):
        if self.toc[new_toc_pos].hasAttribute('class'):
          classval = self.toc[nueva_pos_indice].attributes['class'].value
          if classval == 'chapter':
            found = 1
            realized = 1
        elif not self.toc[new_toc_pos].hasAttribute('class'):
          found = 1
          realized = 1
    if found == 1:
      id_toc = self.toc[new_toc_pos].attributes['id'].value
      found = 0
      i = 0
      while (found == 0) and (i < len(self.booknodes)):
        id_booknode = self.booknodes[i].attributes['id'].value
        if id_toc == id_booknode:
          found = 1
          self.next_toc_pos = self.toc_pos = new_toc_pos
          self.next_booknodes_pos = self.pos_booknodes = i
        self.audio_pos = 0
        i = i + 1
    return realized

  def nextOrPriorPage(self, pos):
    """
    Changes next or prior page
    pos: Wether is next or prior page
    """
    found = 0
    realized = 0
    new_pos_booknodes = self.pos_booknodes
    while (found == 0) and (new_booknodes_pos > 0) and (new_pos_booknodes < len(self.booknodes)):
      new_pos_booknodes = new_pos_booknodes + pos
      if new_pos_booknodes < len(self.booknodes):
        if self.booknodes[new_pos_booknodes].hasAttribute('class'):
          classval = self.booknodes[new_pos_booknodes].attributes['class'].value
          if classval == 'page-normal':
            found = 1
            realized = 1
    if found == 1:
      self.updateTocPosition(new_pos_booknodes)
    return realized


  def updateTocPosition(self, new_pos_booknodes):
    """
    Updates toc position related to booknodes position
    new_pos_booknodes: New position in the booknodes list
    """
    found = 0
    i = new_pos_booknodes
    while (found == 0) and (i > 0):
      i = i - 1
      if self.booknodes[i].hasAttribute('class'):
        classval = self.booknodes[i].attributes['class'].value
        if (classval == 'title') or (classval == 'jacket') or (classval == 'front') or (classval == 'title-page') or (classval == 'copyright-page') or (classval == 'acknowledgement') or (classval == 'prolog') or (classval == 'introduction') or (classval == 'dedication') or (classval == 'foreword') or (classval == 'preface') or (classval == 'print-toc') or (classval == 'part') or (classval == 'chapter') or (classval == 'section') or (classval == 'sub-section') or (classval == 'minor-head') or (classval == 'bibliography') or (classval == 'glossary') or (classval == 'appendix') or (classval == 'index') or (classval == 'index-category'):
          id_booknodes = self.booknodes[i].attributes['id'].value
          found = 1
          finished = 0
          j = len(self.toc)-1
          while (finished == 0) and (j >= 0):
            id_toc = self.toc[j].attributes['id'].value
            if id_toc == id_booknodes:
              self.next_toc_pos = self.toc_pos = j
              self.next_pos_booknodes = self.pos_booknodes = new_pos_booknodes
              self.audio_pos = 0
              finished = 1
            if j > 0:
              j = j - 1
      elif not self.booknodes[i].hasAttribute('class'):
        id_booknodes = self.booknodes[i].attributes['id'].value
        found = 1
        finished = 0
        j = len(self.toc)-1
        while (finished == 0) and (j >= 0):
          id_toc = self.toc[j].attributes['id'].value
          if id_toc == id_booknodes:
            self.next_toc_pos = self.toc_pos = j
            self.next_pos_booknodes = self.pos_booknodes = new_pos_booknodes
            self.audio_pos = 0
            finished = 1
          if j > 0:
            j = j - 1


  def UpdateBooknodesPosition(self, new_toc_pos):
    """
    Updates booknodes position related to toc position
    new_toc_pos: New position in toc
    """
    found = 0
    i = 0
    id_toc = self.toc[new_toc_pos].attributes['id'].value
    while (found == 0) and (i < (len(self.booknodes)-1)):
      id_booknodes = self.booknodes[i].attributes['id'].value
      if id_toc == id_booknodes:
        self.next_toc_pos = self.toc_pos = new_toc_pos
        self.next_pos_booknodes = self.pos_booknodes = i
        self.audio_pos = 0
        self.getAudioTracks(self.booknodes[self.pos_booknodes])
        found = 1
      i = i + 1

  def setReadPosition(self, toc_pos, pos_booknodes, audio_pos):
    """
    Sets current reading position in booknodes, toc and audio
    """
    self.toc_pos = self.next_toc_pos = toc_pos
    self.pos_booknodes = self.next_pos_booknodes = pos_booknodes
    self.audio_pos = audio_pos
    self.getAudioTracks(self.booknodes[self.pos_booknodes])


  def goToPage(self, page):
    """
    Go to a specified page 
    """
    page = int(page)
    number_of_pages = self.getNumberOfPages()
    number_of_pages = int(number_of_pages)
    i = 0
    found = 0
    realized = 0 
    if (page >= 0) and (page <= number_of_pages):
      while (i < len(self.booknodes)) and (found == 0):
        if self.booknodes[i].hasAttribute('class'):
          classval = self.booknodes[i].attributes['class'].value
          if classval == "page-normal":
            num = self.booknodes[i].childNodes[0].firstChild
            if page == int(num.toprettyxml()):
              found = 1
              realized = 1
              self.updateTocPosition(i)
        i = i + 1
    return realized, i


  def getText(self, pos):
    """
    Set to next or prior chunk of text
    pos: Wether to search forward or backward
    """
    found = 0
    realized = 0
    new_pos_booknodes = self.pos_booknodes
    while (found == 0) and (new_pos_booknodes > 0) and (new_pos_booknodes < len(self.booknodes)):
      new_pos_booknodes = new_pos_booknodes + pos
      if new_pos_booknodes < len(self.booknodes):
        if self.booknodes[new_pos_booknodes].hasAttribute('class'):
          classval = self.booknodes[new_pos_booknodes].attributes['class'].value
          if classval == 'group':
            found = 1
            realized = 1
    if found == 1:
      self.updateTocPosition(new_pos_booknodes)
    return realized


  def getAudioTrack(self):
    """
    Gets an audio track and its begin and end playing time
    """
    if self.next_pos_booknodes == (self.pos_booknodes + 1):
      self.pos_booknodes = self.next_pos_booknodes
    if self.next_toc_pos == (self.toc_pos + 1):
      self.toc_pos = self.next_toc_pos
    if self.audio_pos == -1:
      self.audio_pos = 0
    file = self.m[self.audio_pos][0]
    pos_begin = self.m[self.audio_pos][1]
    pos_end = self.m[self.audio_pos][2]
    if (self.audio_pos < (len(self.m)-1)) and (self.audio_pos >= 0):
      self.audio_pos = self.audio_pos + 1
    else:
      if self.pos_booknodes < (len(self.booknodes)-1):
        ind_id = self.toc[self.toc_pos].attributes['id'].value
        nod_id = self.booknodes[self.pos_booknodes].attributes['id'].value
        ind_next_id = self.toc[self.toc_pos+1].attributes['id'].value
        nod_next_id = self.booknodes[self.pos_booknodes+1].attributes['id'].value
        if (ind_id == nod_id) or (ind_next_id == nod_next_id):
          self.next_toc_pos = self.next_toc_pos + 1
        self.next_pos_booknodes = self.next_pos_booknodes + 1
        self.audio_pos = 0
        self.getAudioTracks(self.booknodes[self.next_pos_booknodes])
      else:
        self.next_toc_pos = self.toc_pos = 0
        self.next_pos_booknodes = self.pos_booknodes = 0
        self.audio_pos = 0
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
    file = val.value.split("#")
#    print "SMIL file: " + file[0] #dbg
    full_path = self.path[0] + file[0]
#    print "Full path to the file is: " + full_path #dbg
    smil = MD.parse(full_path) #Parse the smil file
    seq = smil.getElementsByTagName('seq')
    par = seq[0].getElementsByTagName('par')
    if len(par) > 0:
      for i in range(len(par)):
        text = par[i].getElementsByTagName('text')
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
    audio_pos = self.audio_pos
    node = self.pos_booknodes
    duration = 0
    i = 0
    while i <= node:
      href = self.booknodes[i].firstChild.attributes['href'].value
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
            while k < audio_pos:
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
