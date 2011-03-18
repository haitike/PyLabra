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
from dialogoNuevaPalabra import DialogoNuevaPalabra

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
        itemid = self.parent.lvPalabras.GetFirstSelected()
        if itemid != -1: # Si es -1, significa que no se seleciono nada
            item = self.parent.lvPalabras.GetItem(itemid) # si en esta funcion pongo GetItem(itemid, n) Donde n es un entero, Seleccionare el contenido de la columna indicada en n
            self.parent.editarPalabra(item)

    def OnBorrarPalabra(self, event):
        question = wx.MessageDialog(self.parent,'Seguro que quieres Eliminar la palabra', 'Question', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        if question.ShowModal() == wx.ID_YES:
            itemid = self.parent.lvPalabras.GetFirstSelected()
            if itemid != -1: # Si es -1, significa que no se seleciono nada
                item = self.parent.lvPalabras.GetItem(itemid)
                self.parent.deutschDB.borrar(str(item.GetText())) # Borro esa fila por la clave No
                self.parent.commiter()
