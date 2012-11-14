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

import pickle
import os

from dbr_i18n import _          #For i18n support

class Settings:
  """
  Handles working with configuration and bookmarks 
  """

  def __init__(self):
    """
    This class gets configuration for application
    """
    home = os.path.expanduser('~')
    self.config_file = home + "/" + ".dbr"
 #fjdm: we need to create a new configuration system.
    if os.path.exists(self.config_file):
      f = open(self.config_file, "r")
      self.settings = pickle.load(f)
      f.close()
    else:
      self.createConfigFile()


  def saveConfiguration(self, info):
    """
    Saves configuration and latest book reading position to the config file
    info: Configuration and book position for the latest read book
    """
    self.settings[0] = info
    f = open(self.config_file, "w")
    pickle.dump(self.settings, f)
    f.close()


  def getConfiguration(self):
    """
    Gets configuration and latest read book
    """
    return self.settings[0]


  def createConfigFile(self):
    """
    Creates DBR configuration if not exists
    """
    self.settings = [0]
    config = [None, None, [0, 0, 0], 1]
    self.settings[0] = config
    f = open(self.config_file, "w")
    pickle.dump(self.settings, f)
    f.close()


  def createBookmark(self, bookmark):
    """
    Creates or update a bookmark and saves it in the config file
    bookmark: Needed information for the bookmark
    """
    aux = [0]
    # First we look if book was previously saved
    if len(self.settings) > 1:
      i = 0
      found = 0
      while (i < (len(self.settings)-1)) and found == 0:
        i = i + 1
        if self.settings[i][0] == bookmark[0]:
          found = 1
      if found == 1:
        # The book is saved
        # Look for the bookmark if was previously saved
        j = 1
        finish = 0
        while (j < (len(self.settings[i])-1)) and (finish == 0):
          j = j + 1
          if self.settings[i][j][0] == bookmark[5]:
            finish = 1
        if finish == 1:
          # Bookmark exists
          self.settings[i][j][1:4] = bookmark[2:5]
        else:
          # Bookmark doesn't exist
          aux[0] = bookmark[5]
          aux = aux + bookmark[2:5]
          self.settings[i].append(aux)
      else:
        # The book doesn't exist
        self.settings.append(bookmark[0:2])
        aux[0] = bookmark[5]
        aux = aux + bookmark[2:5]
        self.settings[i+1].append(aux)
    else:
      # There are not any book saved
      self.settings.append(bookmark[0:2])
      aux[0] = bookmark[5]
      aux = aux + bookmark[2:5]
      pos = len(self.settings) - 1
      self.settings[pos].append(aux)
    print self.settings #dbg
    f = open(self.config_file, "w")
    pickle.dump(self.settings, f)
    f.close()


  def getBookmarksForBook(self, book_title):
    """
    Returns bookmarks for a specified book
    """
    # Look if there is any book with bookmarks
    if len(self.settings) > 1:
      i = 0
      found = 0
      while (i < (len(self.settings)-1)) and found == 0:
        i = i + 1
        if self.settings[i][0] == book_title:
          found = 1
      if found == 1:
        # Get available bookmarks
        bookmarks = []
        j = 2
        while (j < len(self.settings[i])):
          bookmarks.append(self.settings[i][j])
          j = j + 1
      else:
        bookmarks = []
    else:
      bookmarks = []
    return bookmarks


  def deleteBookmark(self, book_title, bookmark_pos):
    """
    Deletes a bookmark for a specified book
    """
    i = 0
    found = 0
    while (i < len(self.settings)) and (found == 0):
      i = i + 1
      if book_title == self.settings[i][0]:
        found = 1
    if len(self.settings[i]) == 3:
      self.settings.pop(i)
    else:
      self.settings[i].pop(bookmark_pos+2)
    f = open(self.config_file, "w")
    pickle.dump(self.settings, f)
    f.close()


  def getBooks(self):
    """
    Returns the books saved in the config file
    """
    books = []
    if len(self.settings) > 1:
      i = 0
      while (i < (len(self.settings)-1)):
        i = i + 1
        if os.path.exists(self.settings[i][1]):
          books.append(self.settings[i][0:2])
    return books
