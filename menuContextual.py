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
        itemid = self.parent.lvPalabras.GetFocusedItem()       #Cojo el indice de la fila que selcciono
        if itemid != -1: # Si es -1, significa que no se seleciiono nada
            item = self.parent.lvPalabras.GetItem(itemid)          # Guardo los datos de esa fila en item
            self.parent.deutschDB.borrar(str(item.GetText()))      # Borro esa fila por la clave No
        print itemid