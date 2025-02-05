class Item:
    def __init__(self, name, amount, type, price, manufacturer):
        self.name = name
        self.type = type
        self.amount = amount
        self.price = price 
        self.manufacturer = manufacturer 
        
    def addition(self):
        self.amount += 1
        
    def namechange(self, new_name=None):
        if new_name is None:
            new_name = input("Ievadi jauno vārdu: ")
        self.name = new_name
        
    def info(self):
        if self.manufacturer:
            return f"Item: {self.name}, Amount: {self.amount}, Type: {self.type}, Manufacturer: {self.manufacturer}"
        else:
            return f"Item: {self.name}, Amount: {self.amount}, Type: {self.type}"

    def typechange(self):
        newtype = input("Ievadi jauno dzimumu ('v' vīrietis vai 's' sieviete): ").lower()
        self.type = newtype        
        
        self.info()
