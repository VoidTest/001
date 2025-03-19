def kapinat_divi(n):
    return 2 ** n

try:
    n = int(input("Ievadiet skaitli n: "))
    rezultats = kapinat_divi(n)
    print(f"Skaitlis 2^{n} ir: {rezultats}")
except ValueError:
    print("Lūdzu, ievadiet derīgu skaitli.")
