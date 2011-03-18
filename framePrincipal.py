# -*- coding: utf-8 -*-

# py-deutsch is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Py-deutsch is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Py-deutsch.  If not, see <http://www.gnu.org/licenses/>.

import wx
import wx.html as html
from database import BaseDeDatos
from dialogoNuevaPalabra import DialogoNuevaPalabra
from listviewVirtual import ListViewVirtual
from menuContextual import MenuContextual
import resources
import sys
import wx.lib.wxpTag

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
        # Menu
        menu = wx.MenuBar()
        archivo = wx.Menu()
        
        abrir = wx.MenuItem(archivo, 1,'A&brir Idioma\tCtrl+A')
        guardar = wx.MenuItem(archivo,  -1, '&Guardar idioma\tCtrl+G')
        borrar = wx.MenuItem(archivo,  -1, '&Borrar Idioma\tCtrl+B')
        cerrar = wx.MenuItem(archivo,  4, '&Cerrar PyLabra\tCtrl+C')
        
        #abrir.SetBitmap(wx.Bitmap(resources.images['nuevaPalabra']))
        #cerrar.SetBitmap(wx.Bitmap(resources.images['salir']))
        
        menu.Append(archivo, '&Archivo')
        
        archivo.AppendItem(abrir)
        archivo.AppendItem(guardar)
        archivo.AppendItem(borrar)
        archivo.AppendItem(cerrar)
        self.SetMenuBar(menu)

        self.Centre()
        self.Show(True)
        
        # Barra de Herramientas
        barra_herramientas = self.CreateToolBar()
        barra_herramientas.AddLabelTool(1, '', wx.Bitmap(resources.images['nuevaPalabra']), shortHelp="Introduce una nueva palabra")
        barra_herramientas.AddLabelTool(2, '', wx.Bitmap(resources.images['borrarDB']), shortHelp="Borra la base de datos")
        barra_herramientas.AddCheckLabelTool(3, '', wx.Bitmap(resources.images['mostrarNavegador']), shortHelp="Muestra/Oculta el navegador")
        barra_herramientas.AddSeparator()
        barra_herramientas.AddLabelTool(5, '', wx.Bitmap(resources.images['about']), shortHelp="Acerca de...")
        barra_herramientas.AddLabelTool(4, '', wx.Bitmap(resources.images['salir']), shortHelp="Salir")
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
        
        vboxPanel = wx.BoxSizer(wx.VERTICAL)
        # Filtrador
        self.scFiltrar = wx.SearchCtrl(self.panel, -1, pos=(5,10), size=(170,26), style=wx.TE_PROCESS_ENTER)
        self.scFiltrar.ShowCancelButton(True)
        vboxPanel.Add(self.scFiltrar, 0)

        # ListView (Panel 1)        
        self.lvPalabras = ListViewVirtual(self.panel,(5,50),(500,400),self.deutschDB.extraer())
        vboxPanel.Add(self.lvPalabras, 0, wx.EXPAND)
        
        # ListBox (Panel 1)
        self.lbNota = wx.ListBox(self.panel, -1,(5,460),(500,360),"", wx.LB_SINGLE)
        vboxPanel.Add(self.lbNota, 0, wx.EXPAND)
        
        self.panel.SetSizer(vboxPanel)
        vboxPanel.SetSizeHints(self) #Tamanyo minimo para el sizer
        # Rellenados Automáticos
        self.rellenarListBox(self.lbNota, self.deutschDB.extraer())        

        # La ventana comienza sin dividir.
        self.separador.SplitVertically(self.panel, self.panel2)
        #self.separador.Unsplit()

        # EVENTOS
        self.Bind(wx.EVT_TOOL, self.OnNuevaPalabra, id=1)
        self.Bind(wx.EVT_TOOL, self.OnBorrarTodo, id=2)
        self.Bind(wx.EVT_TOOL, self.OnQuitarBrowser, id=3)
        self.Bind(wx.EVT_TOOL, self.OnQuitar, id=4)
        self.Bind(wx.EVT_TOOL, self.OnAbout, id=5)
        self.Bind(wx.EVT_BUTTON, self.OnBuscarWeb, id=bBuscarWeb.GetId())
        self.Bind(wx.EVT_CLOSE, self.OnQuitar, id=self.GetId())
        self.Bind(wx.EVT_LIST_COL_CLICK, self.OnOrdenar, id=self.lvPalabras.GetId())
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnMostrarMenuContextual, id=self.lvPalabras.GetId())        
        self.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.OnFiltrar, id=self.scFiltrar.GetId())
        self.Bind(wx.EVT_TEXT_ENTER, self.OnFiltrar, id=self.scFiltrar.GetId())
        self.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.OnCancelarFiltrar, id=self.scFiltrar.GetId())
                
        self.Maximize()
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
        
    def OnAbout(self, envent):
        self.text = '''
<html>
<body bgcolor="#CCCCCC">
    <center><table bgcolor="#458154" width="100%%" cellspacing="0"
    cellpadding="0" border="1">
    <tr>
        <td align="center">
            <h1>PyLabra Alpha release</h1>
            <h3>Versi&oacute;n de wxPython: %s</h3>
            Corriendo en Python %s<br>
        </td>
    </tr>
    </table>
    <h1>Autores de PyLabra:</h1>
    <p>Alejandro Alcalde <em>(algui91)</em> -> <a href="mailto:algui91@gmail.com">algui91@gmail.com</a></p>
    <p>Francisco José Rodríguez <em>(haitike)</em> -> <a href="mailto:haitike@gmail.com">haitike@gmail.com</a></p>

    <p>
    <font size="-1">About parcialmente realizado de los ejemplos de wxPython.</font>
    </p>
    <p>
    <font size="-1">Licencia: http://www.gnu.org/licenses/gpl-3.0.html</font>
    </p>
    <p>
    <font size="-1">Sitio Web http://bashyc.blogspot.com</font>
    </p>


    <p><wxp module="wx" class="Button">
        <param name="label" value="Cerrar">
        <param name="id"    value="ID_OK">
    </wxp></p>
    </center>
</body>
</html>
'''
        about = wx.Dialog(self, -1, 'Acerca de PyLabra...', size=(420,420))
        FrameHtml = wx.html.HtmlWindow(about, -1, size=(420, -1))
        py_version = sys.version.split()[0]
        txt = self.text % (wx.VERSION_STRING, py_version)
        FrameHtml.SetPage(txt)
        btn = FrameHtml.FindWindowById(wx.ID_OK)
        ir = FrameHtml.GetInternalRepresentation()
        FrameHtml.SetSize( (ir.GetWidth()+25, ir.GetHeight()+25) )
        self.SetClientSize(FrameHtml.GetSize())
        self.CentreOnParent(wx.BOTH)
        
        about.ShowModal()
        
    def editarPalabra(self, palabra):
        editarPalabra = DialogoNuevaPalabra(self, -1, 'Editar palabra')
        seleccion = self.deutschDB.extraerLinea(palabra.GetText())

        editarPalabra.stPalabra.AppendText(seleccion[1])
        editarPalabra.stTraduccion.AppendText(seleccion[4])
        editarPalabra.stNotas.AppendText(seleccion[7])
        
        nivel = editarPalabra.obtener_nivel(str(seleccion[6]))
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

    def OnMostrarMenuContextual(self,event):
        if event.GetIndex() != -1:
            posicion = event.GetPosition()
            posicion.Set(posicion.Get()[0],posicion.Get()[1] + 70) # X vale lo mismo, a Y se le suma 70.
            self.PopupMenu(MenuContextual(self), posicion)
    
    def rellenarListBox(self, listbox, array):
        listbox.Clear() 
        for linea in array: # Recorro linea a linea el array bidimencional con la variable linea.
            listbox.Append(str(linea[0]) + " - " + linea[7])
    def commiter(self):
        self.deutschDB.commit() 
        self.rellenarListBox(self.lbNota, self.deutschDB.extraer(self.criterio,self.orden))
        self.lvPalabras.OnRellenar(self.deutschDB.extraer(self.criterio,self.orden))
