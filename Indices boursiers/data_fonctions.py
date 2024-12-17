import requests
import pandas as pd
from io import StringIO
import yfinance as yf


def load_google_sheet_csv_Russel(url):
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


def get_sp500_list(url):
    """
    Récupère la liste des entreprises du S&P 500 depuis Wikipedia.

    Paramètres:
    - url (str): URL de la page Wikipedia contenant la liste des entreprises du S&P 500.

    Retour:
    - DataFrame contenant la liste des entreprises du S&P 500.
    """
    return pd.read_html(url)[0]


def get_market_cap(symbol):
    """
    Récupère la capitalisation boursière d'une entreprise à partir de son symbole boursier.

    Paramètres:
    - symbol (str): Symbole boursier de l'entreprise.

    Retour:
    - marketCap (float): Capitalisation boursière de l'entreprise ou None si non trouvable.
    """
    try:
        stock = yf.Ticker(symbol)
        return stock.info['marketCap']
    except KeyError:
        return None


def update_symbols(df):
    """
    Met à jour les symboles spéciaux dans le DataFrame du S&P 500.

    Paramètres:
    - df (DataFrame): DataFrame du S&P 500 contenant les symboles à mettre à jour.

    Retour:
    - DataFrame avec les symboles mis à jour.
    """
    corrections = {
        60: 'BRK-B',
        75: 'BF-B'
    }
    for index, symbol in corrections.items():
        df.loc[index, 'Symbol'] = symbol
        df.loc[index, 'MarketCap'] = yf.Ticker(symbol).info['marketCap']
    return df
