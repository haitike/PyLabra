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

import sqlite3 as lite

class BaseDeDatos:
    """Clase gestora de base de datos sqlite3 para el programa PyLabra."""
    connection = None
    cursor = None
    conectado = False  

    def __init__ (self, archivo):                     
        try:                                                     
            self.connection = lite.connect(archivo) 
            self.conectado = True
        except lite.Error, error:                     
            print "Ocurrio un error con la Base de Datos: " + str(error)          
            return                                        
        self.cursor = self.connection.cursor()     
        self.inicializar()
    
    def crearNuevoIdioma(self):
        pass
        
    def borrarIdioma(self):
        pass
        
    def inicializar(self):
        self.campos = 'No int(5) PRIMARY KEY, Palabra varchar2(50), Genero varchar2(10), \
            Plural varchar2(10),  Traduccion varchar2(50), Tipo varchar2(15), nivel tinyint, Notas varchar(100)'
        #self.cursor.execute(
        #   "create table if not exists palabras ("+self.campos+");") 
        self.cursor.execute(
            "create table if not exists tablaIndice (CodIdioma int(3), nombreTabla varchar2(20) primary key);")

    def introducir(self,indice,palabra,genero,plural,traduccion,tipo,tema,notas):
        try:
            self.cursor.execute("insert into palabras values(?, ?, ?, ?, ?, ?, ?, ?)",
                (indice, palabra, genero, plural, traduccion, tipo, tema, notas))     #Intruccion parametrizada qmark style   
        except lite.Error, error:
            print "Error: " + str(error)
    
    def editar(self,palabra,genero,plural,traduccion,tipo,tema,notas,indice):
        try:
            self.cursor.execute("update palabras set Palabra=?, Genero=?, Plural=?, Traduccion=?, Tipo=?, nivel=?, Notas=? where No=?",
                (palabra, genero, plural, traduccion, tipo, tema, notas, indice))     #Intruccion parametrizada qmark style   
        except lite.Error, error:
            print "Error: " + str(error)

    def extraer(self,criterio="No", orden="ASC"):
        try:
            self.cursor.execute("select * from palabras ORDER BY %s %s;" % (criterio, orden))
            return self.cursor.fetchall()
        except lite.Error, error:
            print "Error: " + str(error)
            return

    def extraerLinea(self, criterio):
        try:
            self.cursor.execute("select * from palabras where No='%s'" % criterio )
            return self.cursor.fetchall()[0]
        except lite.Error, error:
            print "Error: " + str(error)
            return

    def borrar(self, indice):
        try:
            self.cursor.execute("delete from palabras WHERE No = :indice", {"indice": indice}) #Intruccion parametrizada named style
        except lite.Error, error:
            print "Error: " + str(error)

    def borrarTodo(self):
        try:
            self.cursor.execute("delete from palabras;")
        except lite.Error, error:
            print "Error: " + str(error)

    def cerrar(self):
        self.cursor.close()
        self.connection.close()
        self.conectado = False

    def commit(self):
        self.connection.commit()
