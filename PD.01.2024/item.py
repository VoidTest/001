class Item:
    def __init__(self, name, amount, type):
        self.name = name
        self.type = type
        self.amount = amount
        
    def addition(self):
        self.amount += 1
        
    def namechange(self, new_name=None):
        if new_name is None:
            new_name = input("Ievadi jauno vārdu: ")
        self.name = new_name
        
    def info(self):
        if self.type == "p":
            typename = "programmatura"
        elif self.type == "d":
            typename = "dators"
        else:
            typename = "NaN" 
        return f"sveiki, mani sauc {self.name}, mans dzimums ir {typename}, man ir {self.amount} gadi."

    def typechange(self):
        newtype = input("Ievadi jauno dzimumu ('v' vīrietis vai 's' sieviete): ").lower()
        self.type = newtype        
        
        self.info()
