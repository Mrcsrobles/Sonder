import csv
import platform
import os


class Sonder:

    def __init__(self):
        self.archivoSalidaNodos = open("salidaNodos.csv", "w", newline="", encoding="utf-8")
        self.escritorNodos = csv.writer(self.archivoSalidaNodos, delimiter=";")
        self.archivoSalidaAdyacencia = open("salidaAdyacencia.csv", "w", newline="", encoding="utf-8")
        self.escritorAdyacencia = csv.writer(self.archivoSalidaAdyacencia, delimiter=";")
        self.listaAdyacencia = []
        self.nodos = [["id", "label", "peso", "tipo", "error"]]
        self.id = 0

    def sondear(self):
        if platform.system() == "Linux":
            self.__rebuscar__("/")
            self.exportarDatos()
        elif platform.system() == "Windows":
            self.__rebuscar__("K:\\")
            self.exportarDatos()
        else:
            print("no implementado")

    def __rebuscar__(self, ruta):

        nombredir = os.path.split(ruta)[1]
        if nombredir == "found.000":
            pass
        else:
            try:
                os.chdir(ruta)

                while nombredir.endswith("\\"):
                    nombredir = nombredir[:-1]

                self.nodos.append([self.id, nombredir, self.__calcularPesoDir__(ruta), "dir", False])
                self.listaAdyacencia.append([self.id])
                idlocal = self.id

                for file in os.listdir(os.getcwd()):
                    self.id += 1
                    self.__añadirAdyacencia__(idlocal, self.id)
                    dst = os.path.join(ruta, file)

                    if os.path.isdir(dst):
                        self.__rebuscar__(dst)
                    elif os.path.isfile(dst):
                        self.nodos.append([self.id, os.path.split(dst)[1], os.path.getsize(dst), "fil", True])
            except PermissionError:
                self.nodos.append([self.id, os.path.split(os.getcwd())[1], 0, "dir", True])

    def __añadirAdyacencia__(self, inicio, fin):
        # todo optimizar la busqueda
        if inicio==0:
            print("aqui")
        for lista in self.listaAdyacencia:
            if lista[0] == inicio:
                lista.append(fin)
                break

    def __calcularPesoDir__(self,path,total=0):
        #todo optimizar el cálculo del peso
        for file in os.listdir(path):
            try:
                file=os.path.join(path,file)
                if os.path.isdir(file):
                    total+=self.__calcularPesoDir__(file)
                elif os.path.isfile(file):
                    total+=os.path.getsize(file)
            except PermissionError:
                pass
        return total

    def exportarDatos(self):
        self.escritorNodos.writerows(self.nodos)
        self.archivoSalidaNodos.flush()
        self.escritorAdyacencia.writerows(self.listaAdyacencia)
        self.archivoSalidaAdyacencia.flush()


print(os.listdir("K:\\"))
s = Sonder()
s.sondear()
s.exportarDatos()
