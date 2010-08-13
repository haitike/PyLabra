import wx
from database import BaseDeDatos

class FramePrincipal(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(250, 200))
        
        boton1 = wx.Button(self, -1, '+', (10,10))
        boton2 = wx.Button(self, -1, '-', (10,60))
        self.texto = wx.StaticText(self, -1, '0', (40,110))

        self.Bind(wx.EVT_BUTTON, self.OnMas, id=boton1.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnMenos, id=boton2.GetId())

        self.Show(True)

    def OnMas(self,event):
        valor = int(self.texto.GetLabel()) + 1
        self.texto.SetLabel(str(valor))

    def OnMenos(self,event):
        valor = int(self.texto.GetLabel()) - 1
        self.texto.SetLabel(str(valor))
