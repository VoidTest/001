from test1 import Sieviete, Human

human_list = []

for i in range(20):
    human_list.append(Sieviete("Anna", "10", "Blonda"))

for sieviete in human_list:
    if sieviete.age % 2 == 0:
        sieviete.sexchange()

print("--------------------")
for sieviete in human_list:
    sieviete.info()