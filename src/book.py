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

class Libro:
  """
  Clase para manipular un libro
  """



  def __init__(self, fichero, pos_indice=0, pos_nodos_libro=0, pos_audio=0):
    """
    Inicia un objeto libro que permite acceder a todos los datos de los archivos DAISY
    """
    self.indice = []
    self.nodos_libro = []
    self.pos_sig_indice = self.pos_indice = pos_indice
    self.pos_sig_nodos_libro = self.pos_nodos_libro = pos_nodos_libro
    self.pos_audio = pos_audio
    self.tree = MD.parse(fichero)
    self.nombre_libro = self.obtener_nombre()
    self.ruta_libro = fichero
    self.obtener_arbol()
    self.obtener_pistas(self.nodos_libro[self.pos_nodos_libro])

  def obtener_nombre(self):
    """
    Método para obtener el nombre del libro
    """
    nombre = ''
    meta = self.tree.getElementsByTagName('meta')
    encontrado = 0
    i = 0
    while encontrado == 0 and i < len(meta):
      if meta[i].hasAttribute('name'):
        if meta[i].attributes['name'].value == 'dc:title':
          nombre = meta[i].attributes['content'].value
          encontrado = 1
      i = i+1
    return nombre


  def obtener_numero_paginas(self):
    """
    Método para obtener el número de páginas de un libro
    """
    meta = self.tree.getElementsByTagName('meta')
    encontrado = 0
    i = 0
    while (encontrado == 0) and (i < len(meta)):
      if meta[i].hasAttribute('name'):
        if (meta[i].attributes['name'].value == 'ncc:pageNormal') or (meta[i].attributes['name'].value == 'ncc:page-normal'):
          paginas_totales_libro = meta[i].attributes['content'].value
          encontrado = 1
      i = i+1
    return paginas_totales_libro


  def obtener_datos_para_marca(self):
    """
    Método para obtener la posición del índice, de los nodos del libro, del audio, así como el nombre y la ruta del libro
    """
    informacion = []
    informacion.append(self.nombre_libro)
    informacion.append(self.ruta_libro)
    informacion.append(self.pos_indice)
    informacion.append(self.pos_nodos_libro)
    informacion.append(self.pos_audio-1)
    return informacion


  def obtener_indice(self):
    """
    Método para obtener el índice del libro
    """
    return self.indice


  def obtener_pos_indice(self):
    """
    Método para obtener la posición del índice
    """
    return self.pos_indice


  def obtener_nodo_actual(self):
    """
    Método para obtener el nodo actual en reproducción
    """
    return self.nodos_libro[self.pos_nodos_libro]


  def obtener_subarbol(self, listaNodos, lista, listado):
    """
    Método para obtener un subarbol del libro
    """
    for x in listaNodos:
      if len(x.childNodes) > 1:
        lista, listado = self.obtener_subarbol(x.childNodes, lista, listado)
      elif len(x.childNodes) == 1:
        listado.append(x)
        if x.hasAttribute('class'):
          at = x.attributes['class']
          if ((at.value == 'title') or (at.value == 'chapter') or (at.value == 'section') or (at.value == 'sub-section') or(at.value == 'jacket') or (at.value == 'front') or (at.value == 'title-page') or (at.value == 'copyright-page') or (at.value == 'acknowledgement') or (at.value == 'prolog') or (at.value == 'introduction') or (at.value == 'dedication') or (at.value == 'foreword') or (at.value == 'preface') or (at.value == 'print-toc') or (at.value == 'part') or (at.value == 'minor-head') or (at.value == 'bibliography') or (at.value == 'glosary') or (at.value == 'appendix') or (at.value == 'index') or (at.value == 'index-category')):
            lista.append(x)
        elif not x.hasAttribute('class'):
          lista.append(x)
    return lista, listado


  def obtener_arbol(self):
    """
    Método de control  para obtener el árbol del libro
    """
    lista = []
    listado = []
    nodos = self.tree.getElementsByTagName('body')
    tamanyo = len(nodos)
    # Si existe el arbol, se muestra
    if tamanyo >= 1:
      lista, listado = self.obtener_subarbol(nodos, lista, listado)
      self.indice = lista
      self.nodos_libro = listado


  def obtener_capitulos(self):
    """
    Método para obtener los capítulos del libro y su posición en la lista de nodos
    """
    i = 0
    capitulos = []
    pos_capitulos = []
    while (i < len(self.indice)):
      if self.indice[i].hasAttribute('class'):
        valor_clase = self.indice[i].attributes['class'].value
        if valor_clase == 'chapter':
          nombre_capitulo = self.indice[i].childNodes[0].firstChild.toprettyxml()
          capitulos.append(nombre_capitulo)
          pos_capitulos.append(i)
      i = i + 1
    return capitulos, pos_capitulos


  def obtener_capitulo(self, pos):
    """
    Método para obtener un capítulo concreto y su posición en el índice y en los nodos del libro
    pos: indica si es el capítulo anterior o siguiente
    """
    encontrado = 0
    cambio = 0
    nueva_pos_indice = self.pos_indice
    while (encontrado == 0) and (nueva_pos_indice > 0) and (nueva_pos_indice < len(self.indice)):
      nueva_pos_indice = nueva_pos_indice + pos
      if nueva_pos_indice < len(self.indice):
        if self.indice[nueva_pos_indice].hasAttribute('class'):
          clase = self.indice[nueva_pos_indice].attributes['class'].value
          if clase == 'chapter':
            encontrado = 1
            cambio = 1
        elif not self.indice[nueva_pos_indice].hasAttribute('class'):
          encontrado = 1
          cambio = 1
    if encontrado == 1:
      id_indice = self.indice[nueva_pos_indice].attributes['id'].value
      encontrado = 0
      i = 0
      while (encontrado == 0) and (i < len(self.nodos_libro)):
        id_nod_libro = self.nodos_libro[i].attributes['id'].value
        if id_indice == id_nod_libro:
          encontrado = 1
          self.pos_sig_indice = self.pos_indice = nueva_pos_indice
          self.pos_sig_nodos_libro = self.pos_nodos_libro = i
        self.pos_audio = 0
        i = i + 1
    return cambio

  def cambiar_pagina(self, pos):
    """
    Método para cambiar a la página anterior o siguiente
    pos: Indica si es la página siguiente o anterior
    """
    encontrado = 0
    cambio = 0
    nueva_pos_nodos_libro = self.pos_nodos_libro
    while (encontrado == 0) and (nueva_pos_nodos_libro > 0) and (nueva_pos_nodos_libro < len(self.nodos_libro)):
      nueva_pos_nodos_libro = nueva_pos_nodos_libro + pos
      if nueva_pos_nodos_libro < len(self.nodos_libro):
        if self.nodos_libro[nueva_pos_nodos_libro].hasAttribute('class'):
          clase = self.nodos_libro[nueva_pos_nodos_libro].attributes['class'].value
          if clase == 'page-normal':
            encontrado = 1
            cambio = 1
    if encontrado == 1:
      self.actualizar_posicion_indice(nueva_pos_nodos_libro)
    return cambio


  def actualizar_posicion_indice(self, nueva_pos_nodos_libro):
    """
    Método para actualizar la posición del índice con respecto a la posición en la lista  de los nodos del libro
    nueva_pos_nodos_libro: nueva posición en la lista de nodos
    """
    encontrado = 0
    i = nueva_pos_nodos_libro
    while (encontrado == 0) and (i > 0):
      i = i - 1
      if self.nodos_libro[i].hasAttribute('class'):
        clase = self.nodos_libro[i].attributes['class'].value
        if (clase == 'title') or (clase == 'jacket') or (clase == 'front') or (clase == 'title-page') or (clase == 'copyright-page') or (clase == 'acknowledgement') or (clase == 'prolog') or (clase == 'introduction') or (clase == 'dedication') or (clase == 'foreword') or (clase == 'preface') or (clase == 'print-toc') or (clase == 'part') or (clase == 'chapter') or (clase == 'section') or (clase == 'sub-section') or (clase == 'minor-head') or (clase == 'bibliography') or (clase == 'glossary') or (clase == 'appendix') or (clase == 'index') or (clase == 'index-category'):
          id_nodos_libro = self.nodos_libro[i].attributes['id'].value
          encontrado = 1
          terminado = 0
          j = len(self.indice)-1
          while (terminado == 0) and (j >= 0):
            id_indice = self.indice[j].attributes['id'].value
            if id_indice == id_nodos_libro:
              self.pos_sig_indice = self.pos_indice = j
              self.pos_sig_nodos_libro = self.pos_nodos_libro = nueva_pos_nodos_libro
              self.pos_audio = 0
              terminado = 1
            if j > 0:
              j = j - 1
      elif not self.nodos_libro[i].hasAttribute('class'):
        id_nodos_libro = self.nodos_libro[i].attributes['id'].value
        encontrado = 1
        terminado = 0
        j = len(self.indice)-1
        while (terminado == 0) and (j >= 0):
          id_indice = self.indice[j].attributes['id'].value
          if id_indice == id_nodos_libro:
            self.pos_sig_indice = self.pos_indice = j
            self.pos_sig_nodos_libro = self.pos_nodos_libro = nueva_pos_nodos_libro
            self.pos_audio = 0
            terminado = 1
          if j > 0:
            j = j - 1


  def actualizar_pos_nodos_libro(self, nueva_pos_indice):
    """
    Método para actualizar la posición en la lista de los nodos del libro con respecto al índice
    nueva_pos_indice: nueva posición en el índice
    """
    encontrado = 0
    i = 0
    id_indice = self.indice[nueva_pos_indice].attributes['id'].value
    while (encontrado == 0) and (i < (len(self.nodos_libro)-1)):
      id_nodos_libro = self.nodos_libro[i].attributes['id'].value
      if id_indice == id_nodos_libro:
        self.pos_sig_indice = self.pos_indice = nueva_pos_indice
        self.pos_sig_nodos_libro = self.pos_nodos_libro = i
        self.pos_audio = 0
        self.obtener_pistas(self.nodos_libro[self.pos_nodos_libro])
        encontrado = 1
      i = i + 1

  def establecer_pos_lectura(self, indice_pos, nodos_libro_pos, audio_pos):
    """
    Método para establecer la posición de lectura en un punto concreto del libro
    """
    self.pos_indice = self.pos_sig_indice = indice_pos
    self.pos_nodos_libro = self.pos_sig_nodos_libro = nodos_libro_pos
    self.pos_audio = audio_pos
    self.obtener_pistas(self.nodos_libro[self.pos_nodos_libro])


  def buscar_pagina(self, pagina):
    """
    Método para localizar una página concreta
    """
    pagina = int(pagina)
    paginas_totales = self.obtener_numero_paginas()
    paginas_totales = int(paginas_totales)
    i = 0
    encontrado = 0
    cambio = 0 
    if (pagina >= 0) and (pagina <= paginas_totales):
      while (i < len(self.nodos_libro)) and (encontrado == 0):
        if self.nodos_libro[i].hasAttribute('class'):
          clase = self.nodos_libro[i].attributes['class'].value
          if clase == "page-normal":
            numero = self.nodos_libro[i].childNodes[0].firstChild
            if pagina == int(numero.toprettyxml()):
              encontrado = 1
              cambio = 1
              self.actualizar_posicion_indice(i)
        i = i + 1
    return cambio, i


  def obtener_texto(self, pos):
    """
    Método para obtener un bloque de texto siguiente o anterior a la posición en la lista de nodos del libro
    pos: indica si hay que buscar el texto hacia adelante o hacia atrás respecto a la posición en la lista de nodos del libro
    """
    encontrado = 0
    cambio = 0
    nueva_pos_nodos_libro = self.pos_nodos_libro
    while (encontrado == 0) and (nueva_pos_nodos_libro > 0) and (nueva_pos_nodos_libro < len(self.nodos_libro)):
      nueva_pos_nodos_libro = nueva_pos_nodos_libro + pos
      if nueva_pos_nodos_libro < len(self.nodos_libro):
        if self.nodos_libro[nueva_pos_nodos_libro].hasAttribute('class'):
          clase = self.nodos_libro[nueva_pos_nodos_libro].attributes['class'].value
          if clase == 'group':
            encontrado = 1
            cambio = 1
    if encontrado == 1:
      self.actualizar_posicion_indice(nueva_pos_nodos_libro)
    return cambio



  def obtener_pista(self):
    """
    Método para extraer una pista de audio, su posición de inicio y de fin, y actualizar las posiciones del índice, de los nodos del libro y el audio
    """
    if self.pos_sig_nodos_libro == (self.pos_nodos_libro + 1):
      self.pos_nodos_libro = self.pos_sig_nodos_libro
    if self.pos_sig_indice == (self.pos_indice + 1):
      self.pos_indice = self.pos_sig_indice
    if self.pos_audio == -1:
      self.pos_audio = 0
    fichero = self.m[self.pos_audio][0]
    pos_ini = self.m[self.pos_audio][1]
    pos_fin = self.m[self.pos_audio][2]
    if (self.pos_audio < (len(self.m)-1)) and (self.pos_audio >= 0):
      self.pos_audio = self.pos_audio + 1
    else:
      if self.pos_nodos_libro < (len(self.nodos_libro)-1):
        ind_id = self.indice[self.pos_indice].attributes['id'].value
        nod_id = self.nodos_libro[self.pos_nodos_libro].attributes['id'].value
        ind_sig_id = self.indice[self.pos_indice+1].attributes['id'].value
        nod_sig_id = self.nodos_libro[self.pos_nodos_libro+1].attributes['id'].value
        if (ind_id == nod_id) or (ind_sig_id == nod_sig_id):
          self.pos_sig_indice = self.pos_sig_indice + 1
        self.pos_sig_nodos_libro = self.pos_sig_nodos_libro + 1
        self.pos_audio = 0
        self.obtener_pistas(self.nodos_libro[self.pos_sig_nodos_libro])
      else:
        self.pos_sig_indice = self.pos_indice = 0
        self.pos_sig_nodos_libro = self.pos_nodos_libro = 0
        self.pos_audio = 0
    return fichero, pos_ini, pos_fin


  def obtener_pistas(self, nodo):
    """
    Método para obtener las pistas de audio de un nodo
    nodo: nodo del que se quiere extraer las pistas de audio
    """
    m = []
    self.ruta = self.ruta_libro.split("ncc.html")
    a = nodo.getElementsByTagName('a')
    valor = a[0].attributes['href']
    fichero = valor.value.split("#")
    print "SMIL file: " + fichero[0] #dbg
    ruta_completa = self.ruta[0] + fichero[0]
    print "Full path to the file is: " + ruta_completa #dbg
    smil = MD.parse(ruta_completa) #Parse the smil file
    seq = smil.getElementsByTagName('seq')
    par = seq[0].getElementsByTagName('par')
    if len(par) > 0:
      for i in range(len(par)):
        text = par[i].getElementsByTagName('text')
        at = text[0].attributes['id'].value
