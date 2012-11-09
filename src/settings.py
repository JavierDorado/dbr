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

class Registro:
  """
  Clase para la gestión del guardado, manipulación y guardado de la configuración y las marcas de los libros
  """

  def __init__(self):
    """
    Método que obtiene la configuración del DBR
    """
    home = os.path.expanduser('~')
    self.fichero_configuracion = home + "/" + ".dbr"
    if os.path.exists(self.fichero_configuracion):
      f = open(self.fichero_configuracion, "r")
      self.registro = pickle.load(f)
      f.close()
    else:
      self.crear_fichero_configuracion()


  def escribir_configuracion(self, informacion):
    """
    Método para escribir en la configuración  los datos de configuración y la última posición de lectura del libro último en reproducción
    informacion: datos de la configuración y el último libro reproducido
    """
    self.registro[0] = informacion
    f = open(self.fichero_configuracion, "w")
    pickle.dump(self.registro, f)
    f.close()


  def obtener_configuracion(self):
    """
    Método para obtener la configuración del DBR y el último libroleído y su posición de lectura
    """
    return self.registro[0]


  def crear_fichero_configuracion(self):
    """
    Método para crear el fichero de configuración del DBR si no existe
    """
    self.registro = [0]
    configuracion = [None, None, [0, 0, 0], 1]
    self.registro[0] = configuracion
    f = open(self.fichero_configuracion, "w")
    pickle.dump(self.registro, f)
    f.close()


  def crear_marca(self, marca):
    """
    Método para crear o actualizar una marca de un libro y almacenarla en el fichero de configuración
    marca: datos necesarios para crear la marca
    """
    aux = [0]
    # Comprobamos si hay algun libro almacenado
    if len(self.registro) > 1:
      # Comprobamos si el libro al que vamos a poner la marca está almacenado ya
      i = 0
      encontrado = 0
      while (i < (len(self.registro)-1)) and encontrado == 0:
        i = i + 1
        if self.registro[i][0] == marca[0]:
          encontrado = 1
      if encontrado == 1:
        # El libro está almacenado
        # Comprobamos si el libro tiene una marca con el nombre de la nueva marca
        j = 1
        terminado = 0
        while (j < (len(self.registro[i])-1)) and (terminado == 0):
          j = j + 1
          if self.registro[i][j][0] == marca[5]:
            terminado = 1
        if terminado == 1:
          # Hay una marca con ese nombre
          self.registro[i][j][1:4] = marca[2:5]
        else:
          # No hay una marca con ese nombre
          aux[0] = marca[5]
          aux = aux + marca[2:5]
          self.registro[i].append(aux)
      else:
        # No hay ningun libro almacenado con ese nombre
        self.registro.append(marca[0:2])
        aux[0] = marca[5]
        aux = aux + marca[2:5]
        self.registro[i+1].append(aux)
    else:
      # No hay ningun libro almacenado
      self.registro.append(marca[0:2])
      aux[0] = marca[5]
      aux = aux + marca[2:5]
      pos = len(self.registro) - 1
      self.registro[pos].append(aux)
    print self.registro
    f = open(self.fichero_configuracion, "w")
    pickle.dump(self.registro, f)
    f.close()


  def obtener_marcas_libro_actual(self, nombre_libro):
    """
    Método para obtener las marcas del libro actualmente en reproducción
    """
    # Comprobamos si hay algun libro con marcas
    if len(self.registro) > 1:
      i = 0
      encontrado = 0
      while (i < (len(self.registro)-1)) and encontrado == 0:
        i = i + 1
        if self.registro[i][0] == nombre_libro:
          encontrado = 1
      if encontrado == 1:
        # Obtenemos las marcas disponibles
        marcas = []
        j = 2
        while (j < len(self.registro[i])):
          marcas.append(self.registro[i][j])
          j = j + 1
      else:
        marcas = []
    else:
      marcas = []
    return marcas


  def borrar_marca(self, nombre_libro, pos_marca):
    """
    Método para borrar una marca en el libro actualmente en reproducción
    """
    i = 0
    encontrado = 0
    while (i < len(self.registro)) and (encontrado == 0):
      i = i + 1
      if nombre_libro == self.registro[i][0]:
        encontrado = 1
    if len(self.registro[i]) == 3:
      self.registro.pop(i)
    else:
      self.registro[i].pop(pos_marca+2)
    f = open(self.fichero_configuracion, "w")
    pickle.dump(self.registro, f)
    f.close()


  def buscar_libros(self):
    """
    Método que busca los libros almacenados en el fichero de configuración
    """
    if len(self.registro) > 1:
      libros = []
      i = 0
      while (i < (len(self.registro)-1)):
        i = i + 1
        if os.path.exists(self.registro[i][1]):
          libros.append(self.registro[i][0:2])
    return libros
