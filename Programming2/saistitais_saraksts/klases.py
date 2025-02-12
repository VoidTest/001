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

    def add(self, jaunais, indekss=-1):
        if indekss == -1 or indekss >= self.skaits:
            if self.sakums is None:
                self.sakums = Node(jaunais)
            else:
                pedejais = self.sakums
                while pedejais.next:
                    pedejais = pedejais.next
                pedejais.next = Node(jaunais, pirms=pedejais)
        else:
            if indekss == 0:
                elements = Node(jaunais, pec=self.sakums)
                self.sakums.prev = elements
                self.sakums = elements
            else:
                aste = self.sakums
                for i in range(indekss):
                    aste = aste.next
                galva = aste.prev
                elements = Node(jaunais, pirms=galva, pec=aste)
                galva.next = elements
                aste.prev = elements
        self.skaits += 1

    def read(self, indekss=None):
        if indekss is None:
            if self.sakums is None:
                print("Saraksts ir tukšs!")
                return
            node = self.sakums
            while node:
                node.read()
                node = node.next
        else:
            if indekss < 0 or indekss >= self.skaits:
                print("Nepareizs indekss!")
                return
            node = self.sakums
            for i in range(indekss):
                node = node.next
            node.read()

    def pop(self, indekss=-1):
        if self.skaits == 0:
            print("Nav ko dzēst")
            return

        if indekss == -1:
            # Dzēš pēdējo elementu.
            if self.skaits == 1:
                self.sakums = None
            else:
                node = self.sakums
                while node.next:
                    node = node.next
                # Piesaista iepriekšējā mezgla next norāde kļūst par None.
                node.prev.next = None
            self.skaits -= 1
            return

        if indekss < 0 or indekss >= self.skaits:
            print("Nepareizs indekss!")
            return

        if indekss == 0:
            # Dzēš pirmo elementu.
            self.sakums = self.sakums.next
            if self.sakums:
                self.sakums.prev = None
            self.skaits -= 1
            return

        # Dzēš elementu vidū.
        node = self.sakums
        for i in range(indekss):
            node = node.next
        if node.prev:
            node.prev.next = node.next
        if node.next:
            node.next.prev = node.prev
        self.skaits -= 1

    def switch(self, i1, i2):
        if i1 < 0 or i1 >= self.skaits or i2 < 0 or i2 >= self.skaits:
            print("Nepareizs indekss!")
            return
        if i1 == i2:
            return

        node1 = self.sakums
        for i in range(i1):
            node1 = node1.next

        node2 = self.sakums
        for i in range(i2):
            node2 = node2.next

        # Apmainām to saturu
        node1.info, node2.info = node2.info, node1.info


# Piemēra izmantošana:

saraksts = List()
saraksts.add("Suns")         # Pievienojam "Suns" (pievienosies saraksta beigās)
saraksts.add("Kāja", 0)       # Pievienojam "Kāja" saraksta sākumā
saraksts.add("Māja", 1)       # Pievienojam "Māja" pozīcijā 1
saraksts.add(2)              # Pievienojam 2 saraksta beigās

print("Saraksta saturs:")
saraksts.read()              # Nolasām visu sarakstu

print("\nNolasīts elements ar indeksu 2:")
saraksts.read(2)             # Nolasām tikai trešo elementu

print("\nPēc pop() ar indeksu 1 (dzēšam otro elementu):")
saraksts.pop(1)
saraksts.read()

print("\nPēc switch(0, 1) (apmainām pirmo un otro elementu):")
saraksts.switch(0, 1)
saraksts.read()

print("\nPēc noklusējuma pop() (dzēšam pēdējo elementu):")
saraksts.pop()               # Noklusējuma gadījumā dzēš pēdējo elementu
saraksts.read()
