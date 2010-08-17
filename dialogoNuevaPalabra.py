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

    datos = { "palabra"    : None,
              "plural"     : None,
              "genero"     : None,
              "traduccion" : None,
              "tema"       : None,
              "notas"      : None}

    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(450, 350))

        panel = wx.Panel(self, -1)
        vbox = wx.BoxSizer(wx.VERTICAL)

        wx.StaticBox(panel, -1, 'Nueva Palabra', (55, 5), (340, 290))
        wx.StaticText(panel, -1, 'Palabra', (65, 30))
        self.stPalabra = wx.TextCtrl(panel, -1, '', (145, 25),(220,-1))
        wx.StaticText(panel, -1, 'Plural', (65, 60))
        self.stPlural =  wx.TextCtrl(panel, -1, '', (145, 55),(220,-1))
        wx.StaticText(panel, -1, 'Genero', (65, 90))
        self.rbGenero = wx.RadioBox(panel,-1,'',(145, 70),(160,28),choices=("der","das","die"),style=wx.NO_BORDER | wx.RA_SPECIFY_COLS)
        wx.StaticText(panel, -1, 'Traduccion', (65, 120))
        self.stTraduccion =  wx.TextCtrl(panel, -1, '', (145, 115),(220,-1))
        wx.StaticText(panel, -1, 'Nivel', (65, 150))
        self.cbNivel = wx.ComboBox(panel, -1, '1(A1)', (145, 145), (80, 28), choices=(self.niveles), style=wx.CB_READONLY)        
        wx.StaticText(panel, -1, 'Tema', (240, 150))
        self.cbTema = wx.ComboBox(panel, -1, '1', (285, 145), (80, 28), choices=(self.temas[self.niveles[0]]), style=wx.CB_READONLY)       
        wx.StaticText(panel, -1, 'Notas', (65, 180))
        self.stNotas = wx.TextCtrl(panel, -1, '', (145, 182),(220,100), style=wx.TE_MULTILINE)

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

    def OnCambiarNivel(self,event):
        self.cbTema.Clear()
        for valor in self.temas[self.niveles[self.cbNivel.GetSelection()]]:
            self.cbTema.Append(valor)
        self.cbTema.SetSelection(0)
   
    def OnGuardarSalir(self,event):
        self.datos["palabra"] = self.stPalabra.GetValue()
        self.datos["plural"] = self.stPlural.GetValue()
        self.datos["genero"] = str(self.rbGenero.GetSelection())
        self.datos["traduccion"] = self.stTraduccion.GetValue()
        self.datos["tema"] = self.cbTema.GetValue()
        self.datos["notas"] = self.stNotas.GetValue()     
        self.Destroy()
        self.SetReturnCode(1)   

    def OnSalir(self,event):
        self.Destroy()

    def GetDatos(self):
        return self.datos

