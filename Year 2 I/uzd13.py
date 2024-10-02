import random
import itertools
import string

def greet_user():
    vards = input("Mans vards ir: ")
    patik = input("Man patik: ")
    print(f"Mani sauc {vards} un man patik {patik}")

def calculate_vat():
    pvn = 21
    summa = int(input("Cenas summa: "))
    print(f"Summa ir {(summa / 100) * (100 + pvn)}")

def check_age():
    birth_year = int(input("Ievadi savu dzimšanas gadu: "))
    age = 2024 - birth_year
    if age >= 18:
        print(f"Tev ir {age} gadi. Tu esi pilngadīgs/a.")
    else:
        print(f"Tev ir {age} gadi. Tu vēl neesi pilngadīgs/a.")

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

def movement_loop():
    for i in range(4):
        kustiba = input(f"Ievadiet {i + 1}. kustību: ")
        print(kustibas_virziens(kustiba))

def print_numbers():
    for skaitlis in range(1, 1001):
        print(skaitlis)

def izvadit_skaitlus():
    while True:
        for skaitlis in range(1, 11):
            print(skaitlis)
        atkartot = input("Vai vēlaties atkārtot? (ja/ne): ").lower()
        if atkartot != 'ja':
            print("Programma pabeigta.")
            break

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

def izvadit_dalosos_skaitlus():
    try:
        dalitajs = int(input("Ievadiet skaitli: "))
        print(f"Skaitļi no 1 līdz 1000, kas dalās ar {dalitajs}:")
        for skaitlis in range(1, 1001):
            if skaitlis % dalitajs == 0:
                print(skaitlis)
    except ValueError:
        print("Lūdzu, ievadiet derīgu skaitli.")

def skaitit_burtus():
    vards = input("Ievadiet vārdu: ")
    burts = input("Ievadiet burtu: ")
    
    if len(burts) != 1:
        print("Lūdzu, ievadiet tikai vienu burtu.")
        return
    
    burta_skaits = vards.count(burts)
    print(f"Vārdā '{vards}' burts '{burts}' parādās {burta_skaits} reizes.")

def divu_burtu_kombinacijas():
    alfabets = string.ascii_lowercase
    kombinacijas = itertools.product(alfabets, repeat=2)
    print("Visas 2 burtu kombinācijas:")
    for kombinacija in kombinacijas:
        print(''.join(kombinacija))

def kapinat_divi(n):
    return 2 ** n

# Task 1: Sum of multiples of 3 or 5 below 1000
def sum_of_multiples():
    sum_of_multiples = sum(x for x in range(1000) if x % 3 == 0 or x % 5 == 0)
    print(f"Sum of multiples of 3 or 5 below 1000 is: {sum_of_multiples}")

# Task 2: Sum of even Fibonacci numbers below 4 million
def sum_even_fibonacci():
    a, b = 1, 2
    even_sum = 0

    while a <= 4000000:
        if a % 2 == 0:
            even_sum += a
        a, b = b, a + b

    print(f"Sum of even Fibonacci numbers below 4 million is: {even_sum}")

def main():
    greet_user()
    calculate_vat()
    check_age()
    movement_loop()
    print_numbers()
    izvadit_skaitlus()
    minet_slepto_skaitli()
    izvadit_dalosos_skaitlus()
    skaitit_burtus()
    divu_burtu_kombinacijas()

    try:
        n = int(input("Ievadiet skaitli n: "))
        rezultats = kapinat_divi(n)
        print(f"Skaitlis 2^{n} ir: {rezultats}")
    except ValueError:
        print("Lūdzu, ievadiet derīgu skaitli.")

    # Call the two new functions
    sum_of_multiples()
    sum_even_fibonacci()

if __name__ == "__main__":
    main()
