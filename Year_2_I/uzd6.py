
def izvadit_skaitlus():
    for skaitlis in range(1, 11):
        print(skaitlis)

while True:
    izvadit_skaitlus() 
    atkartot = input("Vai vēlaties atkārtot? (ja/ne): ").lower()
    if atkartot != 'ja':
        print("Programma pabeigta.")
        break
