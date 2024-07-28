# scripttecnicos
Un script para el manejo de antenas Ubiquiti, para el monitoreo de las mismas, con carga de backup y liberación de compliance.

Para solucionar el comienzo de la obsolescencia del cifrado TripleDES y otros cifrados "decrépitos", de la biblioteca
Paramiko, se pude cambiar el metodo de importación de la siguiente manera:

from cryptography.hazmat.decrepit.ciphers.algorithms import TripleDES

en los modulos pkey y transport de Paramiko.
