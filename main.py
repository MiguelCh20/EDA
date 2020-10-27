from timeit import default_timer as timer


class EDA:

    def main(self):
        archivo = False
        while archivo != True:
            try:
                cargar = input(
                    "Introduzca el nombre del fichero que desea cargar con la extension .txt: ")
                vector = []
                vector = self.lee_fichero(cargar)
                archivo = True
            except FileNotFoundError:
                print("Introduzca un archivo que exista")
        print("*** OPCIONES GENERALES ***")
        usuarios = int(input("Número de nombres a mostrar: "))
        nombre = input("Nombre del usuario: ")

        print("\n*** BUCLE DE CONSULTAS ***")
        fecha1 = input("Introduzca la fecha de inicio de búsqueda: ")
        inicio = self.traduce_fecha(fecha1)
        fecha2 = input("Introduzca la fecha de fin de búsqueda: ")
        fin = self.traduce_fecha(fecha2)

        busqueda = []
        busqueda = self.filtrado(vector, inicio, fin)
        self.ordenamiento(busqueda)
        posicion = self.busqueda_nom(busqueda, nombre)
        self.imprimir(busqueda,usuarios,posicion)

    def filtrado(self, vector, inicio, fin):
        validos = []
        for i in range(1, len(vector)):
            nacimiento = vector[i].nac
            if nacimiento >= inicio and nacimiento <= fin:
                nombre = vector[i].nom
                tamaño = len(validos)
                for j in range(0, tamaño, 1):
                    if nombre == validos[j][0]:
                        validos[j][1] = validos[j][1]+1
                        break
                new = [vector[i].nom, 1]
                validos.append(new)
        return validos

    def ordenamiento(self, busqueda):
        for i in range(len(busqueda)-1, 0, -1):
            for j in range(i):
                if busqueda[j][1] < busqueda[j+1][1]:
                    temporal = busqueda[j]
                    busqueda[j] = busqueda[j+1]
                    busqueda[j+1] = temporal
                    break

    def imprimir(self, busqueda, usuarios,posicion):
        print()
        for i in range(usuarios):
            print(f"\t{i+1}.{busqueda[i][0]}: {busqueda[i][1]}")
        print(f"\t{posicion+1}.{busqueda[posicion][0]}: {busqueda[posicion][1]}\n")

    def busqueda_nom(self, busqueda, nombre):
        for i in range(len(busqueda)):
            if nombre == busqueda[i][0]:
                return i
        return -1

    def lee_fichero(self, nomfich):
        res = []
        with open(nomfich) as f:
            n = int(f.readline())
            print("____|____|____|____|")
            lim = n/20
            dt = timer()
            for i in range(n):
                res.append(Persona(f.readline(), f.readline()))
                if i % lim == lim-1:
                    print("*", end="")
            dt = timer()-dt
            print(f'\nLectura fichero: {dt:.5} seg.')
            print(f'n = {n} personas en total. \n')
            return res

    def dc(self, a, b):
        return a//b if a >= 0 else -((-a)//b)

    def traduce_fecha(self, txt):
        f = list(map(int, txt.split('/')))
        return 367*f[2]-(7*(f[2]+5001+self.dc(f[1]-9, 7)))//4+(275*f[1])//9+f[0]-692561


class Persona:
    def __init__(self, lin1, lin2):
        self.nac = (ord(lin1[0])-48)*10000 + (ord(lin1[1])-48)*1000 + \
                   (ord(lin1[2])-48)*100 + (ord(lin1[3])-48)*10 + \
                   (ord(lin1[4])-48)
        self.fac = (ord(lin1[6])-48)*10000 + (ord(lin1[7])-48)*1000 + \
                   (ord(lin1[8])-48)*100 + (ord(lin1[9])-48)*10 + \
                   (ord(lin1[10])-48)
        self.gen = ord(lin1[12])-48
        self.nom = lin2[:-1]

    def __repr__(self):
        return f'nac: {self.nac}, fac: {self.fac}, gen: {self.gen}, nom: {self.nom}'


if __name__ == "__main__":
    principal = EDA()
    principal.main()
