def check_age():
    birth_year = int(input("Ievadi savu dzimšanas gadu: "))
    age = 2024 - birth_year
    
    if age >= 18:
        print(f"Tev ir {age} gadi. Tu esi pilngadīgs/a.")
    else:
        print(f"Tev ir {age} gadi. Tu vēl neesi pilngadīgs/a.")

check_age()