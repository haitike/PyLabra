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

class DialogoNuevaPalabraBase(wx.Dialog):

    niveles = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10')

    datos = { 
                "palabra":"",
                "plural":"",
                "genero":"NULL",    #NULL de SQL
                "traduccion":"",
                "tipo":"NULL",
                "tema":"NULL",
                "notas":""
                }
                
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(450, 380))

        panel = wx.Panel(self, -1)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        wx.StaticBox(panel, -1, _('Nueva Palabra'), (55, 5), (340, 320))
        wx.StaticText(panel, -1, _('Tipo'), (65, 30))
        self.rbTipo = wx.RadioBox(panel,-1,'',(145, 10),(160,28),choices=(_("sust."),_("verbo"),_("adj."),_("otro")),style=wx.NO_BORDER | wx.RA_SPECIFY_COLS)
        wx.StaticText(panel, -1, _('Palabra'), (65, 60))
        self.stPalabra = wx.TextCtrl(panel, -1, '', (145, 55),(220,-1))
        wx.StaticText(panel, -1, _('Plural'), (65, 90))
        self.stPlural =  wx.TextCtrl(panel, -1, '', (145, 85),(220,-1))
        wx.StaticText(panel, -1, _('Genero'), (65, 120))
        #self.rbGenero = wx.RadioBox(panel,-1,'',(145, 100),(160,28),choices=("der","das","die"),style=wx.NO_BORDER | wx.RA_SPECIFY_COLS)
        wx.StaticText(panel, -1, _('Traduccion'), (65, 150))
        self.stTraduccion =  wx.TextCtrl(panel, -1, '', (145, 145),(220,-1))
        wx.StaticText(panel, -1, _('Nivel'), (65, 180))
        self.cbNivel = wx.ComboBox(panel, -1, self.niveles[0], (145, 175), (80, 28), choices=(self.niveles), style=wx.CB_READONLY)        
        #wx.StaticText(panel, -1, 'Tema', (240, 180))
        #self.cbTema = wx.ComboBox(panel, -1, '1', (285, 175), (80, 28), choices=(self.niveles[0]), style=wx.CB_READONLY)       
        wx.StaticText(panel, -1, _('Notas'), (65, 210))
        self.stNotas = wx.TextCtrl(panel, -1, '', (145, 212),(220,100), style=wx.TE_MULTILINE)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.bGuardarSalir = wx.Button(self, -1, _('Guardar y Salir'))#, size=(70, 30))
        self.bGuardarContinuar = wx.Button(self, -1, _('Guardar y Continuar'))#, size=(70, 30))
        self.bGuardarContinuar.Enable(False)  # Borrar en el futuro
        self.bSalir = wx.Button(self, -1, _('Salir'), size=(70, 30))
        hbox.Add(self.bGuardarSalir, 1)
        hbox.Add(self.bGuardarContinuar, 1, wx.LEFT, 5)
        hbox.Add(self.bSalir, 1, wx.LEFT, 5)

        vbox.Add(panel)
        vbox.Add(hbox, 1, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)

        self.SetSizer(vbox)

        #self.Bind(wx.EVT_COMBOBOX, self.OnCambiarNivel, id=self.cbNivel.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnGuardarSalir, id=self.bGuardarSalir.GetId())
        self.Bind(wx.EVT_BUTTON, lambda id: self.Close(), id=self.bSalir.GetId())
        self.Bind(wx.EVT_RADIOBOX, self.OnCambiarTipo, id=self.rbTipo.GetId())
        
    def OnCambiarTipo(self,event):
        if self.rbTipo.GetSelection() == 0: # Si es Sustantivo
            self.stPlural.Enable(True)
            self.rbGenero.Enable(True)
        else:
            self.stPlural.Enable(False)
            self.rbGenero.Enable(False)     # Si es Adjetivo, Verbo o Adverbio

    def OnCambiarNivel(self,event=None):
        self.cbTema.Clear()
        for valor in self.temas[self.cbNivel.GetValue()]:
            self.cbTema.Append(valor)
        self.cbTema.SetSelection(0)
   
    def OnGuardarSalir(self,event):
        self.datos["palabra"] = self.stPalabra.GetValue()
        self.datos["traduccion"] = self.stTraduccion.GetValue()
        self.datos["tipo"] = self.rbTipo.GetStringSelection()
        #self.datos["tema"] = self.cbTema.GetValue()
        self.datos["notas"] = self.stNotas.GetValue()     

        if self.rbTipo.GetSelection() == 0: # Si es Sustantivo
            self.datos["plural"] = self.stPlural.GetValue()
            self.datos["genero"] = self.rbGenero.GetStringSelection()
        else:
            self.datos["plural"] = ""
            self.datos["genero"] = ""

        self.Destroy()
        self.SetReturnCode(1) # Hacemos que al llamarlo con ShowModal devuelva el integer 1.   

    def obtener_nivel(self, tema):
        for n, ts in self.temas.iteritems(): # iterItem asigna a n, la clave del dict, y a ts, el valor
            if tema in ts: 
                return n
