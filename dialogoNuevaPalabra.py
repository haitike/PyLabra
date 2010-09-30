import wx

class DialogoNuevaPalabra(wx.Dialog):

    niveles = ("1(A1)","2(A1)","3(A2)","4(A2)","5(B1)","6(B1)","1-1","1-2","2-1","2-2",">3")
    
    temas = { niveles[0] : ("1","2","3","4","5","6","7"),
              niveles[1] : ("8","9","10","11","12","13","14"),
              niveles[2] : ("15","16","17","18","19","20","21"),
              niveles[3] : ("22","23","24","25","26","27","28"),
              niveles[4] : ("29","30","31","32","33","34","35"),
              niveles[5] : ("36","37","38","39","40","41","42"),
              niveles[6] : ("43","44","45","46"),
              niveles[7] : ("47","48","49","50"),
              niveles[8] : ("51","52","53","54"),
              niveles[9] : ("55","56","57","58"),
              niveles[10] : ("59","60","61","62","63","64","65","66","67","68","69","70","71","72","73","74",)}

    datos = { "palabra"    : "",
              "plural"     : "",
              "genero"     : "NULL",    #NULL de SQL
              "traduccion" : "",
              "tipo"       : "NULL",
              "tema"       : "NULL",
              "notas"      : ""}

    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(450, 380))

        panel = wx.Panel(self, -1)
        vbox = wx.BoxSizer(wx.VERTICAL)

        wx.StaticBox(panel, -1, 'Nueva Palabra', (55, 5), (340, 320))
        wx.StaticText(panel, -1, 'Tipo', (65, 30))
        self.rbTipo = wx.RadioBox(panel,-1,'',(145, 10),(160,28),choices=("sust.","verbo","adj.","otro"),style=wx.NO_BORDER | wx.RA_SPECIFY_COLS)
        wx.StaticText(panel, -1, 'Palabra', (65, 60))
        self.stPalabra = wx.TextCtrl(panel, -1, '', (145, 55),(220,-1))
        wx.StaticText(panel, -1, 'Plural', (65, 90))
        self.stPlural =  wx.TextCtrl(panel, -1, '', (145, 85),(220,-1))
        wx.StaticText(panel, -1, 'Genero', (65, 120))
        self.rbGenero = wx.RadioBox(panel,-1,'',(145, 100),(160,28),choices=("der","das","die"),style=wx.NO_BORDER | wx.RA_SPECIFY_COLS)
        wx.StaticText(panel, -1, 'Traduccion', (65, 150))
        self.stTraduccion =  wx.TextCtrl(panel, -1, '', (145, 145),(220,-1))
        wx.StaticText(panel, -1, 'Nivel', (65, 180))
        self.cbNivel = wx.ComboBox(panel, -1, '1(A1)', (145, 175), (80, 28), choices=(self.niveles), style=wx.CB_READONLY)        
        wx.StaticText(panel, -1, 'Tema', (240, 180))
        self.cbTema = wx.ComboBox(panel, -1, '1', (285, 175), (80, 28), choices=(self.temas[self.niveles[0]]), style=wx.CB_READONLY)       
        wx.StaticText(panel, -1, 'Notas', (65, 210))
        self.stNotas = wx.TextCtrl(panel, -1, '', (145, 212),(220,100), style=wx.TE_MULTILINE)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.bGuardarSalir = wx.Button(self, -1, 'Guardar y Salir')#, size=(70, 30))
        self.bGuardarContinuar = wx.Button(self, -1, 'Guardar y Continuar')#, size=(70, 30))
        self.bGuardarContinuar.Enable(False)  # Borrar en el futuro
        self.bSalir = wx.Button(self, -1, 'Salir', size=(70, 30))
        hbox.Add(self.bGuardarSalir, 1)
        hbox.Add(self.bGuardarContinuar, 1, wx.LEFT, 5)
        hbox.Add(self.bSalir, 1, wx.LEFT, 5)

        vbox.Add(panel)
        vbox.Add(hbox, 1, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)

        self.SetSizer(vbox)

        self.Bind(wx.EVT_COMBOBOX, self.OnCambiarNivel, id=self.cbNivel.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnGuardarSalir, id=self.bGuardarSalir.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnSalir, id=self.bSalir.GetId())
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
        self.datos["tema"] = self.cbTema.GetValue()
        self.datos["notas"] = self.stNotas.GetValue()     

        if self.rbTipo.GetSelection() == 0: # Si es Sustantivo
            self.datos["plural"] = self.stPlural.GetValue()
            self.datos["genero"] = self.rbGenero.GetStringSelection()
        else:
            self.datos["plural"] = ""
            self.datos["genero"] = ""

        self.Destroy()
        self.SetReturnCode(1) # Hacemos que al llamarlo con ShowModal devuelva el integer 1.   

    def OnSalir(self,event):
        self.Destroy()

    def obtener_nivel(self, tema):
        for n, ts in self.temas.iteritems(): # iterItem asigna a n, la clave del dict, y a ts, el valor
            if tema in ts: 
                return n
