import wx
import wx.html as html
from database import BaseDeDatos
from dialogoNuevaPalabra import DialogoNuevaPalabra

class FramePrincipal(wx.Frame):
    """Ventana principal del programa """
    deutschDB = BaseDeDatos("deutsch.db")

    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title,size=(1024,768))

        self.separador = wx.SplitterWindow(self, -1)
        self.panel = wx.Panel(self.separador,-1,style=wx.BORDER_SUNKEN)
        self.panel2 = wx.Panel(self.separador,-1)

        vbox = wx.BoxSizer(wx.VERTICAL)
        buscadorWeb = wx.Panel(self.panel2, -1, size=(-1, 20))
        buscadorWeb.SetBackgroundColour('#6f6a59')
        buscadorWeb.SetForegroundColour('WHITE')
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        st = wx.StaticText(buscadorWeb, -1, 'Buscar en WordReference', (5, 5))
        hbox.Add(st, 1, wx.TOP | wx.BOTTOM | wx.LEFT, 5)
        self.tcPalabraBuscarWeb = wx.TextCtrl(buscadorWeb, -1, '')
        hbox.Add(self.tcPalabraBuscarWeb, 0)
        bBuscarWeb = wx.Button(buscadorWeb, -1, 'Buscar')  
        hbox.Add(bBuscarWeb, 0)
        buscadorWeb.SetSizer(hbox)

        vbox.Add(buscadorWeb, 0, wx.EXPAND)

        self.browser = html.HtmlWindow(self.panel2, -1, style=wx.NO_BORDER)
        vbox.Add(self.browser, 1, wx.EXPAND)
        self.panel2.SetSizer(vbox)
        self.panel.SetFocus()

        self.separador.SplitVertically(self.panel, self.panel2)

        bNuevoContacto = wx.Button(self.panel, -1, 'Introducir Nueva Palabra', (10,10))
        bBorrarAll = wx.Button(self.panel, -1, 'Borrar All', (10,60))
        bQuitarBrowser = wx.Button(self.panel, -1, 'Quitar/Mostrar Browser', (10,110))
        self.lista = wx.ListBox(self.panel, -1,(180,10),(310,600),"", wx.LB_SINGLE)
        self.rellenarListBox(self.lista, self.deutschDB.extraer())

        self.Bind(wx.EVT_BUTTON, self.OnNuevaPalabra, id=bNuevoContacto.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnBorrarTodo, id=bBorrarAll.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnQuitarBrowser, id=bQuitarBrowser.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnBuscarWeb, id=bBuscarWeb.GetId())
        self.Bind(wx.EVT_CLOSE, self.OnQuitar, id=self.GetId())

        self.CreateStatusBar()
        self.Centre()
        self.Show(True)

    def OnNuevaPalabra(self,event):      
        nuevaPalabra = DialogoNuevaPalabra(None, -1, 'Introducir Nueva Palabra')
        if nuevaPalabra.ShowModal() == 1:
            datos = nuevaPalabra.GetDatos()      
        
            #Warning: Actualmente se asigna indice con el GetCount del litbox. El sistema debe mejorarse si en el futuro.            
            self.deutschDB.introducir(str(self.lista.GetCount()),datos["palabra"],datos["plural"],datos["genero"],datos["traduccion"],datos["tema"],
                                          datos["notas"])
            self.deutschDB.commit()
            self.rellenarListBox(self.lista, self.deutschDB.extraer())

        nuevaPalabra.Destroy()

    def OnBorrarTodo(self,event):
            self.deutschDB.borrarTodo()
            self.deutschDB.commit()
            self.rellenarListBox(self.lista, self.deutschDB.extraer())

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

    def rellenarListBox(self, listbox, array):
        articulos = { 0 : ",der" , 1 : ",das" , 2 : ",die", None : ""}
        listbox.Clear() 
        for linea in array: # Recorro linea a linea el array bidimencional con la variable linea.
            listbox.Append(str(linea[0]) + " - " + linea[1] + articulos[linea[3]] + " (" + linea[2] + ") ----> Tema " + str(linea[5]) + "|| NOTAS: " + str(linea[6]) )
