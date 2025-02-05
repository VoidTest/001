class Node:
    def __init__(self, saturs, pirms=None, pec=None):
        self.info = saturs
        self.next = pec
        self.prev = pirms

    def read(self):
        print(self.info)


class List:
    def __init__(self):
        self.sakums = None
        self.skaits = 0
        return

    def add(self, jaunais, indekss = -1):
        if indekss == -1 or indekss >= self.skaits:
            if self.sakums == None:
                self.sakums = Node(jaunais)
            else:
                pedejais = self.sakums
                while pedejais.next:
                    pedejais = pedejais.next
                pedejais.next = Node(jaunais, pirms = pedejais)
        else:
            if indekss == 0:
                elements = Node(jaunais, pec = self.sakums)
                elements.next.prev = elements
                self.sakums = elements
            else:
                aste = self.sakums
                for i in range (indekss):
                    aste = aste.next
                galva = aste.prev
                elements = Node(jaunais, galva, aste)
                galva.next = elements
                aste.prev = elements
        self.skaits += 1
        return


    def read(self):
        if self.sakums == None:
            print("Saraksts ir tukšs!")
        esosais = self.sakums
        while esosais:
            esosais.read()
            esosais = esosais.next

    def pop(self):
        if self.skaits == 0:
            print("Nav ko dzēst")
            return
        if self.skaits == 1:
            self.sakums = None
            self.skaits = 0
            return
        primspedejais = self.sakums
        while primspedejais.next.next:
            primspedejais = primspedejais.next
        primspedejais.next = None
        self.skaits -= 1
        return


saraksts = List()
saraksts.read()
saraksts.add("Suns", 30)
saraksts.add("Kāja", 0)
saraksts.add("Māja", 25)
saraksts.add(2)

saraksts.read()
print("=====")
saraksts.sakums.next.next.next.prev.prev.prev.next.read()
    