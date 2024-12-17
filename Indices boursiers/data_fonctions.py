import requests
import pandas as pd
from io import StringIO


def gsheet_Russel2000(url):
    """
    Charge un Google Sheet exporté en CSV depuis une URL et le retourne sous forme de DataFrame.

    Paramètres:
    - url (str): URL complète du fichier Google Sheet exporté en CSV.

    Retour:
    - DataFrame contenant les données du fichier CSV.

    Exceptions:
    - AssertionError pour les réponses HTTP non réussies.
    - Exception pour les erreurs de lecture CSV.
    """
    response = requests.get(url)
    if response.status_code == 200:
        return pd.read_csv(StringIO(response.text))
    else:
        raise AssertionError('Erreur HTTP avec le code de statut: {}'.format(response.status_code))


def obtenir_liste_entreprises(url, nom_indice):
    """
    Récupère la liste des entreprises d'un indice boursier spécifié depuis Wikipedia ou un Google Sheet.

    Paramètres :
    - url (str) : URL de la page Wikipedia ou du Google Sheet contenant la liste des entreprises de l'indice boursier.
    - nom_indice (str) : Nom de l'indice boursier ('Russell 2000', 'CAC 40', 'S&P 500', 'DAX').

    Retour :
    - DataFrame contenant la liste des entreprises pour l'indice boursier spécifié.
    """
    # Dictionnaire pour mapper les noms des indices aux indices de leurs tables sur Wikipedia
    index_table_map = {
        'CAC 40': 4,      # 5è tableau pour le CAC 40
        'S&P 500': 0,     # 1er tableau pour le S&P 500
        'DAX': 4,         # 5è tableau pour le DAX
        'FTSE MIB': 1,    # 2è tableay pour le FTSE MIB
        'FTSE 100': 4,
        'IBEX 35': 2
    }

    # Gestion spéciale pour le Russell 2000 via une fonction définie précédemment
    if nom_indice == 'Russell 2000':
        return gsheet_Russel2000(url)

    # Gestion des indices de Wikipedia
    if nom_indice in index_table_map:
        try:
            df = pd.read_html(url)[index_table_map[nom_indice]]
            return df
        except Exception as e:
            raise Exception(f"Une erreur s'est produite lors de la récupération des données depuis {url} : {e}")
    else:
        raise ValueError(f"Le nom de l'indice '{nom_indice}' n'est pas reconnu. Veuillez utiliser l'un des suivants : {list(index_table_map.keys()) + ['Russell 2000']}")
