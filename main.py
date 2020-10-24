
class EDA:

    def main():
        print("hola mundo")

    def lee_fichero(nomfich):
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
        print(f'n = {n} personas en total.')
        return res

    def dc(a, b):
        return a//b if a >= 0 else -((-a)//b)

    def traduce_fecha(txt):
        f = list(map(int, txt.split('/')))
        return 367*f[2]-(7*(f[2]+5001+dc(f[1]-9, 7)))//4+(275*f[1])//9+f[0]-692561

    if __name__ == '__main__':
        main()
