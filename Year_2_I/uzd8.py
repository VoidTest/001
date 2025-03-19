def izvadit_dalosos_skaitlus():
    try:
        dalitajs = int(input("Ievadiet skaitli: "))
        
        print(f"Skaitļi no 1 līdz 1000, kas dalās ar {dalitajs}:")
        for skaitlis in range(1, 1001):
            if skaitlis % dalitajs == 0:
                print(skaitlis)
                
    except ValueError:
        print("Lūdzu, ievadiet derīgu skaitli.")

izvadit_dalosos_skaitlus()
