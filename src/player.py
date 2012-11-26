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


import sys, os, os.path, time
import pygst
pygst.require("0.10")
import gst

from dbr_i18n import _          #For i18n support

class Player:
  """
  Class to handle playback of a DTB
  """



  def setController(self, c):
    self.c = c

  def __init__(self):
    """
    Initializes the player for playing audio tracks of the DTB
    """
    self._state = "Stopped"
    self.time_format = gst.Format(gst.FORMAT_TIME)
    self.player = gst.Pipeline("player")
    source = gst.element_factory_make("filesrc", "file-source")
    self.player.add(source)
    decoder = gst.element_factory_make("mad", "mp3-decoder")
    self.player.add(decoder)
    conv = gst.element_factory_make("audioconvert", "converter")
    self.player.add(conv)
    volume = gst.element_factory_make("volume", "volume")
    self.player.add(volume)
#     speed = gst.element_factory_make("speed", "speed")
    # self.player.add(speed)
    sink = gst.element_factory_make("pulsesink", "pulseaudio-output")
    self.player.add(sink)
    gst.element_link_many(source, decoder, conv, volume, sink)
    self.player.set_state(gst.STATE_NULL)
    bus = self.player.get_bus()
    bus.add_signal_watch()
    bus.connect('message', self.onMessage)

  def play(self, file, pos_begin, pos_end):
    """
    Function for playing an audio track.
    file: filename which to play
    pos_begin: Begin position for playing
    pos_end: End position for playing
    """
    if self._state == "Stopped" or self.player.get_by_name("file-source").get_property('location') != file:
      if os.path.exists(file) and self.player.get_by_name("file-source").get_property('location') != file:
        self.player.set_state(gst.STATE_NULL)
        self.player.get_by_name("file-source").set_property('location', file)
    time.sleep(0.1)
    self.player.set_state(gst.STATE_PAUSED)
    print "file:" + file + "set position begin at " + str(pos_begin) + " and end position at " + str(pos_end) #dbg
    if self.player.seek(1.0, self.time_format, gst.SEEK_FLAG_FLUSH | gst.SEEK_FLAG_SEGMENT, gst.SEEK_TYPE_SET, pos_begin, gst.SEEK_TYPE_SET, pos_end):
      time.sleep(0.2)
      self._state="Playing"
      self.player.set_state(gst.STATE_PLAYING)
    else:
      print "Can not seek. Trying a simple seek." #dbg
      self.player.set_state(gst.STATE_PAUSED)
      time.sleep(0.1)
      self.player.seek_simple(self.time_format, gst.SEEK_FLAG_FLUSH | gst.SEEK_FLAG_SEGMENT, pos_begin)
      self.player.set_state(gst.STATE_PLAYING)

  def stop(self):
    """
    Function for stopping an audio track playback
    """
#    if self._state == "Playing" or self._state == "Paused":
    self.player.set_state(gst.STATE_NULL)
    time.sleep(0.1) #Ensure we have enough time for changing state
    self._state = "Stopped"

  def onMessage(self, bus, message):
    """
    Function for handling gstreamer messages
    bus: bus of pipeline
    message: message received from Gstreamer
    """
    t = message.type
    if t == gst.MESSAGE_EOS:
      self.player.set_state(gst.STATE_PAUSED)
      self.c.syncViewAudio()
    elif t == gst.MESSAGE_BUFFERING:
      print "buffering"
    elif t == gst.MESSAGE_SEGMENT_DONE: 
      self.player.set_state(gst.STATE_NULL)
      self.c.syncViewAudio()
    elif t == gst.MESSAGE_ERROR:
      print "error, error"
      self.player.set_state(gst.STATE_NULL)
#      self._state = "Stopped"
      err, debug = message.parse_error()
      print "Error: %s" % err, debug

  def playPause(self):
    """
    Function for toggle between play and pause
    """
    if self._state == "Playing":
      self.player.set_state(gst.STATE_PAUSED)
      self._state = "Paused"
    elif self._state == "Paused":
      self.player.set_state(gst.STATE_PLAYING)
      self._state = "Playing"

  def getCurrentNs(self):
    """
    Function to get current playing track position in nanoseconds 
    """
    pos = self.player.query_position(self.time_format, None)[0]
    return pos


  def getState(self):
    """
    Returns the player status
    """
    return self._state


  def changeVolume(self, inc):
    """
    Changes player volume
    inc: volume value positive or negative value
    """
    current_volume = self.player.get_by_name("volume").get_property("volume")
    new_volume = current_volume + inc
    if (new_volume >= 0) and (new_volume <= 10):
      self.player.get_by_name("volume").set_property('volume', new_volume)


  def getVolume(self):
    """
    Returns current volume 
    """
    return self.player.get_by_name("volume").get_property("volume")



  def mute(self):
    """
    Toggles mute 
    """
    mute = self.player.get_by_name("volume").get_property("mute")
    if mute == True:
      self.player.get_by_name("volume").set_property("mute", False)
    else:
      self.player.get_by_name("volume").set_property("mute", True)
