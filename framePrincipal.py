import wx
from database import BaseDeDatos

class FramePrincipal(wx.Frame):
    """Ventana principal del programa """
    deutschDB = BaseDeDatos("deutsch.db")

    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(250, 250))
        
        boton1 = wx.Button(self, -1, '+', (10,10))
        boton2 = wx.Button(self, -1, '-', (10,60))
        boton3 = wx.Button(self, -1, 'Meter', (10,110))
        boton4 = wx.Button(self, -1, 'Borrar All', (10,160))
        self.texto = wx.StaticText(self, -1, '0', (40,210))
        self.lista = wx.ListBox(self, -1,(100,10),(100,160),self.deutschDB.extraer(), wx.LB_SINGLE)

        self.Bind(wx.EVT_BUTTON, self.OnMas, id=boton1.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnMenos, id=boton2.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnPush, id=boton3.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnBorrarTodo, id=boton4.GetId())
        self.Bind(wx.EVT_CLOSE, self.OnQuitar, id=self.GetId())

        self.Show(True)

    def OnMas(self,event):
        valor = int(self.texto.GetLabel()) + 1
        self.texto.SetLabel(str(valor))

    def OnMenos(self,event):
        valor = int(self.texto.GetLabel()) - 1
        self.texto.SetLabel(str(valor))

    def OnPush(self,event):      
        # Warning: Actualmente se asigna indice con el GetCount del litbox. Este sistema debe mejorarse si en el futuro se permite borrar lineas individuales.
        self.deutschDB.introducir(str(self.lista.GetCount()),self.texto.GetLabel())
        self.deutschDB.commit()
        self.lista.Set(self.deutschDB.extraer())

    def OnBorrarTodo(self,event):
            self.deutschDB.borrarTodo()
            self.deutschDB.commit()
            self.lista.Set(self.deutschDB.extraer())

    def OnQuitar(self,event):
        self.deutschDB.cerrar()
        self.Destroy()
