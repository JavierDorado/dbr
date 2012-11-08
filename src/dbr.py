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

import sys
sys.argv[0]="dbr"
import pygtk
pygtk.require('2.0')
import gtk
import vista, controlador, reproductor, registro

from dbr_i18n import _          #for i18n support

def main():
  """
  Método principal de la aplicación
  """
  r = reproductor.Reproductor()
  reg = registro.Registro()
  c = controlador.Controlador(r, reg)
  v = vista.Vista(c)
  r.setControlador(c)

  gtk.main()
  return 0

main()


if __name__ == "__main__":
      pass
