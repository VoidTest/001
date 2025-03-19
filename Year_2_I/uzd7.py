import random

def minet_slepto_skaitli():
    sleptais_skaitlis = random.randint(1, 10)
    minets = False

    while not minets:
        try:
            minetais_skaitlis = int(input("Uzminiet slēpto skaitli (1-10): "))
            
            if minetais_skaitlis < 1 or minetais_skaitlis > 10:
                print("Lūdzu, ievadiet skaitli diapazonā no 1 līdz 10.")
            elif minetais_skaitlis == sleptais_skaitlis:
                print("Apsveicam! Jūs uzminējāt pareizi!")
                minets = True
            else:
                print("Nepareizi, mēģiniet vēlreiz.")
        
        except ValueError:
            print("Lūdzu, ievadiet derīgu skaitli.")

minet_slepto_skaitli()