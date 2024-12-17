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


def update_dataframe_Russel(df):
    """
    Met à jour la colonne 'Market Cap' du DataFrame :
    - Si 'Market Cap' est NaN, remplace par les données de yfinance.
    - Sinon, supprime le symbole '$' de 'Market Cap',
             le convertit en float * million, puis en entier.

    Paramètres:
    - df (DataFrame): DataFrame contenant les données du Russel 2000 à mettre à jour.

    Retour:
    - DataFrame avec la colonne 'Market Cap' mise à jour.
    """
    for index, row in df.iterrows():
        if pd.isna(row['Market Cap']):
            ticker = row['Ticker']
            yf_ticker = yf.Ticker(ticker)
            market_cap = yf_ticker.info.get('marketCap')
            if market_cap:
                df.at[index, 'Market Cap'] = int(market_cap)
            else:
                print(f"Erreur lors de la récupération du Market Cap pour {ticker}.")
        else:
            market_cap_value = float(str(row['Market Cap']).replace('$', '').replace(',', '')) * 1e6
            df.at[index, 'Market Cap'] = int(market_cap_value)
    return df
