def kvadrati_lidz_n(n):
    for i in range(1, n + 1):
        print(f"{i}^2 = {i**2}")

try:
    n = int(input("Ievadiet skaitli: "))

    kvadrati_lidz_n(n)
except ValueError:
    print("Lūdzu, ievadiet derīgu veselu skaitli.")
