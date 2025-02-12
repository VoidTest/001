# Nolasa tekstu no faila
with open("Programming2/teksta_vardu_skaititajs/teksts.txt", "r", encoding="utf-8") as f:
    teksts = f.read()

# Sadala tekstu vārdos (izmantojot tukšumus kā atdalītājus)
vardi = teksts.split()

# Saraksti visiem vārdiem un tikai tiem, kuri ir vismaz 4 burtu gari
all_words = []   # visi apstrādātie vārdi (jebkura garuma)
words_4 = []     # tikai vārdi ar vismaz 4 burtiem

# Definējam simbolu virkni, kuru vēlamies noņemt no vārdiem
puntuation = ".,!-?*'\"()"

for vards in vardi:
    # Noņemam nevajadzīgās zīmes sākumā un beigās un pārvēršam uz mazajiem burtiem
    clean_word = vards.strip(puntuation).lower()
    if clean_word:  # pievieno, ja vārds nav tukšs
        all_words.append(clean_word)
        if len(clean_word) >= 4:
            words_4.append(clean_word)

# Saskaita vārdu biežumu visu vārdu (jebkura garuma) sarakstā
freq_all = {}
for word in all_words:
    freq_all[word] = freq_all.get(word, 0) + 1

# Saskaita vārdu biežumu sarakstā ar vismaz 4 burtiem
freq_4 = {}
for word in words_4:
    freq_4[word] = freq_4.get(word, 0) + 1

# Sakārtojam vārdu biežumu sarakstu (ar vismaz 4 burtiem) dilstošā secībā
sorted_words_4 = sorted(freq_4.items(), key=lambda item: item[1], reverse=True)

print("5 biežāk lietotie vārdi (ar vismaz 4 burtiem):")
for word, freq in sorted_words_4[:5]:
    print(f"{word}: {freq}")

# Izvēlamies visbiežāk lietoto vārdu no visu vārdu kopas (jebkurā garumā)
sorted_all = sorted(freq_all.items(), key=lambda item: item[1], reverse=True)
if sorted_all:
    most_common_word, most_common_freq = sorted_all[0]
    print(f"\nVisbiežāk lietotais vārds (jebkurā garumā): {most_common_word} ar {most_common_freq} parādījumiem.")

# Bonus: Grupējam vārdus (ar vismaz 4 burtiem) pēc to pirmiem 4 burtiem
prefix_freq = {}
for word in words_4:
    prefix = word[:4]
    prefix_freq[prefix] = prefix_freq.get(prefix, 0) + 1

# Sakārtojam prefiksu sarakstu dilstošā secībā pēc biežuma
sorted_prefixes = sorted(prefix_freq.items(), key=lambda item: item[1], reverse=True)

print("\n5 biežāk sastopamie 4 burtu prefiksi:")
for prefix, freq in sorted_prefixes[:5]:
    print(f"{prefix}: {freq}")
