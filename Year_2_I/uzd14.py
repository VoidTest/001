def lielakais_skaitlis(a, b, c):
    return max(a, b, c)

try:
    a = int(input("Ievadiet pirmo skaitli: "))
    b = int(input("Ievadiet otro skaitli: "))
    c = int(input("Ievadiet trešo skaitli: "))

    rezultats = lielakais_skaitlis(a, b, c)
    print(f"Lielākais skaitlis ir: {rezultats}")
except ValueError:
    print("Lūdzu, ievadiet derīgu skaitli.")