#        if at == fichero[1]: 
        audio = par[i].getElementsByTagName('audio')
        for j in range(len(audio)):
          if audio[j].hasAttribute('clip-begin'):
            ruta_audio = self.ruta[0] + audio[j].attributes['src'].value
            l = []
            l.append(ruta_audio)
            inicio = self.obtener_tiempo(audio[j].attributes['clip-begin'].value)
            l.append(inicio)
            fin = self.obtener_tiempo(audio[j].attributes['clip-end'].value)
            l.append(fin)
            print "Audio track " + str(j)+ "\n" + "Audio file is: " + str(l[0]) + "Begins at " + str(l[1]) + " and ends at " + str(l[2]) #dbg
            m.append(l)
    else:
      audio = seq[0].getElementsByTagName('audio')
      for j in range(len(audio)):
        if audio[j].hasAttribute('clip-begin'):
          ruta_audio = self.ruta[0] + audio[j].attributes['src'].value
          l = []
          l.append(ruta_audio)
          inicio = self.obtener_tiempo(audio[j].attributes['clip-begin'].value)
          l.append(inicio)
          fin = self.obtener_tiempo(audio[j].attributes['clip-end'].value)
          l.append(fin)
          m.append(l)
          print "Audio track " + str(j) + "\n" + "Audio file is: " + str(l[0]) + "Begins at " + str(l[1]) + " and ends at " + str(l[2]) #dbg

    self.m = m


  def obtener_tiempo(self, audio):
    """
    Método para convertir a nanosegundos el tiempo pasado en una cadena de texto
    audio: cadena de texto que contiene el valor del audio
    """
    aux = audio.split("=")
    tiempo = aux[1].split("s")
    aux = float(tiempo[0]) * 1000000000
    ns = int(aux)
    return ns


  def obtener_inf_libro(self):
    """
    Método para obtener información general del libro
    """
    l = []
    informacion = ''
    separador = ''
    v = ['ncc:sourceTitle', 'dc:title', 'dc:creator', 'ncc:sourceEdition', 'ncc:sourceDate', 'ncc:sourcePublisher', 'ncc:sourceRights']
    datos = self.tree.getElementsByTagName('meta')
    for i in range(len(v)):
      for x in datos:
        if x.hasAttribute('name'):
          at = x.attributes['name']
          if at.value == v[i]:
            l.append(x.attributes['content'].value)
            l.append("\n")
    informacion = separador.join(l)
    return informacion


  def obtener_inf_traduccion(self):
    """
    Método para obtener información de la traducción del libro
    """
    l = []
    informacion = ''
    separador = ''
    v = ['ncc:sourceTitle', 'dc:title', 'dc:publisher', 'dc:identifier', 'ncc:producer', 'ncc:narrator', 'dc:date', 'dc:format', 'ncc:totalTime', 'ncc:totaltime']
    datos = self.tree.getElementsByTagName('meta')
    for i in range(len(v)):
      for x in datos:
        if x.hasAttribute('name'):
          at = x.attributes['name']
          if at.value == v[i]:
            l.append(x.attributes['content'].value)
            l.append("\n")
    informacion = separador.join(l)
    return informacion


  def obtener_pos_actual_audio(self):
    """
    Método para obtener la posición actual de reproducción del libro en segundos
    """
    audio_pos = self.pos_audio
    nodo = self.pos_nodos_libro
    duracion = 0
    i = 0
    while i <= nodo:
      href = self.nodos_libro[i].firstChild.attributes['href'].value
      smil = href.split("#")
      ruta_completa = self.ruta[0] + smil[0]
      fichero = MD.parse(ruta_completa)
      if i < nodo:
        seq = fichero.getElementsByTagName('seq')
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
                inicio = self.obtener_tiempo(audio[k].attributes['clip-begin'].value)
                fin = self.obtener_tiempo(audio[k].attributes['clip-end'].value)
                aux = fin - inicio
                duracion = duracion + aux
              k = k + 1
          j = j + 1 
      elif i == nodo:
        seq = fichero.getElementsByTagName('seq')
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
                inicio = self.obtener_tiempo(audio[k].attributes['clip-begin'].value)
                fin = self.obtener_tiempo(audio[k].attributes['clip-end'].value)
                aux = fin - inicio
                duracion = duracion + aux
              k = k + 1
            aux = audio[k].attributes['clip-begin'].value
            begin = self.obtener_tiempo(aux)
            aux = begin / 1000000000
            aux = int(aux)
          j = j + 1
      i = i + 1
    segundos = duracion / 1000000000
    return segundos, aux


  def obtener_tiempo_total_audio(self):
    """
    Método para obtener el tiempo total de grabación del libro
    """
    i = 0
    encontrado = 0
    meta = self.tree.getElementsByTagName('meta')
    while (i < len(meta)) and (encontrado == 0):
      if meta[i].hasAttribute('name'):
        if (meta[i].attributes['name'].value == 'ncc:totalTime') or (meta[i].attributes['name'].value == 'ncc:totaltime'):
          tiempo_total = meta[i].attributes['content'].value
          encontrado = 1
      i = i + 1
    aux = tiempo_total.split(":")
    tiempo_total = int(aux[0]) * 3600
    tiempo_total = tiempo_total + int(aux[1]) * 60
    tiempo_total = tiempo_total + int(aux[2])
    return float(tiempo_total)


  def establecer_formato_hora(self, time_int):
    """
    Método para conventir los segundos al formato de horas "hh:mm:ss"
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
