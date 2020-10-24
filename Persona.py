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
        