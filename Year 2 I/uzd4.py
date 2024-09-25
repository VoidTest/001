def kustibas_virziens(kustiba):
    if kustiba.lower() in ['w']:
        return "Virziens: Uz augšu"
    elif kustiba.lower() in ['s']:
        return "Virziens: Uz leju"
    elif kustiba.lower() in ['a']:
        return "Virziens: Pa kreisi"
    elif kustiba.lower() in ['d']:
        return "Virziens: Pa labi"
    else:
        return "Nederīga kustība"

for i in range(4):
    kustiba = input(f"Ievadiet {i+1}. kustību: ")
    print(kustibas_virziens(kustiba))
