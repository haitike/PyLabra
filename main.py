#!/usr/bin/python
# -*- coding: utf-8 -*-

try:
    import wx

    try:
        import psyco
        psyco.profile()
    except ImportError:
        print "\nSe recomienda la instalación del compilador en tiempo de ejecución 'Python-Psyco' para mejorar el rendimiento.\n"

    from framePrincipal import FramePrincipal
    #from database import BaseDeDatos

    programa = wx.App()

    try:
        miFrame = wx.Frame(None, -1, 'Py-Deutsch')
        miFrame.Show()
        programa.MainLoop()
    finally:
        del programa

except ImportError:
    print """No se encontraron las librerías WX para Python. 
    En distribuciones derivadas de Debian use el comando
    'apt-get install python-wxgtk2.8'

    Saliendo del Programa....."""

