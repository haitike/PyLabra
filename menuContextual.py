import wx

class MenuContextual(wx.Menu):
    def __init__(self, parent):
        wx.Menu.__init__(self)

        self.parent = parent
        
        editarPalabra = wx.MenuItem(self, wx.NewId(), 'Editar Palabra')
        self.AppendItem(editarPalabra)
        self.Bind(wx.EVT_MENU, self.OnEditarPalabra, id=editarPalabra.GetId())

        borrarPalabra = wx.MenuItem(self, wx.NewId(), 'Borrar Palabra')
        self.AppendItem(borrarPalabra)
        self.Bind(wx.EVT_MENU, self.OnBorrarPalabra, id=borrarPalabra.GetId())
        
        
    def OnEditarPalabra(self, event):
        print "editando palabra"

    def OnBorrarPalabra(self, event):
        print "borrando palabra"
        self.parent.deutschDB.borrar(str(self.parent.lvPalabras.GetFocusedItem()+1))