#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
import wx.html as html
from database import BaseDeDatos
from dialogoNuevaPalabra import DialogoNuevaPalabra
from listviewVirtual import ListViewVirtual
from menuContextual import MenuContextual

class FramePrincipal(wx.Frame):
    """Ventana principal del programa """
    # ATRIBUTOS
    deutschDB = BaseDeDatos("deutsch.db")
    criterio = "No"
    orden = "ASC"

    # MAIN
    def __init__(self, parent, id, title):
        """Incicializador de framePrincipal"""
        wx.Frame.__init__(self, parent, id, title,size=(1024,768))

        # Creo los dos paneles, un sizer y un separador
        self.separador = wx.SplitterWindow(self, -1)
        self.panel = wx.Panel(self.separador,-1,style=wx.BORDER_SUNKEN)
        self.panel2 = wx.Panel(self.separador,-1)
        vboxNavegadorWeb = wx.BoxSizer(wx.VERTICAL)
        hboxBuscarWeb = wx.BoxSizer(wx.HORIZONTAL)
        
        # Barra de Herramientas
        barra_herramientas = self.CreateToolBar()
        barra_herramientas.AddLabelTool(1, '', wx.Bitmap('./icons/nuevaPalabra.png'), shortHelp="Introduce una nueva palabra")
        barra_herramientas.AddLabelTool(2, '', wx.Bitmap('./icons/borrarDB.png'), shortHelp="Borra la base de datos")
        barra_herramientas.AddCheckLabelTool(3, '', wx.Bitmap('./icons/mostrarNavegador.png'), shortHelp="Muestra/Oculta el navegador")
        barra_herramientas.AddSeparator()
        barra_herramientas.AddLabelTool(4, '', wx.Bitmap('./icons/salir.png'), shortHelp="Salir")
        barra_herramientas.Realize()

        # Barra de Busqueda del Navegador Web.
        buscadorWeb = wx.Panel(self.panel2, -1, size=(-1, 20))
        buscadorWeb.SetBackgroundColour('#6f6a59')
        buscadorWeb.SetForegroundColour('WHITE')
        stBuscarWeb = wx.StaticText(buscadorWeb, -1, 'Buscar en WordReference', (5, 5))
        self.tcPalabraBuscarWeb = wx.TextCtrl(buscadorWeb, -1, '',size=(150,-1))
        bBuscarWeb = wx.Button(buscadorWeb, -1, 'Buscar')  
        hboxBuscarWeb.Add(stBuscarWeb, 1, wx.TOP | wx.BOTTOM | wx.LEFT, 5)
        hboxBuscarWeb.Add(self.tcPalabraBuscarWeb, 0)        
        hboxBuscarWeb.Add(bBuscarWeb, 0)
        buscadorWeb.SetSizer(hboxBuscarWeb)
        
        # Navegador Web
        self.browser = html.HtmlWindow(self.panel2, -1, style=wx.NO_BORDER)
        vboxNavegadorWeb.Add(buscadorWeb, 0, wx.EXPAND)
        vboxNavegadorWeb.Add(self.browser, 1, wx.EXPAND)
        self.panel2.SetSizer(vboxNavegadorWeb)
        self.panel.SetFocus()

        # Filtrador
        self.scFiltrar = wx.SearchCtrl(self.panel, -1, pos=(5,10), size=(170,26), style=wx.TE_PROCESS_ENTER)
        self.scFiltrar.ShowCancelButton(True)

        # ListView (Panel 1)        
        self.lvPalabras = ListViewVirtual(self.panel,(5,50),(500,400),self.deutschDB.extraer())

        # ListBox (Panel 1)
        self.lbNota = wx.ListBox(self.panel, -1,(5,460),(500,360),"", wx.LB_SINGLE)

        # Rellenados Automáticos
        self.rellenarListBox(self.lbNota, self.deutschDB.extraer())        

        # La ventana comienza sin dividir.
        self.separador.SplitVertically(self.panel, self.panel2)
        self.separador.Unsplit()

        # EVENTOS
        self.Bind(wx.EVT_TOOL, self.OnNuevaPalabra, id=1)
        self.Bind(wx.EVT_TOOL, self.OnBorrarTodo, id=2)
        self.Bind(wx.EVT_TOOL, self.OnQuitarBrowser, id=3)
        self.Bind(wx.EVT_TOOL, self.OnQuitar, id=4)
        self.Bind(wx.EVT_BUTTON, self.OnBuscarWeb, id=bBuscarWeb.GetId())
        self.Bind(wx.EVT_CLOSE, self.OnQuitar, id=self.GetId())
        self.Bind(wx.EVT_LIST_COL_CLICK, self.OnOrdenar, id=self.lvPalabras.GetId())
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnMenuContextual, id=self.lvPalabras.GetId())        
        self.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.OnFiltrar, id=self.scFiltrar.GetId())
        self.Bind(wx.EVT_TEXT_ENTER, self.OnFiltrar, id=self.scFiltrar.GetId())
        self.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.OnCancelarFiltrar, id=self.scFiltrar.GetId())
        #self.Bind(wx.EVT_MENU, self.editarPalabra, id=MenuContextual.editarPalabra.GetId())
                
        self.Centre()
        self.Show()

    # METODOS
    def OnNuevaPalabra(self,event):
        nuevaPalabra = DialogoNuevaPalabra(self, -1, 'Introducir Nueva Palabra')
        if nuevaPalabra.ShowModal() == 1:
            datos = nuevaPalabra.datos      
            try: nuevo_indice = self.deutschDB.extraer()[-1][0] + 1
            except: nuevo_indice = 1
                   
            self.deutschDB.introducir(str(nuevo_indice),datos["palabra"],datos["genero"],datos["plural"],
                                      datos["traduccion"],datos["tipo"],datos ["tema"],datos["notas"])
            self.commiter()
        nuevaPalabra.Destroy()

    def editarPalabra(self, palabra):
        editarPalabra = DialogoNuevaPalabra(self, -1, 'Editar palabra')
        seleccion = self.deutschDB.extraerLinea(palabra.GetText())

        editarPalabra.stPalabra.AppendText(seleccion[1])
        editarPalabra.stTraduccion.AppendText(seleccion[4])
        editarPalabra.stNotas.AppendText(seleccion[7])
        
        nivel = self.obtener_nivel(str(seleccion[6]), editarPalabra.temas)
        editarPalabra.cbNivel.SetValue(nivel)
        editarPalabra.OnCambiarNivel()
        editarPalabra.cbTema.SetValue(str(seleccion[6]))
                
        if seleccion[2]: # Es sustantivo
            editarPalabra.rbTipo.SetSelection(0)
            editarPalabra.stPlural.AppendText(seleccion[3])
            editarPalabra.rbGenero.SetStringSelection(seleccion[2])
        else:
            editarPalabra.stPlural.Enable(False)
            editarPalabra.rbGenero.Enable(False)
            editarPalabra.rbTipo.SetStringSelection(seleccion[5])
        
        if editarPalabra.ShowModal() == 1:
            datos = editarPalabra.datos
            self.deutschDB.editar(datos["palabra"],datos["genero"],datos["plural"],
                                      datos["traduccion"],datos["tipo"],datos ["tema"],datos["notas"], str(seleccion[0]))
            self.commiter()

    def OnBuscarWeb(self,event):
        self.browser.LoadPage("http://www.wordreference.com/deen/"+self.tcPalabraBuscarWeb.GetValue())
        
    def OnBorrarTodo(self, event):
        self.deutschDB.borrarTodo()
        self.commiter()

    def OnQuitarBrowser(self,event):
        if self.separador.IsSplit():
            self.separador.Unsplit()
        else:
            self.separador.SplitVertically(self.panel, self.panel2)

    def OnQuitar(self,event):
        self.deutschDB.cerrar()
        self.Destroy()

    def OnOrdenar(self,event):
        criterio = self.lvPalabras.GetColumn(event.GetColumn()).GetText() # Cojo el nombre de la columna
        if self.criterio == criterio:   # Compruebo que el anterior criterio y el nuevo sea el mismo.
            if self.orden == "DESC":    # En caso de serlo intercambiamos entre ASC y DESC
                self.orden = "ASC" 
            else: 
                self.orden = "DESC"
        else:                           # Guardamos el criterio para que sirva para las demás funciones (filtrar, nueva_palabra, etc.)
            self.criterio = criterio 
            self.orden = "ASC"
        array_ordenado = self.deutschDB.extraer(self.criterio,self.orden)  # consulta SQL ORDER BY ese nombre de columna
        self.lvPalabras.OnRellenar(array_ordenado)    # Relleno el listview con el array ordenado

    def OnFiltrar(self,event):
        array_ordenado = self.deutschDB.extraer(self.criterio,self.orden)
        array_filtrado = []
        for linea in array_ordenado:
            coincidencia = False
            for i in (1,3,4,7): # 1 = palabra, 3 = plural, 4 = traduccion, 7 = notas
                if linea[i].count(self.scFiltrar.GetValue()) > 0:
                    coincidencia = True
            if coincidencia == True:
                array_filtrado.append(linea)

        self.lvPalabras.OnRellenar(array_filtrado)
        self.rellenarListBox(self.lbNota, array_filtrado)

    def OnCancelarFiltrar(self,event):
        self.scFiltrar.Clear()
        self.lvPalabras.OnRellenar(self.deutschDB.extraer(self.criterio,self.orden))

    def OnMenuContextual(self,event):
        self.PopupMenu(MenuContextual(self), event.GetPosition())
    
    def rellenarListBox(self, listbox, array):
        listbox.Clear() 
        for linea in array: # Recorro linea a linea el array bidimencional con la variable linea.
            listbox.Append(str(linea[0]) + " - " + linea[7])
    def commiter(self):
        self.deutschDB.commit() 
        self.rellenarListBox(self.lbNota, self.deutschDB.extraer(self.criterio,self.orden))
        self.lvPalabras.OnRellenar(self.deutschDB.extraer(self.criterio,self.orden))
        
    def obtener_nivel(self, tema, dict):
        for n, ts in dict.iteritems(): # iterItem asigna a n, la clave del dict, y a ts, el valor
            if tema in ts: 
                return n
