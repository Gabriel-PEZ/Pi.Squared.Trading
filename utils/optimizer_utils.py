# utils/optimizer_utils.py

import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import yfinance as yf
import plotly.graph_objs as go
import plotly.express as px
import requests
import numpy as np

def calculate_portfolio_performance(tickers, weights, period='1y'):
    """
    Calcule les performances d'un portefeuille sur une période donnée.

    :param tickers: Liste des tickers des actifs.
    :param weights: Pondérations des actifs dans le portefeuille.
    :param period: Période pour télécharger les données (par défaut '1y').
    :return: Tuple (cumul des rendements du portefeuille, rendements journaliers du portefeuille).
    """
    # Téléchargement des prix ajustés des tickers
    data = yf.download(tickers, period=period)['Adj Close']

    # Gérer le cas où un seul ticker est fourni (data devient une série au lieu d'un DataFrame)
    if isinstance(data, pd.Series):
        data = data.to_frame()

    # Calcul des rendements journaliers
    returns = data.pct_change().dropna()

    # Calcul des rendements pondérés du portefeuille
    weighted_returns = returns.multiply(weights, axis=1)
    portfolio_returns = weighted_returns.sum(axis=1)  # Somme des rendements pondérés pour chaque jour

    # Calcul des rendements cumulés du portefeuille
    portfolio_cumulative = (1 + portfolio_returns).cumprod()

    return portfolio_cumulative, portfolio_returns

def get_risk_free_rate(api_key="f1f1a2d3abcf1f08e76d3bc4fc1efd19"):
    """
    Récupère le taux sans risque (rendement des obligations à 10 ans) depuis l'API FRED.

    Si une erreur survient, retourne un taux par défaut de 2 %.

    :param api_key: Clé API pour accéder à l'API FRED.
    :return: Taux sans risque sous forme de float (par exemple, 0.02 pour 2 %).
    """
    url = 'https://api.stlouisfed.org/fred/series/observations'
    params = {
        'series_id': 'DGS10',
        'api_key': api_key,
        'file_type': 'json',
        'sort_order': 'desc',
        'limit': 1
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Vérifie les erreurs HTTP
        data = response.json()
        # Retourne le premier taux disponible, converti en décimal
        return float(data['observations'][0]['value']) / 100
    except Exception:
        # Retourne un taux par défaut de 2 % en cas d'erreur
        return 0.02

def calculate_portfolio_metrics(weights, returns, cov_matrix, risk_free_rate):
    """
    Calcule les métriques d'un portefeuille : rendement attendu, volatilité et ratio de Sharpe.

    :param weights: Liste ou tableau des pondérations des actifs dans le portefeuille.
    :param returns: Liste ou tableau des rendements attendus des actifs.
    :param cov_matrix: Matrice de covariance des actifs.
    :param risk_free_rate: Taux sans risque (float).
    :return: Tuple (rendement attendu, volatilité, ratio de Sharpe).
    """
    weights = np.array(weights)  # Conversion en tableau NumPy
    portfolio_return = np.dot(returns, weights)  # Rendement attendu du portefeuille
    
    # Calcul de la variance et de la volatilité
    portfolio_variance = np.dot(weights, np.dot(cov_matrix, weights))
    portfolio_volatility = np.sqrt(portfolio_variance)

    # Calcul du ratio de Sharpe
    sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_volatility if portfolio_volatility else 0

    return portfolio_return, portfolio_volatility, sharpe_ratio

def simulate_portfolios(returns, cov_matrix, risk_free_rate, num_portfolios):
    """
    Génère des portefeuilles aléatoires pour simuler la frontière efficiente.

    :param returns: Liste ou tableau des rendements attendus des actifs.
    :param cov_matrix: Matrice de covariance des actifs.
    :param risk_free_rate: Taux sans risque (float).
    :param num_portfolios: Nombre de portefeuilles à simuler (int).
    :return: Tableau NumPy contenant les pondérations, rendements, volatilités et ratios de Sharpe pour chaque portefeuille.
    """
    num_assets = len(returns)
    results = np.zeros((num_portfolios, num_assets + 3))  # Colonnes : pondérations + métriques

    for i in range(num_portfolios):
        weights = np.random.random(num_assets)     # Génération de pondérations aléatoires
        weights /= weights.sum()                   # Normalisation à 1

        # Calcul des métriques pour le portefeuille
        portfolio_return, portfolio_volatility, sharpe_ratio = calculate_portfolio_metrics(
            weights, returns, cov_matrix, risk_free_rate
        )

        # Stockage des résultats
        results[i, :num_assets] = weights
        results[i, num_assets:] = portfolio_return, portfolio_volatility, sharpe_ratio

    return results

def plot_efficient_frontier(results, portfolio_weights, returns, cov_matrix):
    """
    Trace la frontière efficiente avec les portefeuilles simulés et le portefeuille actuel.

    :param results: Tableau des résultats des portefeuilles simulés (pondérations, rendements, volatilités, ratios de Sharpe).
    :param portfolio_weights: Pondérations du portefeuille actuel.
    :param returns: Rendements moyens des actifs (liste ou tableau).
    :param cov_matrix: Matrice de covariance des actifs.
    :return: Objet Plotly `Figure` contenant la visualisation.
    """
    # Création d'un DataFrame des portefeuilles simulés
    num_assets = len(portfolio_weights)
    columns = [f'Weight {i+1}' for i in range(num_assets)] + ['Return', 'Volatility', 'Sharpe Ratio']
    portfolios = pd.DataFrame(results, columns=columns)

    # Conversion des rendements et volatilités en pourcentages
    portfolios['Return'] *= 100
    portfolios['Volatility'] *= 100

    # Création du graphique pour les portefeuilles simulés
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=portfolios['Volatility'],  # Volatilité sur l'axe des X
        y=portfolios['Return'],      # Rendement sur l'axe des Y
        mode='markers',
        marker=dict(
            size=5,
            color=portfolios['Sharpe Ratio'],  # Couleur selon le ratio de Sharpe
            colorscale='Viridis',
            showscale=True
        ),
        text=portfolios['Sharpe Ratio'],  # Ratio de Sharpe en info-bulle
        name='Simulated Portfolios'
    ))

    # Calcul des métriques du portefeuille actuel
    portfolio_return, portfolio_volatility, _ = calculate_portfolio_metrics(
        portfolio_weights, 
        returns.mean(), 
        cov_matrix, 
        get_risk_free_rate()
    )

    # Ajout du portefeuille actuel au graphique
    fig.add_trace(go.Scatter(
        x=[portfolio_volatility * 100],  # Volatilité actuelle
        y=[portfolio_return * 100],      # Rendement actuel
        mode='markers',
        marker=dict(color='red', size=10),
        name='Current Portfolio'
    ))

    # Mise en forme du graphique
    fig.update_layout(
        title='Efficient Frontier with Current Portfolio',
        xaxis_title='Volatility (%)',
        yaxis_title='Expected Return (%)',
        legend_title='Portfolio Details',
        width=800,
        height=600
    )

    return fig