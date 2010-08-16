import wx
import wx.html as html
from database import BaseDeDatos

class FramePrincipal(wx.Frame):
    """Ventana principal del programa """
    deutschDB = BaseDeDatos("deutsch.db")

    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title,size=(1024,768))

        self.separador = wx.SplitterWindow(self, -1)
        self.panel = wx.Panel(self.separador,-1,style=wx.BORDER_SUNKEN)
        self.panel2 = wx.Panel(self.separador,-1)

        vbox = wx.BoxSizer(wx.VERTICAL)

        self.browser = html.HtmlWindow(self.panel2, -1, style=wx.NO_BORDER)
        vbox.Add(self.browser, 1, wx.EXPAND)
        self.panel2.SetSizer(vbox)
        self.panel.SetFocus()

        self.separador.SplitVertically(self.panel, self.panel2)

        self.tcValor = wx.TextCtrl(self.panel, -1, '', (10, 10))
        bMeter = wx.Button(self.panel, -1, 'Meter', (10,60))
        bBorrarAll = wx.Button(self.panel, -1, 'Borrar All', (10,110))
        bBuscar = wx.Button(self.panel, -1, 'Buscar', (10,160))
        bQuitarBrowser = wx.Button(self.panel, -1, 'Quitar/Mostrar Browser', (10,210))
        self.lista = wx.ListBox(self.panel, -1,(100,10),(100,160),self.deutschDB.extraer(), wx.LB_SINGLE)

        self.Bind(wx.EVT_BUTTON, self.OnPush, id=bMeter.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnBorrarTodo, id=bBorrarAll.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnQuitarBrowser, id=bQuitarBrowser.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnBuscar, id=bBuscar.GetId())
        self.Bind(wx.EVT_CLOSE, self.OnQuitar, id=self.GetId())

        #self.CreateStatusBar()
        self.Centre()
        self.Show(True)

    def OnPush(self,event):      
        # Warning: Actualmente se asigna indice con el GetCount del litbox.El sistema debe mejorarse si en el futuro se permite borrar lineas individuales.
        self.deutschDB.introducir(str(self.lista.GetCount()),self.tcValor.GetValue())
        self.deutschDB.commit()
        self.lista.Set(self.deutschDB.extraer())

    def OnBorrarTodo(self,event):
            self.deutschDB.borrarTodo()
            self.deutschDB.commit()
            self.lista.Set(self.deutschDB.extraer())

    def OnBuscar(self,event):
        self.browser.LoadPage("http://www.wordreference.com/deen/"+self.tcValor.GetValue())

    def OnQuitarBrowser(self,event):
        if self.separador.IsSplit():        
            self.separador.Unsplit()
        else:
            self.separador.SplitVertically(self.panel, self.panel2)

    def OnQuitar(self,event):
        self.deutschDB.cerrar()
        self.Destroy()
