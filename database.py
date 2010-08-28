import sqlite3 as lite

class BaseDeDatos:
    """Clase gestora de base de datos sqlite3 para el programa py-deutsch."""
    connection = None
    cursor = None
    conectado = False  

    def __init__ (self, archivo):                     
        try:                                                     
            self.connection = lite.connect(archivo) 
        except lite.Error, error:                     
            print "Error: " + str(error)          
            return                                        
        self.cursor = self.connection.cursor()     
        self.crearTablaOperacion()
        self.conectado = True
    
    def crearTablaOperacion(self):
        self.cursor.execute("create table if not exists palabras (indice int, palabra varchar, genero tinyint, plural varchar,  traduccion varchar, tipo tinyint, tema tinyint, notas varchar);") 
        self.cursor.execute("create table if not exists gramatica (indice int, texto varchar);") 
        self.cursor.execute("create table if not exists opciones (nombre varchar, valor boolean);") 

    def introducir(self,indice,palabra,genero,plural,traduccion,tipo,tema,notas):
        try:
            self.cursor.execute("insert into palabras values("+indice+",'"+palabra+"',"+genero+",'"+plural+"','"+traduccion+"',"+tipo+","+tema+",'"+notas+"');")        
        except lite.Error, error:
            print "Error: " + str(error)

    def extraer(self):
        try:
            self.cursor.execute("select * from palabras;")
            return self.cursor.fetchall()
        except lite.Error, error:
            print "Error: " + str(error)

    def borrar(self, indice):
        try:
            self.cursor.execute("delete from palabras WHERE indice = "+indice+";")
        except lite.Error, error:
            print "Error: " + str(error)

    def borrarTodo(self):
        try:
            self.cursor.execute("delete from palabras;")
        except lite.Error, error:
            print "Error: " + str(error)

    def commit(self):    
        self.connection.commit() 
   
    def cerrar(self):
        self.cursor.close()
        self.connection.close()
        self.conectado = False
    
    def estaConectado(self):
        return self.conectado
