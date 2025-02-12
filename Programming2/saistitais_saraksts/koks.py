class Node:
    def __init__(self, saturs, vecaks=None, mazais=None, lielais=None, limenis=0):
        self.info = saturs
        self.parent = vecaks
        self.smaller = mazais
        self.bigger = lielais
        self.level = limenis

    def read(self):
        print(f"dati: {self.info}, līmenis: {self.level}")


class Koks:
    def __init__(self):
        self.sakne = None

    def add(self, jaunais):
        if self.sakne is None:
            self.sakne = Node(jaunais, limenis=0)
        else:
            self._add_recursive(self.sakne, jaunais, 0)

    def _add_recursive(self, node, value, level):
        # Ja vērtība lielāka par pašreizējo, mēģina ievietot labajā apakškokā
        if value > node.info:
            if node.bigger is None:
                node.bigger = Node(value, vecaks=node, limenis=level + 1)
            else:
                self._add_recursive(node.bigger, value, level + 1)
        else:
            # Vērtība mazāka vai vienāda – kreisajā apakškokā
            if node.smaller is None:
                node.smaller = Node(value, vecaks=node, limenis=level + 1)
            else:
                self._add_recursive(node.smaller, value, level + 1)

    def read(self):
        if self.sakne is None:
            print("Kokā nav neviena elementa!")
        else:
            self._read_recursive(self.sakne)

    def _read_recursive(self, node):
        if node is None:
            return
        node.read()
        self._read_recursive(node.smaller)
        self._read_recursive(node.bigger)

    def sort(self):
        sorted_list = self._inorder_traverse(self.sakne)
        print("Elementi augošā secībā:")
        for item in sorted_list:
            print(item, end=" ")
        print()  # pāreja uz nākamo rindu pēc izdrukas
        return sorted_list

    def _inorder_traverse(self, node):
        if node is None:
            return []
        # Rekursīva in-orden traversēšana: kreisais apakškoks, pašreizējais, labais apakškoks
        return self._inorder_traverse(node.smaller) + [node.info] + self._inorder_traverse(node.bigger)

    def search(self, value):
        return self._search_recursive(self.sakne, value, 1)

    def _search_recursive(self, node, value, level):
        if node is None:
            return None  # vērtība nav atrasta
        if node.info == value:
            return level
        if value < node.info:
            return self._search_recursive(node.smaller, value, level + 1)
        else:
            return self._search_recursive(node.bigger, value, level + 1)


def koks_main():
    koks_inst = Koks()
    # Pievieno elementus kokam
    for value in [7505, 5643, 678, 2885, 6244, 4643, 7319, 8163, 2824, 8846,
                  1216, 8751, 8884, 3635, 1767, 9153, 3892, 883, 780, 6459,
                  4553, 5092, 4409, 9221, 947, 7382, 3285, 7482, 3006, 5769]:
        koks_inst.add(value)

    print("Koka elementi:")
    koks_inst.read()

    print("\nSorted numbers:")
    sorted_numbers = koks_inst.sort()
    print("Atgrieztais saraksts:", sorted_numbers)

    value_to_find = 9221
    level = koks_inst.search(value_to_find)
    if level is None:
        print(f"Vērtība {value_to_find} nav atrasta kokā.")
    else:
        # Ja saknes līmenis ir 1, tad apakškokiem līmenis tiek uzskatīts par (level - 1)
        print(f"Vērtība {value_to_find} ir atrasta {level - 1}. līmenī.")


koks_main()
