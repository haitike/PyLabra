#!/usr/bin/python
# -*- coding: utf-8 -*-

try:
	import wx
	
	try:
		import psyco
		psyco.profile()
	except ImportError:
		print "\nSe recomienda la instalación del compilador en tiempo de ejecución 'Python-Psyco' para mejorar el rendimiento.\n"
	
	from database import BaseDeDatos
	programa = wx.App()

	miFrame = wx.Frame(None, -1, 'simple.py',size=(800,500))
	miFrame.Show()

	programa.MainLoop()

except ImportError:
	print """		  No se encontraron las librerías WX para Python. 
		  En distribuciones derivadas de Debian use el comando
		  'apt-get install python-wxgtk2.8'

		  Saliendo del Programa..."""
