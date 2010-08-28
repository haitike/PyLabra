#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
import wx.html as html
from database import BaseDeDatos
from dialogoNuevaPalabra import DialogoNuevaPalabra

class FramePrincipal(wx.Frame):
    """Ventana principal del programa """
    deutschDB = BaseDeDatos("deutsch.db")

    def __init__(self, parent, id, title):
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

        # ListBox (Panel 1)
        self.lbNota = wx.ListBox(self.panel, -1,(5,420),(500,400),"", wx.LB_SINGLE)

        # LAS DOS LINEAS DE ABAJO SON EQUIVALENTES. LISTVIEW ES UN LISTCTRL CON ESTILO LC_REPORT.
        #self.lcPalabras = wx.ListCtrl(self.panel, -1,(5,10),(500,400), style=wx.LC_REPORT)
        #self.lcPalabras = wx.ListView(self.panel, -1,(5,10),(500,400))

        # ListView (Panel 1)        
        self.lvPalabras = wx.ListView(self.panel, -1,(5,10),(500,400))
        self.lvPalabras.InsertColumn(0,"#")
        self.lvPalabras.InsertColumn(1,"Palabra")
        self.lvPalabras.InsertColumn(2,"Genero")
        self.lvPalabras.InsertColumn(3,"Plural")
        self.lvPalabras.InsertColumn(4,"Traduccion")
        self.lvPalabras.InsertColumn(5,"Tipo")        
        self.lvPalabras.InsertColumn(6,"Tema")
        self.lvPalabras.InsertColumn(7,"Notas")
        self.lvPalabras.SetColumnWidth(0,20)#wx.LIST_AUTOSIZE)
        for i in range(1,8): self.lvPalabras.SetColumnWidth(i,65)#wx.LIST_AUTOSIZE)

        # Rellenados Automáticos
        self.rellenarListBox(self.lbNota, self.deutschDB.extraer())        
        self.rellenarListView(self.lvPalabras, self.deutschDB.extraer())   

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

        self.Centre()
        self.Show(True)

    def OnNuevaPalabra(self,event):      
        nuevaPalabra = DialogoNuevaPalabra(None, -1, 'Introducir Nueva Palabra')
        if nuevaPalabra.ShowModal() == 1:
            datos = nuevaPalabra.GetDatos()      
        
            #Warning: Actualmente se asigna indice con el GetCount del litbox. El sistema debe mejorarse si en el futuro.            
            self.deutschDB.introducir(str(self.lvPalabras.GetItemCount()),datos["palabra"],datos["plural"],datos["genero"],datos["traduccion"],datos["tipo"],
                                          datos ["tema"],datos["notas"])
            self.deutschDB.commit()
            self.rellenarListBox(self.lbNota, self.deutschDB.extraer())
            self.rellenarListView(self.lvPalabras, self.deutschDB.extraer())   

        nuevaPalabra.Destroy()

    def OnBorrarTodo(self,event):
            self.deutschDB.borrarTodo()
            self.deutschDB.commit()
            self.rellenarListBoxs(self.lbPalabras, self.lbNota, self.deutschDB.extraer())

    def OnBuscarWeb(self,event):
        self.browser.LoadPage("http://www.wordreference.com/deen/"+self.tcPalabraBuscarWeb.GetValue())

    def OnQuitarBrowser(self,event):
        if self.separador.IsSplit():        
            self.separador.Unsplit()
        else:
            self.separador.SplitVertically(self.panel, self.panel2)

    def OnQuitar(self,event):
        self.deutschDB.cerrar()
        self.Destroy()

    def OnOrdenar(self,event):
        print event.GetColumn()

    def rellenarListBox(self, listbox, array):
        listbox.Clear() 
        for linea in array: # Recorro linea a linea el array bidimencional con la variable linea.
            listbox.Append(str(linea[0]) + " - " + linea[7])

    def rellenarListView(self, listview, array):
        articulos = { 0 : "der" , 1 : "das" , 2 : "die", None : ""}
        tipos = { 0 : "sustantivo" , 1 : "verbo" , 2 : "adjetivo", 3 : "Otro"}
        listview.DeleteAllItems() 
        for linea in array:
            listview.InsertStringItem(linea[0], str(linea[0]))
            listview.SetStringItem(linea[0],1, linea[1])
            listview.SetStringItem(linea[0],2, articulos[linea[3]])
            listview.SetStringItem(linea[0],3, linea[2])
            listview.SetStringItem(linea[0],4, linea[4])
            listview.SetStringItem(linea[0],5, tipos[linea[5]])
            listview.SetStringItem(linea[0],6, str(linea[6]))
            listview.SetStringItem(linea[0],7, linea[7])
            # Pendiente: mirar correctamente el asignamiento del índice de la fila y del atributo data del listview.
