#!/usr/bin/python
# -*- coding: utf-8 -*-

try:
    import wx
    from framePrincipal import FramePrincipal
    try:
        import psyco
        psyco.profile()
    except ImportError:
        print "\nSe recomienda la instalación del compilador en tiempo de ejecución 'Python-Psyco' para mejorar el rendimiento.\n"

    programa = wx.App()
    try:
        FramePrincipal(None, -1, 'Py-Deutsch')
        programa.MainLoop()
    finally:
        del programa

except ImportError:
    print """No se encontraron las librerías WX para Python. 
    En distribuciones derivadas de Debian use el comando
    'apt-get install python-wxgtk2.8'

    Saliendo del Programa....."""

