import csv
import platform
import os


def char_range(c1, c2):  # crea un iterador de carácters
    """Generates the characters from `c1` to `c2`, inclusive."""
    for c in range(ord(c1), ord(c2) + 1):
        yield chr(c)


class Sonder:  # clase que sirve para explorar el sistema de ficheros
    def __init__(self):
        # inicia los writers a csv de nodos y adyacencia
        self.archivoSalidaNodos = open("salidaNodos.csv", "w", newline="", encoding="utf-8")
        self.escritorNodos = csv.writer(self.archivoSalidaNodos, delimiter=";")
        self.archivoSalidaAdyacencia = open("salidaAdyacencia.csv", "w", newline="", encoding="utf-8")
        self.escritorAdyacencia = csv.writer(self.archivoSalidaAdyacencia, delimiter=";")
        # inicia el resto de variables necesarias
        self.listaAdyacencia = []
        self.nodos = [["id", "label", "peso", "tipo", "error"]]
        self.id = 0

    def sondear(self):
        if platform.system() == "Linux":  # Si la plataforma es linux
            self.__rebuscar__("/")  # Se busca a partir del directorio raiz
            self.exportarDatos()
        elif platform.system() == "Windows":  # Si la plataforma es Windows
            for letter in char_range("A", "Z"):  # Se busca por todos los discos posibles
                ruta = letter + ":\\"
                if os.path.exists(ruta):
                    self.__rebuscar__(ruta)

            self.exportarDatos()
        else:  # Sino, pasa
            print("no implementado")

    def __rebuscar__(self, ruta):
        """
        Esta función toma la ruta de un directorio y añade a los csv los datos que va recopilando de manera
        recursiva
        :param ruta:
        :return:
        """
        nombredir = os.path.split(ruta)[1]  # Toma el nombre del directorio
        if nombredir == "found.000":  # todo revisar esto
            pass
        else:
            try:  # Si no da permission error
                os.chdir(ruta)
                while nombredir.endswith("\\"):  # Los nombres que terminan en \ dan error, por eso se quita
                    nombredir = nombredir[:-1]

                self.listaAdyacencia.append([self.id])
                idlocal = self.id  # Se almacena el id del directorio local
                pos = len(self.nodos)#Se almacena la posición para insertar ahí el directorio actual
                #Esto se hace para mantener los nodos como una lista ordenada

                for file in os.listdir(os.getcwd()):  # Por cada fichero en el directorio
                    self.id += 1  # Se aumenta el contador
                    self.__añadirAdyacencia__(idlocal,
                                              self.id)  # Se crea una relación entre el directorio local y el sub
                    dst = os.path.join(ruta, file)  # Se crea el path del directorio

                    if os.path.isdir(dst):  # Si es un directorio
                        self.__rebuscar__(dst)  # Se recursa
                    elif os.path.isfile(dst):  # Si es un fichero
                        # Se añade a los nodos
                        self.nodos.append([self.id, os.path.split(dst)[1], os.path.getsize(dst), "fil", True])
                self.nodos.insert(pos, [idlocal, nombredir, self.__calcularPesoDir1__(ruta,idlocal), self.__calcularPesoDir2__(ruta,idlocal),"dir", False])
            # Se coloca el directorio actual al final para poder sacar el peso de manera "auxiliada"
            except PermissionError:
                self.nodos.append([self.id, os.path.split(os.getcwd())[1], 0, "dir", True])

    def __añadirAdyacencia__(self, inicio, fin):
        """
        Añade en la lista de adyacencia un enlace de principio a fin
        :param inicio:
        :param fin:
        :return:
        """
        location = self.__busquedaBinaria__(inicio,self.listaAdyacencia)
        self.listaAdyacencia[location].append(fin)

    def __busquedaBinaria__(self, buscado, lista):
        """
        Bsuqueda binaria basandose en el elemento 0 de las listas que forman la lista introducida
        :param buscado:
        :param lista: lista de listas
        :return:
        """
        if len(lista) == 0:  # Comprueba si la lista está vacía
            return 0
        elif buscado == lista[0][0]:  # comprueba si el buscado es menor que el primero
            return 0
        elif buscado == lista[-1][0]:  # comprueba si el buscado es mayor que el último
            return len(lista) - 1
        else:  # Busca recursivamente
            return self.__bs__(buscado, 0, len(lista),lista)

    def __bs__(self, buscado, ini, fin, lista):
        """
        Función recursiva de busqueda binaria
        :param buscado:
        :param ini:
        :param fin:
        :param lista:
        :return:
        """
        mitad = (ini + fin) // 2
        vmitad = lista[mitad][0]
        if vmitad == buscado:
            return mitad
        elif vmitad > buscado:
            return self.__bs__(buscado, ini, mitad - 1, lista)
        elif vmitad < buscado:
            return self.__bs__(buscado, mitad + 1, fin, lista)

    def __calcularPesoDir1__(self, path,iddir, total=0):
        """
        Función que dado un directoria saca su peso
        :param path:
        :param total:
        :return:
        """
        # todo optimizar el cálculo del peso

        for id in self.listaAdyacencia[self.__busquedaBinaria__(iddir,self.listaAdyacencia)][1:]:
            elemento=self.nodos[self.__busquedaBinaria__(id,self.nodos)]
            peso=elemento[2]
            total+=peso
        return total


    def __calcularPesoDir2__(self, path, iddir, total=0):

        for file in os.listdir(path):  # por cada ficheros en el directorío
            try:  # Siempre que no haya ningún error
                file = os.path.join(path, file)
                if os.path.isdir(file):  # Si es un directorio se llama a la función
                    total += self.__calcularPesoDir__(file)  # Y se suma al peso actual
                elif os.path.isfile(file):  # Si es un fichero
                    total += os.path.getsize(file)  # Simplemente se suma su peso
            except PermissionError:
                pass
        return total

    def exportarDatos(self):
        """
        Función que escribe los datos a los csv
        :return:
        """
        self.escritorNodos.writerows(self.nodos)
        self.archivoSalidaNodos.flush()
        self.escritorAdyacencia.writerows(self.listaAdyacencia)
        self.archivoSalidaAdyacencia.flush()


s = Sonder()
# s.sondear()
s.__rebuscar__("G://")
s.exportarDatos()
