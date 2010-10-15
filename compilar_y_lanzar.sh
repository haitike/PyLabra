# Script en bash personalizado que compila usando wxwidgets, y si el archivo resultante existe lo lanza.

nombre=deutcsh

g++ main.cpp frameprincipal.cpp database.cpp `wx-config --libs --unicode=yes` `wx-config --cxxflags --unicode=yes --debug=yes` -o $nombre
if [ -e $nombre ]; then
	./$nombre
	rm $nombre
fi
