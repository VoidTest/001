import itertools
import string

def divu_burtu_kombinacijas():
    alfabets = string.ascii_lowercase
    
    kombinacijas = itertools.product(alfabets, repeat=2)

    print("Visas 2 burtu kombinācijas:")
    for kombinacija in kombinacijas:
        print(''.join(kombinacija))

divu_burtu_kombinacijas()
