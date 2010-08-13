import sqlite3 as lite

class BaseDeDatos:
    """Clase gestora de base de datos sqlite3 para el programa py-deutsch."""
    __connection = None
    __cursor = None
    __conectado = False  

    def __init__ (self, archivo):                     
        try:                                                     
            self.__connection = lite.connect(archivo) 
        except lite.Error, error:                     
            print "Error: " + str(error)          
            return                                        
        self.__cursor = self.__connection.cursor()     
        self.crearTablaOperacion()
        self.__conectado = True
    
    def crearTablaOperacion(self):
        self.__cursor.execute("create table if not exists tabla1 (numero1 int, numero2 int, signo varchar(1));") 

    def introducir(self, number1, number2, sign):
        try:
            self.__cursor.execute("insert into tabla1 values(?,?,?);", (number1,number2,sign))
        except lite.Error, error:
            print "Error: " + str(error)

    def extraer(self):
        try:
            self.__cursor.execute("select * from tabla1;")
            return self.__cursor.fetchall()
        except lite.Error, error:
            print "Error: " + str(error)
    
    def borrar(self):
        try:
            self.__cursor.execute("delete from tabla1;")
            print "Borrando el historial..."
        except lite.Error, error:
            print "Error: " + str(error)

    def commit(self):    
        self.__cursor.commit() 
   
    def cerrar(self):
        self.__cursor.close()
        self.__connection.close()
        self.__conectado = False
    
    def estaConectado(self):
        return self.__conectado
