# -*- coding: iso-8859-15 -*-


import pygtk
pygtk.require('2.0')
import gtk
import controlador, libro, reproductor
import xml.dom.minidom as MD


from dbr_i18n import _          #For i18n support

class Vista:
  """
  Creaci�n de la clase vista para el interfaz del DBR
  """



  def ventanaNueva(self):
    """
    M�todo para crear la ventana principal del DBR
    """
    window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    window.connect("destroy", self.destruir_aplicacion)
    window.set_title("Daisy Book Reader")
    window.set_border_width(1)
    window.set_default_size(640, 480)
    return window


  def menuPrincipal(self, ventana):
    """
    M�todo para crear la barra de men� principal
    """
    accel_group = gtk.AccelGroup()
    # Inicializacion de la factoria de elementos.
    # Parametro 1: Tipo de menu.
    # Parametro 2: Ruta del menu.
    # Parametro 3: Una referencia a AccelGroup.
    item_factory = gtk.ItemFactory(gtk.MenuBar, "<main>", accel_group)

    # Generacion de los elementos de menu.
    item_factory.create_items(self.menu_items)
    # Se incluye el grupo de AccelGroup a la ventana.
    ventana.add_accel_group(accel_group)

    # Se necesita una referencia a item_factory para  prevenir su destruccion
    self.item_factory = item_factory
    # Se devuelve la barra de menu creada.
    return item_factory.get_widget("<main>")


  def __init__(self, controlador):
    """
    M�todo __init__ de la clase Vista
    """
    self.c = controlador
    self.c.setVista(self)


    self.menu_items = (
      ("/" +  _("_File"), "<alt>F", None, 0, "<Branch>"),
      ("/" + _("File") + "/" + _("_Open book"), "<control>O", self.inicio_cargaFichero_callback, 0, None),
      ("/" + _("File") + "/" + _("_Find book"), "<control>F", self.c.buscar_libro_callback, 0, None),
      ("/" + _("File") + "/" + _("_Close book"), "<control>F4", self.c.cerrar_libro_callback, 0, None),
      ("/" + _("File") + "/" + _("_Quit"), "<control>Q", self.cerrar_aplicacion, 0, None),

      ("/" + _("_Control"), "<alt>C", None, 0, "<Branch>"),
      ("/" + _("Control") + "/" + _("_Play-Pause"), "<control>space", self.c.control_estado_callback, 0, None),
      ("/" + _("Control") + "/" + _("_Mute"), "<control>M", self.c.activar_desactivar_sonido_callback, 0, None),
      ("/" + _("Control") + "/" + _("_Stop"), "<control>S", self.c.detener_callback, 0, None),
      ("/" + _("Control") + "/" + _("_Volume"), "<alt>V", None, 0, "<Branch>"),
      ("/" + _("Control") + "/" + _("Volume") + "/" + _("Increase volume"), "<control>V", self.c.control_aumento_volumen_callback, 0, None),
      ("/" + _("Control") + "/" + _("Volume") + "/" + _("Decrease volume"), "<control><shift>V", self.c.control_disminucion_volumen_callback, 0, None),

      ("/" + _("_Navigation"), "<alt>N", None, 0, "<Branch>"),
      ("/" + _("Navigation") + "/" + _("Previous chapter"), "<control><shift>L", self.c.ir_cap_ant_callback, 0, None),
      ("/" + _("Navigation") + "/" + _("Next chapter"), "<control>L", self.c.ir_cap_sig_callback, 0, None),
      ("/" + _("Navigation") + "/" + _("Previous page"), "<control><shift>N", self.c.ir_pag_ant_callback, 0, None),
      ("/" + _("Navigation") + "/" + _("Next page"), "<control>N", self.c.ir_pag_sig_callback, 0, None),
      ("/" + _("Navigation") + "/" + _("Previous paragraph"), "<control><shift>P", self.c.ir_texto_ant_callback, 0, None),
      ("/" + _("Navigation") + "/" + _("Next paragraph"), "<control>P", self.c.ir_texto_sig_callback, 0, None),
      ("/" + _("_Go to"), "<control>G", None, 0, "<Branch>"),
      ("/" + _("_Go to") + "/" + _("Chapter"), None, self.c.listar_capitulos_callback, 0, None),
      ("/" + _("_Go to") + "/" + _("Page"), None, self.c.ir_a_pagina_callback, 0, None),
      ("/" + _("_Bookmarks"), "<alt>B", None, 0, "<Branch>"),
      ("/" + _("Bookmarks") + "/" + _("_Set bookmark"), "<control>K", self.c.establecer_marca_callback, 0, None),
      ("/" + _("Bookmarks") + "/" + _("_Delete bookmarks"), "<control>D", self.c.borrado_de_marcas_callback, 0, None),
      ("/" + _("Bookmarks") + "/" + _("_List bookmarks"), "<control>B", self.c.listar_marcas_callback, 0, None),
      ("/" + _("_Info"), "<alt>I", None, 0, "<Branch>"),
      ("/" + _("Info") + "/" + _("_Book info"), "<control>O", self.c.mostrar_inf_libro_callback, 0, None),
      ("/" + _("Info") + "/" + _("Book _translation information"), "<control>N", self.c.mostrar_inf_traduccion_callback, 0, None),
      ("/" + _("Info") + "/" + _("Playback _duration"), "<control>X", self.c.mostrar_pos_actual_callback, 0, None),
      ("/" + _("Info") + "/" + _("Total play _duration"), "<control>W", self.c.mostrar_tiempo_total_callback, 0, None),
      ("/" + _("_Help"), "<alt>H", None, 0, "<Branch>"),
      ("/" + _("Help") + "/" + _("_User help"), "<control>u", self.c.mostrar_ayuda_callback, 0, None),
      ("/" + _("Help") + "/" + _("_About DBR"), "<control>Y", self.c.display_about_dialog_callback, 0, None),
      ("/" + _("Help") + "/" + _("_License"), "<control>J", self.c.mostrar_licencia_callback, 0, None)
      )

    self.ventana = self.ventanaNueva()


    caja_principal = gtk.VBox(False, 1)
    caja_principal.set_border_width(1)
    caja_principal.show()

    barraMenu = self.menuPrincipal(self.ventana)

    caja_principal.pack_start(barraMenu, False, True, 0)
    barraMenu.show()


    #crear un toolbar
    self.toolbar = gtk.Toolbar()
    self.toolbar.set_orientation(gtk.ORIENTATION_HORIZONTAL)
    self.toolbar.set_style(gtk.TOOLBAR_BOTH)
    self.toolbar.set_border_width(5)
    
    # Opciones del toolbar: abrir...
    toolbar_item = gtk.ToolButton(_("Open"))
    toolbar_item.set_stock_id(gtk.STOCK_OPEN)
    toolbar_item.connect("clicked", self.inicio_cargaFichero_callback, toolbar_item)
    toolbar_item.show()
    self.toolbar.insert(toolbar_item, -1)

    self.toolbar_item2 = gtk.ToggleToolButton(gtk.STOCK_MEDIA_PLAY)
    #self.toolbar_item2.set_stock_id(gtk.STOCK_MEDIA_PAUSE)
    self.toolbar_item2.set_active(False)

    self.toolbar_item2.connect("clicked", self.c.control_estado_callback, self.toolbar_item2)
    self.toolbar_item2.show()
    self.toolbar.insert(self.toolbar_item2, -1)
    
    toolbar_item3 = gtk.ToolButton(_("Stop"))
    toolbar_item3.set_stock_id(gtk.STOCK_MEDIA_STOP)
    toolbar_item3.connect("clicked", self.c.detener_callback, toolbar_item3)
    toolbar_item3.show()
    self.toolbar.insert(toolbar_item3, -1)

    
    toolbar_item6 = gtk.ToolButton(_("Next Chapter"))
    toolbar_item6.set_stock_id(gtk.STOCK_MEDIA_REWIND)
    toolbar_item6.connect("clicked", self.c.ir_cap_ant_callback, toolbar_item6)
    toolbar_item6.show()
    self.toolbar.insert(toolbar_item6, -1)
    
    toolbar_item4 = gtk.ToolButton(_("Previous Chapter"))
    toolbar_item4.set_stock_id(gtk.STOCK_MEDIA_FORWARD)
    toolbar_item4.connect("clicked", self.c.ir_cap_sig_callback, toolbar_item4)
    toolbar_item4.show()
    self.toolbar.insert(toolbar_item4, -1)

    iconw = gtk.Image() # icon widget
    iconw.set_from_file("/usr/share/icons/gnome/32x32/actions/bookmarks.png")

    toolbar_item5 = gtk.ToolButton(iconw,_("Set Bookmark"))
    #toolbar_item5.set_stock_id(gtk.STOCK_INDEX)
    toolbar_item5.connect("clicked", self.c.establecer_marca_callback, toolbar_item5)
    toolbar_item5.show()
    self.toolbar.insert(toolbar_item5, -1)

    caja_principal.pack_start(self.toolbar, False, True, 0)
    self.toolbar.show()


    # Crear un TreeStore con una columna de texto.
    self.treestore = gtk.TreeStore(str)

    # Creaci�n del TreeView usando treestore
    self.treeview = gtk.TreeView(self.treestore)

    # Creaci�n del TreeViewColumn para mostrar los datos
    self.tvcolumn = gtk.TreeViewColumn(_("Table of contents"))

    # Agregar la columna  al treeview
    self.treeview.append_column(self.tvcolumn)

    # crear un CellRendererText  para mostrar los datos
    self.cell = gtk.CellRendererText()

    # Agregar la celda a la vcolumn y permitirle expandirse
    self.tvcolumn.pack_start(self.cell, True)

    # Incluir el atributo "text" de la celda a la columna 0 - devolver el texto
    # desde la columna  en el �rbol.
    self.tvcolumn.add_attribute(self.cell, 'text', 0)


    # Hacerlo buscable
    self.treeview.set_search_column(0)
    self.treeselection = self.treeview.get_selection()

    self.cursor_cambiado = self.treeview.connect("cursor-changed", self.actualizar_audio)


    ventana_libro = gtk.ScrolledWindow()
    ventana_libro.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    ventana_libro.show()
    ventana_libro.add_with_viewport(self.treeview)


    self.treeview.show_all()

    caja_general = gtk.VBox(False, 1)
    caja_general.set_border_width(1)
    self.ventana.add(caja_general)
    caja_general.show()
    caja_general.pack_start(caja_principal, False, True, 0)
    caja_general.pack_start(ventana_libro, True, True, 0)



    self.ventana.show_all()
    lista, posicion_indice = self.c.obtener_configuracion()
    if len(lista) > 0:
      self.mostrar_libro(lista)
      self.actualizar_vista(posicion_indice)
      self.c.carga_fichero_inicial()
    
    self.treeview.grab_focus()

  def view_play_icon(self):
    """
    Cambia el icono del boton del toolbar a play
    """
    self.toolbar_item2.set_active(False)
    #self.toolbar_item2.show()

  def view_pause_icon(self):
    """
    Cambia el icono del boton del toolbar a pause
    """
    self.toolbar_item2.set_active(True)
    #self.toolbar_item2.show()
    
  def inicio_cargaFichero_callback(self, w, data):
    """
    M�todo para mostrar el libro en la pantalla cuando es abierto desde el men�
    """
    lista = self.c.cargaFichero(w)
    self.mostrar_libro(lista)
    self.c.sinc_vista_audio()


  def mostrar_libro(self, lista):
    """
    M�todo para mostrar un libro por pantalla cuando se carga el DBR
    """
    self.limpiar_modelo()
    l = []
    for x in range(len(lista)):
      y = lista[x].childNodes
      z = y[0].firstChild.toprettyxml()
      l.append(y[0])
      iter = self.treestore.append(None, ['%s' % z])
    titulo = self.c.obtener_titulo()
    self.ventana.set_title("Daisy Book Reader - " + titulo)


  def limpiar_modelo(self):
    """
    M�todo para eliminar las filas del treemodel
    """
    self.treestore.clear()
    self.ventana.set_title("Daisy Book Reader")



  def actualizar_vista(self, n):
    """
    M�todo para actualizar la vista del cursor del treeview
    """
    t = (n)
    self.treeview.handler_block(self.cursor_cambiado)
    self.treeview.set_cursor_on_cell(t, self.tvcolumn, self.cell)
    self.treeview.handler_unblock(self.cursor_cambiado)


  def actualizar_audio(self, data):
    """
    M�todo para actualizar el audio cuando el  usuario mueve el cursor
    """
    pos_cursor = self.treeview.get_cursor()
    aux = list(pos_cursor)
    lista = list(aux[0])
    self.c.sinc_audio_vista(lista[0])


  def cerrar_aplicacion(self, w, data):
    """
    M�todo para cerrar la aplicaci�n desde el men�
    """
    self.c.cerrar_aplicacion()
    gtk.main_quit()


  def destruir_aplicacion(self, widget):
    """
    M�todo para cerrar la aplicaci�n cuando se emite la se�al destroy
    """
    self.c.cerrar_aplicacion()
    gtk.main_quit()
