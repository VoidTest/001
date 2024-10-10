class Human:
    def __init__(self, name, age, sex):
        self.name = name
        self.sex = sex
        self.age = age
        
    def birthday(self):
        self.age += 1
        
    def namechange(self, new_name=None):
        if new_name is None:
            new_name = input("Ievadi jauno vārdu: ")
        self.name = new_name
        
    def info(self):
        if self.sex == "s":
            sexname = "sieviete"
        elif self.sex == "v":
            sexname = "vīrietis"
        else:
            sexname = "TEST" 
        return f"sveiki, mani sauc {self.name}, mans dzimums ir {sexname}, man ir {self.age} gadi."

    def sexchange(self):
        newgender = input("Ievadi jauno dzimumu ('v' vīrietis vai 's' sieviete): ").lower()
        self.sex = newgender        
        
        self.info()
class Sieviete(Human):
    def __init__(self, name, age, hair_color):
        super().__init__(name, age, "s")
        self.__hair_color = hair_color
        # self.info()
    
    def info(self):
        super().info()
        # ("Mana matu krāsa ir", self.__hair_color)

# Example Usage
# persona = Human("Marta", 34, "s")
# print(persona.name, persona.age, persona.sex)

# person = Human("Aleksis", 17, "v")
# print(person.name, person.age, person.sex)

# person.birthday()
# print(person.age)
# person.info()
# person.namechange()
# person.sexchange()

# personn = Sieviete("Anna", 18, "Blonda")
