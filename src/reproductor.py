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

class Reproductor:
  """
  Clase para la reproducción de un libro
  """



  def setControlador(self, c):
    self.c = c

  def __init__(self):
    """
    Inicializa el reproductor para la reproducción de los archivos de audio del libro DAISY
    """
    self.estado = "Parado"
    self.activar = "Si"
    self.time_format = gst.Format(gst.FORMAT_TIME)
    self.reproductor = gst.Pipeline("player")
    fuente = gst.element_factory_make("filesrc", "file-source")
    self.reproductor.add(fuente)
    decoder = gst.element_factory_make("mad", "mp3-decoder")
    self.reproductor.add(decoder)
    conv = gst.element_factory_make("audioconvert", "converter")
    self.reproductor.add(conv)
    volume = gst.element_factory_make("volume", "volume")
    self.reproductor.add(volume)
    # speed = gst.element_factory_make("speed", "speed")
    # self.reproductor.add(speed)
    sink = gst.element_factory_make("pulsesink", "pulseaudio-output")
    self.reproductor.add(sink)
    gst.element_link_many(fuente, decoder, conv, volume, sink)
    self.reproductor.set_state(gst.STATE_NULL)
    bus = self.reproductor.get_bus()
    bus.add_signal_watch()
    bus.connect('message', self.on_message)

  def prueba(self, l):
    i = 0
    while (i < len(l)):
      if self.estado == "Parado" or self.estado == "Pausado":
        if os.path.exists(l[i][0]):
          self.reproductor.get_by_name("file-source").set_property('location', l[i][0])
          self.estado = "Reproduciendo"
          self.reproductor.set_state(gst.STATE_PAUSED)
          time.sleep(0.1)
          self.reproductor.seek(1.0, self.time_format, gst.SEEK_FLAG_FLUSH, gst.SEEK_TYPE_SET, l[i][1], gst.SEEK_TYPE_SET, l[i][2])
          time.sleep(0.1)
          self.reproductor.set_state(gst.STATE_PLAYING)
          espera = (l[i][2]-l[i][1]) / 1000000000 + 0.1
          time.sleep(espera)
          i = i + 1
          self.reproductor.set_state(gst.STATE_NULL)
      elif self.estado == "Reproduciendo":
        if os.path.exists(l[i][0]):
          self.reproductor.get_by_name("file-source").set_property('location', l[i][0])
          # self.estado = "Reproduciendo"
          self.reproductor.set_state(gst.STATE_PAUSED)
          time.sleep(0.1)
          self.reproductor.seek(1.0, self.time_format, gst.SEEK_FLAG_FLUSH, gst.SEEK_TYPE_SET, l[i][1], gst.SEEK_TYPE_SET, l[i][2])
          self.reproductor.set_state(gst.STATE_PLAYING)
          espera = (l[i][2]-l[i][1]) / 1000000000 + 0.1
          time.sleep(espera)
          i = i + 1
          self.reproductor.set_state(gst.STATE_NULL)

  def start_stop(self, l):
    i = 0
    if self.estado == "Parado":
      while ((self.reproductor.get_state() == gst.STATE_NULL) and (i <= range(len(l)))):
        print l[i][0]
        if os.path.exists(l[i][0]):
          print "aquí tb estoy"
          self.estado = "Reproduciendo"
          self.reproductor.get_by_name("file-source").set_property('location', l[0])
          self.reproductor.set_state(gst.STATE_PLAYING)
          time.sleep(0.1)
          self.reproductor.seek(1.0, self.time_format, gst.SEEK_FLAG_FLUSH, gst.SEEK_TYPE_SET, l[i:1], gst.SEEK_TYPE_SET, l[i:2])
    else:
      print "hola"
      while self.reproductor.get_state == (gst.STATE_PAUSED or gst.STATE_PLAYING) and i < len(l):
        if self.reproductor.get_message == gst.MESSAGE_EOS:
          self.reproductor.set_state(gst.STATE_NULL)
          self.estado = "Parado"
          self.reproductor.set_state(gst.STATE_PLAYING)
          time.sleep(0.1)
          self.player.seek(1.0, self.time_format, gst.SEEK_FLAG_FLUSH, gst.SEEK_TYPE_SET, l[i:1], gst.SEEK_TYPE_SET, l[i:2])
          i = i + 1


  def reproducir(self, fichero, pos_ini, pos_fin):
    """
    Método para reproducir una pista de audio.
    fichero: fichero a reproducir
    pos_ini: posición de inicio de la reproducción
    pos_fin: posición final de reproducción
    """
    if self.estado == "Parado" and self.activar == "Si":
      if os.path.exists(fichero):
        self.estado = "Reproduciendo"
        self.reproductor.get_by_name("file-source").set_property('location', fichero)
        self.reproductor.set_state(gst.STATE_PAUSED)
        time.sleep(0.0001)
        self.reproductor.seek(1.0, self.time_format, gst.SEEK_FLAG_FLUSH, gst.SEEK_TYPE_SET, pos_ini, gst.SEEK_TYPE_SET, pos_fin)
        self.reproductor.set_state(gst.STATE_PLAYING)
    elif (self.estado == "Pausado" or self.estado == "Parado") and self.activar == "No":
      if os.path.exists(fichero):
        self.estado = "Pausado"
        self.reproductor.set_state(gst.STATE_NULL)
        self.reproductor.get_by_name("file-source").set_property('location', fichero)
        self.reproductor.set_state(gst.STATE_PAUSED)
        time.sleep(0.0001)
        self.reproductor.seek(1.0, self.time_format, gst.SEEK_FLAG_FLUSH, gst.SEEK_TYPE_SET, pos_ini, gst.SEEK_TYPE_SET, pos_fin)
        self.reproductor.set_state(gst.STATE_PAUSED)



  def detener(self):
    """
    Método para detener la reproducción de una pista de audio
    """
    if self.estado == "Reproduciendo" or self.estado == "Pausado":
      self.reproductor.set_state(gst.STATE_NULL)
      self.estado = "Parado"


  def on_message(self, bus, message):
    """
    Método para detectar cuando se produce algun mensaje en gst h
    bus: bus del pipeline
    message: mensaje emitido por gst
    """
    t = message.type
    if t == gst.MESSAGE_EOS:
      self.reproductor.set_state(gst.STATE_NULL)
      self.estado = "Parado"
      self.c.sinc_vista_audio()
    elif t == gst.MESSAGE_ERROR:
      self.reproductor.set_state(gst.STATE_NULL)
      self.estado = "Parado"
      err, debug = message.parse_error()
      print "Error: %s" % err, debug

  def reproducir_pausar(self):
    """
    Método para pausar o reanudar la reproducción de un libro
    """
    if self.estado == "Reproduciendo":
      self.reproductor.set_state(gst.STATE_PAUSED)
      self.estado = "Pausado"
      self.activar = "No"
