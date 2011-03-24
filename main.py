#!/usr/bin/python
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

import language
  
try:
    import wxversion
    wxversion.select("2.8") # Forzando la version 2.8 de WX
    import wx
    from framePrincipal import FramePrincipal
    try:
        import psyco
        psyco.profile()
    except ImportError:
        print _("\nSe recomienda la instalación del compilador en tiempo de ejecución 'Python-Psyco' para mejorar el rendimiento.\n")
except ImportError:
    print _("""No se encontraron las librerías WX para Python. 
    En distribuciones derivadas de Debian use el comando
    'apt-get install python-wxgtk2.8'

    Saliendo del Programa.....""")

def main():
    programa = wx.App()
    try:
        FramePrincipal(None, -1, 'PyLabra')
        programa.MainLoop()
    finally:
        del programa

if __name__ == '__main__':
    main()
