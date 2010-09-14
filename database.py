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
        self.cursor.execute("create table if not exists palabras (No int, Palabra varchar, Genero varchar, \
            Plural varchar,  Traduccion varchar, Tipo varchar, Tema tinyint, Notas varchar);") 
        self.cursor.execute("create table if not exists gramatica (indice int, texto varchar);") 
        self.cursor.execute("create table if not exists opciones (nombre varchar, valor boolean);") 

    def introducir(self,indice,palabra,genero,plural,traduccion,tipo,tema,notas):
        try:
            self.cursor.execute("insert into palabras values(?, ?, ?, ?, ?, ?, ?, ?)",
                (indice, palabra, genero, plural, traduccion, tipo, tema, notas))     #Intruccion parametrizada qmark style   
        except lite.Error, error:
            print "Error: " + str(error)

    def extraer(self,criterio="No", orden="ASC"):
        try:
            self.cursor.execute("select * from palabras ORDER BY "+criterio+" "+orden+";")
            return self.cursor.fetchall()
        except lite.Error, error:
            print "Error: " + str(error)
            return

    def extraer2(self, criterio):
        try:
            self.cursor.execute("select * from palabras where No='%s'" % criterio )
            return self.cursor.fetchall()
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
