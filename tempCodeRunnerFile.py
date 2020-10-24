try:

                cargar = input("Introduzca el nombre del fichero que desea cargar con la extension .txt: ")

                lee_fichero(cargar)

                archivo = True

            except FileNotFoundError:

                print("Introduzca un archivo que exista")