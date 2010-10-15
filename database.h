#ifndef DATABASE_H
#define DATABASE_H

#include <sqlite3.h>
#include <string.h>

using namespace std;

class database {
private:
	sqlite3 *db;	         // Objeto de tipo sqlite donde se almacena la conexión con la base de datos.
	sqlite3_stmt *datos;  	 // Los objetos "stmt" de sqlite almacenan los datos obetenidos con una consulta/query (ej: Select...)
	
public:
	database(string);
	void conectar();
	void crearTabla();
	void introducir( string dni, string nombre, string apellido, string direccion, string localidad, int telefono1, int telefono2, int telefono3 );
	void prepararExtraer();
	void cerrar();

};

#endif // DATABASE_H
