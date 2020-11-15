#!/usr/bin/env python3
# -*- coding: <UTF-8> -*-
from timeit import default_timer as timer
import copy

"""
CURSO:2020/2021
ASIGNATURA: ESTRUCTURAS DE DATOS Y ALGORITMOS
GRUPO T1-X5
PRACTICA 1:Nombres más comunes 
@author:MIGUEL CHAVEINTE GARCIA
"""


class EDA:
    """
    Main en el cual pediremos los datos que necesitemos para llevar a cabo el programa al usuario
    y una vez con estos datos llamaremos a las funciones que nos permiten hacer las fases de
    filtrado,insercion 1 y 2, ordenamiento y seguimiento y posteriormente mostraremos los
    datos correspondientes por pantalla. Por último el usuario decide si ejecutar una nueva
    interacción.
    """

    def main(self):
        continuar = True
        while continuar:
            archivo = False
            # Comprobamos que el archivo que nos da el usuario se encuentra en la carpeta en la que
            # está nuestro codigo.
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
            nombre = input("Nombre del usuario(en mayúsculas): ")

            print("\n*** BUCLE DE CONSULTAS ***")
            fecha1 = input(
                "Introduzca la fecha de inicio de búsqueda(dd/mm/aa): ")
            inicio = self.traduce_fecha(fecha1)
            fecha2 = input(
                "Introduzca la fecha de fin de búsqueda(dd/mm/aa): ")
            fin = self.traduce_fecha(fecha2)

            # Inserción 1
            busqueda, m, comp_ins, movi_ins, timer_fil, timer_ins = self.filtrado(
                vector, inicio, fin)
            # Inserción 2
            segundo, timer_ins2, comp_ins2, movi_ins2 = self.insercion2(
                vector, inicio, fin)
            # Movimientos y comparaciones en un array de 1 elemento(su suma) para pasarlo
            # como parametro a ordenacion para que se actualice ya que si se pasa por variable
            # al ser una función recursiva perderiamos los valores de cada llamada.
            sum_movimientos = [0]
            sum_comparaciones = [0]
            timer_ext = timer()
            # Ordenación
            ordenado, movi_ext, comp_ext = self.ordenamiento(
                busqueda, len(busqueda), sum_movimientos, sum_comparaciones)
            timer_ext = timer()-timer_ext
            # Seguimiento
            posicion, timer_seg = self.busqueda_nom(ordenado, nombre)
            # Imprimir valores pedidos y seguimiento
            self.imprimir(ordenado, usuarios, posicion, nombre)
            print("*** RESULTADOS ***")
            print("m= ", m, " personas que cumplen las condiciones")
            print("p= ", len(busqueda), "nombres distintos")
            print("d= ", fin-inicio+1, "dias en el intervalo")
            # Impresion movimientos,comparaciones y tiempo de las fases
            self.procesos(len(vector), timer_fil, comp_ins, movi_ins,
                          timer_ins, comp_ins2, movi_ins2,
                          timer_ins2, comp_ext, movi_ext, timer_ext, timer_seg, posicion+1)
            pregunta = input("\n¿Continuar[S/N]? ")
            # Bucle de petición a usuario si quiere continuar el proceso con una nueva interacción
            # Si introduce una "S" o una "s" se ejecuta de nuevo el bucle
            if pregunta != "S" and pregunta != "s":
                continuar = False
                exit()
            print()

    def filtrado(self, vector, inicio, fin):
        """
        Funcion que nos filtra el conjunto total de personas del array principal obtenido
        del fichero, según la fecha de nacimiento de cada una de esas personas que deberá estar
        en el intervalo de fechas que indico el usuario. Si esa persona cumple esa característica
        llamamos a la función busqueda secuencial que nos almacenará a esa persona en una nueva lista
        o si ya otra persona con el mismo nombre se encontraba en ese nuevo array se le incrementará el campo nº de veces
        -Parámetros de entrada:
            vector: vector original con todas las personas del fichero
            inicio:fecha inicio  de la que contar (int) que nos ha introducido el usuario
            fin:fecha fin (int) que nos ha introducido el usuario
        -Returns:
            -validos:lista nuevo con las personas de nombre diferente que cumplen las características de fecha y almacenado también el número de apariciones
            -contador:personas que cumplen las condiciones aunque tengan nombre repetido en la lista
            -comparaciones: veces que hemos comparado un elemento del vector
            -movimientos:nº de movimientos realizados.
            -dt:tiempo de filtrado
            -dt1_sum:tiempo de insercion
        """
        validos = []
        contador = 0
        comparaciones = 0
        movimientos = 0
        dt = timer()
        dt1_sum = 0
        for i in range(0, len(vector)):
            nacimiento = vector[i].nac
            if nacimiento >= inicio and nacimiento <= fin:
                dt1 = timer()
                nombre = vector[i].nom
                contador += 1
                validos, comparaciones, movimientos, = self.busqueda_secuencial(
                    validos, nombre, comparaciones, movimientos)
                dt1 = timer()-dt1
                dt1_sum += dt1
        dt = timer()-dt-dt1_sum
        return validos, contador, comparaciones, movimientos, dt, dt1_sum

    def busqueda_secuencial(self, validos, nombre, comparaciones, movimientos):
        """
        Funcion que realiza la busqueda secuencial sobre la lista donde vamos a guardar los nombres diferentes de las personas que cumplen las condiciones y el nº de apariciones de esta.Su funcionamiento es dado una persona que cumple las condiciones realizamos una busqueda secuencial sobre la lista para ver si su nombre ya se encuentra en esta. Si es asi, el campo de nº de veces se incrementa uno, sino se inserta al final de la lista con el campo a uno.
        -Parametros de entrada:
            validos:lista sobre la que vamos a guarda dichos nombres y apariciones
            nombre: campo nombre de la persona que cumple las condiciones
            comparaciones:veces que hemos comparado un elemento del vector
            movimientos:nº de movimientos realizados
        -Returns:
            validos:lista actualizada
            comparaciones:actualizados
            movimientos:actualizados
        """
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
            new = [nombre, 1]
            validos.append(new)
        return validos, comparaciones, movimientos

    def insercion2(self, vector, inicio, fin):
        """
        Same as filtrado solo que llamando a busqueda binaria.
        """
        validos = []
        comparaciones = 0
        movimientos = 0
        dt = timer()
        for i in range(0, len(vector)):
            nacimiento = vector[i].nac
            if nacimiento >= inicio and nacimiento <= fin:
                nombre = vector[i].nom
                # Si el vector esta vacio le completamos con el nombre de la persona que cumple por primera vez la condicion y a 1 el nº de apariciones.
                if len(validos) == 0:
                    movimientos += 1
                    new = [vector[i].nom, 1]
                    validos.append(new)
                else:
                    validos, comparaciones, movimientos = self.busqueda_binaria(
                        validos, nombre, comparaciones, movimientos)
        dt = timer()-dt
        return validos, dt, movimientos, comparaciones

    def busqueda_binaria(self, validos, nombre, comparaciones, movimientos):
        """
        Funcion que implementa un algoritmo que tras una busqueda binaria encuentra la posición donde debemos introducir el nombre de la persona que cumple las condiciones, si ese nombre no se encuentra en la lista previamente;si fuera como en este último caso solo se incrementa el campo nº de apariciones.Una vez encuentra el lugar donde insertar(ordenado alfabeticamente la lista) llama a la función mover que nos hace "hueco" moviendonos una posicion a la derecha los elementos a la derecha del lugar donde vamos a insertar ese nuevo elemento.
        -Parametros de entrada:
            validos:lista sobre la que vamos a guarda dichos nombres y apariciones
            nombre: campo nombre de la persona que cumple las condiciones
            comparaciones:veces que hemos comparado un elemento del vector
            movimientos:nº de movimientos realizados
        -Returns:
            validos:lista actualizada
            comparaciones:actualizados
            movimientos:actualizados
        """
        inicio = 0
        fin = len(validos)
        while inicio <= fin:
            medio = int((inicio+fin)/2)
            comparaciones += 1
            if nombre == validos[medio][0]:
                movimientos += 1
                validos[medio][1] += 1
                return validos, movimientos, comparaciones
            elif nombre > validos[medio][0]:
                comparaciones += 1
                if (medio+1) >= len(validos):
                    movimientos += 1
                    new = [nombre, 1]
                    validos.append(new)
                    return validos, movimientos, comparaciones
                elif nombre < validos[medio+1][0]:
                    comparaciones += 1
                    movimientos = self.mover(
                        validos, medio+1, nombre, movimientos)
                    return validos, movimientos, comparaciones
                comparaciones += 1
                inicio = medio+1
            else:
                comparaciones += 1
                if (medio-1) < 0:
                    movimientos = self.mover(
                        validos, 0, nombre,  movimientos)
                    return validos, movimientos, comparaciones
                elif nombre > validos[medio-1][0]:
                    comparaciones += 1
                    movimientos = self.mover(
                        validos, medio, nombre, movimientos)
                    return validos, movimientos, comparaciones
                comparaciones += 1
                fin = medio-1
        return validos, movimientos, comparaciones

    def mover(self, validos, medio, nombre,  movimientos):
        """
        Función  que nos hace "hueco" moviendonos una posicion a la derecha los elementos a la derecha del lugar(medio) donde vamos a insertar ese nuevo elemento.
        -Parametros de entrada:
            validos:lista sobre la que vamos a guarda dichos nombres y apariciones
            medio:posicion indexeada donde introducir el nuevo nombre con nº de apariciones a 1
            nombre: campo nombre de la persona que cumple las condiciones
            movimientos:nº de movimientos realizados
        -Returns:
            movimientos:actualizados
        (Validos se actualiza)
        """
        new = ["", 0]
        validos.append(new)
        movimientos += 1
        for i in range(len(validos)-2, medio-1, -1):
            movimientos += 2
            temporal = copy.deepcopy(validos[i])
            validos[i+1] = temporal
        validos[medio][0] = nombre
        validos[medio][1] = 1
        movimientos += 2
        return movimientos

    def ordenamiento(self, busqueda, size, sum_movimientos, sum_comparaciones):
        """
        Implementacion de algoritmo de fusión para ordenar la lista validos por el nº de apariciones
        Parámetros de entrada:
            -busqueda:lista de personas validas que contiene nombres diferentes y cada uno de ellos el nº de apariciones
            -size:tamaño de busqueda
            -sum_movimientos:array que almacena la suma total de movimientos
            -sum_comparaciones:array que almacena la suma total de comparaciones
        Returns:
            -lista_nueva:lista busqueda ordenada por el nº de aparicioens de mayor a menor.
            -sum_movimientos:actualizado con la suma de movimientos de cada interaccion
            -sum_comparaciones :actualizado con la suma de comparaciones de cada interaccion
        """
        if len(busqueda) <= 1:
            return busqueda

        medio = int(len(busqueda) / 2)
        izquierda = busqueda[:medio]
        derecha = busqueda[medio:]

        izquierda = self.ordenamiento(
            izquierda, size, sum_movimientos, sum_comparaciones)
        derecha = self.ordenamiento(
            derecha, size, sum_movimientos, sum_comparaciones)

        lista_nueva, comparaciones, movimientos = self.merge(
            izquierda, derecha)
        sum_comparaciones[0] = comparaciones+sum_comparaciones[0]
        sum_movimientos[0] = movimientos+sum_movimientos[0]
        # Si la lista_nueva ha llegado a la misma longitud que la lista busqueda original,retorne
        # todos los valores,sino solo la lista nueva en construccion para una nueva interacción.
        if len(lista_nueva) == size:
            return lista_nueva, sum_movimientos[0], sum_comparaciones[0]
        return lista_nueva

    def merge(self, listaA, listaB):
        """
        Fusion en una lista nueva ordenada dadas dos listas.
        -Parámetros de entrada:
            listaA: lista izquierda algoritmo fusion
            listaB: lista derecha algoritmo fusion
        -Return:
            lista_nueva:fusion de las dos lista pero ordenado sus elementos.
            comparaciones:nº de comparaciones entre las listas
            movimientos:nº de movimientos que se realizan sobre las listas
        """
        comparaciones = 0
        movimientos = 0
        lista_nueva = []
        a = 0
        b = 0

        while a < len(listaA) and b < len(listaB):
            comparaciones += 1

            if listaA[a][1] < listaB[b][1]:
                lista_nueva.append(listaB[b])
                movimientos += 1
                b += 1
            else:
                lista_nueva.append(listaA[a])
                movimientos += 1
                a += 1

        while a < len(listaA):
            lista_nueva.append(listaA[a])
            movimientos += 1
            a += 1

        while b < len(listaB):
            lista_nueva.append(listaB[b])
            movimientos += 1
            b += 1

        return lista_nueva, comparaciones, movimientos

    def imprimir(self, busqueda, usuarios, posicion, nombre):
        """
        Funcion que imprime por pantalla los primeros n(variable usuarios) primeros usuarios y sus indices y su nº de aparicioens y además aquel cuyo nombre ha introducido el usuario con su indice y su nº de apariciones.
        -Parametros de entrada:
            busqueda:lista ordenada
            usuarios:numero n de usuarios a mostrar
            posicion:poscicion(index) donde se encuentra el nombre dado por el usuario
            nombre: nombre dado por el usuario a mostrar
        """
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
        """
        Funcion que recorre la lista busqueda ya ordenada hasta que encuentre que el nombre de uno es igual al que te dio el usuario.
        -Parametro de entrada:
            busqueda:lista ordenada
            nombre:nombre dado por el usuario para buscarlo en busqueda
        -Returns:
            posicion:index de la lista busqueda
            dt: tiempo seguimiento
        """
        dt = timer()
        posicion = len(busqueda)-1
        for i in range(len(busqueda)):
            if nombre == busqueda[i][0]:
                posicion = i
        dt = timer()-dt
        return posicion, dt

    def procesos(self, n, timer_fil, comp_ins, movi_ins, timer_ins, comp_ins2, movi_ins2, timer_ins2, comp_ext, movi_ext, timer_ext, timer_seg, posicion):
        """
        Funcion que imprime los resultados de comparaciones,movimientos y tiempo formateados de las diferentes fases del proceso.
        -Parámetros de entrada:
            n:comparaciones de filtrado
            timer_fil:tiempo filtrado
            comp_ins:comparaciones insercion 1
            movi_ins:movimientos insercion 1
            timer_ins:tiempo insercion 1
            comp_ins2:comparaciones insercion 2
            movi_ins2:movimientos insercion 2
            timer_ins2:tiempo insercion 2
            comp_ext:comparaciones insercion extracción
            movi_ext:movimientos extracción
            timer_ext:tiempo extracción
            timer_seg:tiempo seguimiento
            posicion:poscion elemento de nombre
        """
        print("{:14}{:1}{:>22}{:1}{:>22}{:1}{:>14}".format("FILTRADO",
                                                           "|", f"{n} comps ", "|", "0 movs ", "|", f"{timer_fil:.5} seg"))
        print("{:14}{:1}{:>22}{:1}{:>22}{:1}{:>14}".format("INSERCIÓN#1",
                                                           "|", f"{comp_ins} comps ", "|", f"{movi_ins} movs ", "|", f"{timer_ins:.5} seg"))
        print("{:14}{:1}{:>22}{:1}{:>22}{:1}{:>14}".format("INSERCIÓN#2",
                                                           "|", f"{comp_ins2} comps ", "|", f"{movi_ins2} movs ", "|", f"{timer_ins2:.5} seg"))
        print("{:14}{:1}{:>22}{:1}{:>22}{:1}{:>14}".format("EXTRACCIÓN",
                                                           "|", f"{comp_ext} comps ", "|", f"{movi_ext} movs ", "|", f"{timer_ext:.5} seg"))
        print("{:14}{:1}{:>22}{:1}{:>22}{:1}{:>14}".format("SEGUIMIENTO",
                                                           "|", f"{posicion} comps ", "|", "0 movs ", "|", f"{timer_seg:.5} seg"))

    def lee_fichero(self, nomfich):
        """
        Función que nos lee el fichero y nos almacena la persona leida por linea en una lista en la que se guardan los atributos dados por la clase persona.
        -Parametros de entrada:
            nomfich:nombre del fichero
        -Returns:
            res:vector que almacena todas las personas
        """
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
        """
        Funcion que covierte el string fecha en formato dd/mm/aa a un int que representa los dias transcurridos desde el 1 de enero de 1920 hasta la fecha txt
        -Parámetros de entrada:
            txt:String dd/mm/aa de fecha
        -Returns:
            El int de los dias transcurridos
        """
        f = list(map(int, txt.split('/')))
        return 367*f[2]-(7*(f[2]+5001+self.dc(f[1]-9, 7)))//4+(275*f[1])//9+f[0]-692561


class Persona:
    """
    Implementa la clase Persona formado por los atributos nac(nacimiento), fac(fallecimiento),gen(genero) y nom(nombre) mediante las dos lineas que recibe de cada persona del fichero.
    """

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
    # Programa principal.
    principal = EDA()
    principal.main()