#      self.c.change_play_pause_tollbutton(gst.STATE_PAUSED)
    elif self.estado == "Pausado" or self.activar == "No":
      self.reproductor.set_state(gst.STATE_PLAYING)
      self.estado = "Reproduciendo"
      self.activar = "Si"
      self.c.change_play_pause_tollbutton(gst.STATE_PLAYING)


  def obtener_ins_actual(self):
    """
    Método para obtener la posición en nanosegundos de reproducción de la pista actual
    """
    pos = self.reproductor.query_position(self.time_format, None)[0]
    return pos


  def obtener_estado(self):
    """
    Método para obtener el estado actual de la reproducción
    """
    return self.estado


  def cambiar_volumen(self, inc):
    """
    Método para cambiar el volumen del reproductor
    inc: parámetro con  el aumento o disminución del volumen
    """
    volumen_actual = self.reproductor.get_by_name("volume").get_property("volume")
    nuevo_volumen = volumen_actual + inc
    if (nuevo_volumen >= 0) and (nuevo_volumen <= 10):
      self.reproductor.get_by_name("volume").set_property('volume', nuevo_volumen)


  def obtener_volumen(self):
    """
    Método para obtener el nivel de volumen actual
    """
    return self.reproductor.get_by_name("volume").get_property("volume")



  def silenciar(self):
    """
    Método para activar o desactivar el sonido
    """
    silencio = self.reproductor.get_by_name("volume").get_property("mute")
    if silencio == True:
      self.reproductor.get_by_name("volume").set_property("mute", False)
    else:
      self.reproductor.get_by_name("volume").set_property("mute", True)
