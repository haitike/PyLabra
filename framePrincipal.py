import wx
from database import BaseDeDatos

class FramePrincipal(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(250, 250))
        
        boton1 = wx.Button(self, -1, '+', (10,10))
        boton2 = wx.Button(self, -1, '-', (10,60))
        boton3 = wx.Button(self, -1, 'Meter', (10,110))
        boton4 = wx.Button(self, -1, 'Quitar', (10,160))
        self.texto = wx.StaticText(self, -1, '0', (40,210))
        self.lista = wx.ListBox(self, -1,(100,10),(100,160),["0"], wx.LB_SINGLE)

        self.Bind(wx.EVT_BUTTON, self.OnMas, id=boton1.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnMenos, id=boton2.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnMeter, id=boton3.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnQuitar, id=boton4.GetId())

        self.Show(True)

    def OnMas(self,event):
        valor = int(self.texto.GetLabel()) + 1
        self.texto.SetLabel(str(valor))

    def OnMenos(self,event):
        valor = int(self.texto.GetLabel()) - 1
        self.texto.SetLabel(str(valor))

    def OnMeter(self,event):
        self.lista.Insert(self.texto.GetLabel(),self.lista.GetCount())

    def OnQuitar(self,event):
        if self.lista.GetSelection() >= 0: 
            self.lista.Delete(self.lista.GetSelection())
        else:
             wx.MessageBox('Selecciona el elemento a borrar', 'Error',wx.ICON_ERROR)
