import random
import string
import re

def generer_chaine_alea(taille=10):
    caracteres = string.ascii_letters + string.digits  # lettres + chiffres
    return ''.join(random.choice(caracteres) for _ in range(taille))


def sub_speciaux(texte) :
    # Garder seulement lettres (a-zA-Z), chiffres (0-9) et espaces
    resultat = re.sub(r'[^a-zA-Z0-9 ]', '', texte)
    
    return resultat

