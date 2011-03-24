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

class agregarIdioma(wx.Dialog):
    #metodos
    def __init__(self,  parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(300, 90))
        
        #widgets
        self.panel1 = wx.Panel(self,-1, style=wx.NO_BORDER)
        self.panel2 = wx.Panel(self,-1, style=wx.NO_BORDER)
        
        #self.panel1.SetBackgroundColour("BLUE")
        #self.panel2.SetBackgroundColour("RED")
        
        self.bSalir= wx.Button(self,  wx.ID_CLOSE, _('Salir'))
        self.bCrearIdioma= wx.Button(self,  -1, _('Crear Idioma'))
        
        self.box = wx.BoxSizer(wx.VERTICAL)
        self.hBox = wx.BoxSizer(wx.HORIZONTAL)
        self.box.Add(self.panel1, 2, wx.EXPAND)
        self.box.Add(self.panel2, 1, wx.EXPAND)
        self.box.Add(self.hBox,  0,  wx.EXPAND | wx.ALIGN_BOTTOM)
        self.hBox.Add(self.bSalir,  1, wx.RIGHT)
        self.hBox.Add(self.bCrearIdioma,  1, wx.LEFT)
        
        self.SetAutoLayout(True)
        self.SetSizer(self.box)
        self.Layout()
        
        #eventos
        self.Bind(wx.EVT_BUTTON, self.onSalir, id=wx.ID_CLOSE)
    
    def onSalir(self,  event):
        self.Destroy()
        self.SetReturnCode(1)
