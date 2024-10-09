import random  # Importē random moduli, lai nejauši izvēlētos vārdu spēlei.

# Funkcija, lai uzsāktu un pārvaldītu pakaramā spēli
def spēles_sākšana():
    global atjaunot_attēlojumu  # Izmanto globālo mainīgo, lai atiestatītu attēlojumu jaunai spēlei
    
    # Vārdu saraksts, no kura nejauši izvēlēties spēlei
    vārdu_saraksts = ["aardvark", "baboon", "camel", "jazz", "grass", "follow", "castle", "cloud"]
    
    # Nejauši izvēlas vārdu no vārdu saraksta un pārveido to par rakstzīmju sarakstu
    izvēlētais_vārds = random.choice(vārdu_saraksts)
    
    # Izveido tukšo (apakšsvītru) sarakstu katram izvēlētā vārda burtam
    tukšo_vietu_saraksts = ["_"] * len(izvēlētais_vārds)
    
    # Inicializē/atjaunina pakaramā attēlojuma pakāpi uz 0 (sākuma pakāpe)
    atjaunot_attēlojumu = 0
    
    # Saraksts, lai izsekotu burtus, ko spēlētājs ir minējis
    minētie_burti = []

    # Parāda sākotnējo pakaramā pakāpi un tukšo vārdu
    print(KARATAVU_ATTĒLI[atjaunot_attēlojumu])
    print("Laipni lūdzam pakaramo spēlē.")
    print(" ".join(tukšo_vietu_saraksts))  # Parāda tukšās vietas kā atstarpi atdalītu virkni

    # Galvenais spēles cikls, kas turpinās, līdz spēlētājs izdara 6 nepareizus minējumus
    while atjaunot_attēlojumu < 6:
        # Izsauc funkciju, lai apstrādātu spēlētāja minējumu
        # Ja minējuma_izteikšana atgriež False (spēlētājs minēja to pašu burtu), izlaiž pārējo ciklu
        if not minējuma_izteikšana(minētie_burti, izvēlētais_vārds, tukšo_vietu_saraksts):
            continue
        
        # Parāda pašreizējo pakaramā pakāpi un pašreizējo minētā vārda stāvokli
        print(KARATAVU_ATTĒLI[atjaunot_attēlojumu])
        print(" ".join(tukšo_vietu_saraksts))  # Parāda pašreizējo vārdu ar pareizi minētajiem burtiem
        
        # Parāda burtus, kurus spēlētājs līdz šim ir minējis
        print(f"Minētie burti: {', '.join(minētie_burti)}")
        
        # Ja spēlētājs ir minējis visus burtus pareizi, viņš uzvar un spēle beidzas
        if tukšo_vietu_saraksts == list(izvēlētais_vārds):
            print("TU UZVARI!")
            break

    # Ja spēlētājs sasniedz 6. nepareizo minējumu, spēle ir beigusies, un tiek atklāts pareizais vārds
    if atjaunot_attēlojumu == 6:
        print("SPĒLE BEIGTA.")
        print(f"Vārds bija: {izvēlētais_vārds}")

# Funkcija, kas apstrādā spēlētāja minējumu
def minējuma_izteikšana(minētie_burti, izvēlētais_vārds, tukšo_vietu_saraksts):
    global atjaunot_attēlojumu  # Izmanto globālo mainīgo, lai izsekotu nepareizo minējumu skaitu (pakaramā attēlošanai)
    
    pareizs_minējums = False  # Karodziņš, lai pārbaudītu, vai spēlētāja minējums ir pareizs.
    
    # Saņem spēlētāja minējumu un pārveido to par mazajiem burtiem, lai nodrošinātu nejutību pret reģistru
    minējums = input("Ievadi minējumu: ").lower()
    
    # Ja spēlētājs jau ir minējis šo burtu, informē un atgriež False (nav nepieciešams vēlreiz apstrādāt minējumu)
    if minējums in minētie_burti:
        print("Tu jau minēji šo burtu.")
        return False
    
    # Pievieno jauno minēto burtu sarakstam ar minētajiem burtiem
    minētie_burti.append(minējums)
    
    # Pārbaudi, vai minētais burts ir izvēlētajā vārdā
    for i, burts in enumerate(izvēlētais_vārds): # enumerate dod katram burtam sarakstā indexu jeb ciparu.
        if minējums == burts:  # Ja minētais burts ir atrasts
            tukšo_vietu_saraksts[i] = minējums  # Atjauno tukšo sarakstu (pareizo minējumu attēlojums) ar minēto burtu
            pareizs_minējums = True  # Iestata karodziņu uz True, jo minējums bija pareizs
    
    # Ja minētais burts nav vārdā, palielina pakaramā pakāpi (attēlojums)
    if not pareizs_minējums:
        print(f"Nav '{minējums}', atvainojamies.")
        atjaunot_attēlojumu += 1  # Palielina pakaramā pakāpi, ja minējums bija nepareizs
    
    return True  # Atgriež True, lai norādītu, ka minējums tika apstrādāts

# Funkcija, kas kontrolē spēles plūsmu un pārvalda vairākas spēles sesijas
def galvenais():
    spēles_sākšana()  # Sāk pirmo spēli
    
    # Pēc spēles beigām jautā spēlētājam, vai viņš vēlas spēlēt vēlreiz
    # Ja spēlētājs ievada 'y', spēle sākas no jauna
    while input("Vai vēlaties spēlēt vēlreiz? (y/n): ").lower() == 'y':
        spēles_sākšana()  # Sāk jaunu spēli, ja spēlētājs izvēlas spēlēt vēlreiz

# Pakaramā attēlu saraksts, lai parādītu dažādas pakaramā pakāpes (ja spēlētājs izdara nepareizu minējumu)
KARATAVU_ATTĒLI = [r'''  +---+
  |   |
      |
      |
      |
      |
=========''', r'''  +---+
  |   |
  O   |
      |
      |
      |
=========''', r'''  +---+
  |   |
  O   |
  |   |
      |
      |
=========''', r'''  +---+
  |   |
  O   |
 /|   |
      |
      |
=========''', r'''  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========''', r'''  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========''', r'''  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========''']

# Izpildi spēli, ja šis skripts tiek izpildīts (nevis importēts)
if __name__ == "__main__":
    galvenais()  # Sāk spēles ciklu
