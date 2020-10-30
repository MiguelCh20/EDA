from timeit import default_timer as timer
import copy


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
        busqueda, m, comp_ins, movi_ins, timer_fil, timer_ins = self.filtrado(
            vector, inicio, fin)
        segundo = []
        segundo = self.insercion2(vector, inicio, fin)
        print(segundo[0], segundo[1], segundo[-1], segundo[-2])
        movi_ext, comp_ext, timer_ext = self.ordenamiento(busqueda)
        posicion = self.busqueda_nom(busqueda, nombre)
        self.imprimir(busqueda, usuarios, posicion, nombre)
        print("*** RESULTADOS ***")
        print("m= ", m, " personas que cumplen las condiciones")
        print("p= ", len(busqueda), "nombres distintos")
        print("d= ", fin-inicio, "dias en el intervalo")
        timer_seg = 0  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.procesos(len(vector), timer_fil, comp_ins, movi_ins,
                      timer_ins, comp_ext, movi_ext, timer_ext, timer_seg)

    def filtrado(self, vector, inicio, fin):
        validos = []
        contador = 0
        comparaciones = 0
        movimientos = 0
        dt = timer()
        dt1 = 0
        for i in range(0, len(vector)):
            nacimiento = vector[i].nac
            if nacimiento >= inicio and nacimiento <= fin:
                nombre = vector[i].nom
                contador += 1
                contador_j = 0
                for j in range(len(validos)):
                    contador_j += 1
                    comparaciones += 1
                    if nombre == validos[j][0]:
                        movimientos += 1
                        validos[j][1] = validos[j][1]+1
                        break
                if len(validos) == 0 or contador_j == (len(validos)) and nombre != validos[contador_j-1][0]:
                    comparaciones += 1
                    movimientos += 1
                    new = [vector[i].nom, 1]
                    validos.append(new)
                dt1 = timer()-dt
        dt = timer()-dt
        return validos, contador, comparaciones, movimientos, dt, dt1

    def insercion2(self, vector, inicio, fin):
        validos = []
        contador = 0
        comparaciones = 0
        movimientos = 0
        dt = timer()
        dt1 = 0
        for i in range(0, len(vector)):
            nacimiento = vector[i].nac
            if nacimiento >= inicio and nacimiento <= fin:
                nombre = vector[i].nom
                contador += 1
                contador_j = 0
                if len(validos) == 0:
                    new = [vector[i].nom, 1]
                    validos.append(new)
                else:
                    validos = self.busqueda_binaria(vector, validos, nombre)
        return validos

    def busqueda_binaria(self, vector, validos, nombre):
        inicio = 0
        fin = len(validos)
        while inicio <= fin:
            medio = int((inicio+fin)/2)
            if nombre == validos[medio][0]:
                validos[medio][1] += 1
                return validos
            elif nombre > validos[medio][0]:
                if (medio+1) >= len(validos):
                    new = [nombre, 1]
                    validos.append(new)
                    return validos
                elif nombre < validos[medio+1][0]:
                    self.mover(validos, medio+1, nombre)
                    return validos
                inicio = medio+1
            else:
                if (medio-1) < 0:
                    self.mover(validos, 0, nombre)
                    return validos
                elif nombre > validos[medio-1][0]:
                    self.mover(validos, medio, nombre)
                    return validos
                fin = medio-1
        return validos

    def mover(self, validos, medio, nombre):
        temporal = copy.deepcopy(validos[medio])
        validos[medio][0] = nombre
        validos[medio][1] = 1
        validos.append(temporal)
        while validos[medio+1] != temporal:
            temporal2 = validos[medio+1]
            validos.remove(validos[medio+1])
            validos.append(temporal2)

    def ordenamiento(self, busqueda):
        comparaciones = 0
        movimientos = 0
        dt = timer()
        for i in range(len(busqueda)-1, 0, -1):
            for j in range(i):
                comparaciones += 1
                if busqueda[j][1] < busqueda[j+1][1]:
                    temporal = busqueda[j]
                    busqueda[j] = busqueda[j+1]
                    busqueda[j+1] = temporal
                    movimientos += 3
        dt = timer()-dt
        return movimientos, comparaciones, dt

    def imprimir(self, busqueda, usuarios, posicion, nombre):
        print()
        for i in range(usuarios):
            print(f"\t{i+1}.{busqueda[i][0]}: {busqueda[i][1]}")
        if posicion != -1:
            print(
                f"\t{posicion+1}.{busqueda[posicion][0]}: {busqueda[posicion][1]}\n")
        else:
            print(
                f"\n\tEl nombre introducido({nombre}) no se encuentra en ese rango de fechas\n")

    def busqueda_nom(self, busqueda, nombre):
        for i in range(len(busqueda)):
            if nombre == busqueda[i][0]:
                return i
        return -1

    def procesos(self, n, timer_fil, comp_ins, movi_ins, timer_ins, comp_ext, movi_ext, timer_ext, timer_seg):
        print("{:14}{:1}{:>22}{:1}{:>22}{:1}{:>14}".format("FILTRADO",
                                                           "|", f"{n} comps", "|", "0 movs", "|", f"{timer_fil:.5} seg"))
        # AÑADIR EL RESTO

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
