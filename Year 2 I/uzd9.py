def skaitit_burtus():
    vards = input("Ievadiet vārdu: ")
    burts = input("Ievadiet burtu: ")

    if len(burts) != 1:
        print("Lūdzu, ievadiet tikai vienu burtu.")
        return
    
    burta_skaits = vards.count(burts)
    print(f"Vārdā '{vards}' burts '{burts}' parādās {burta_skaits} reizes.")

skaitit_burtus()
