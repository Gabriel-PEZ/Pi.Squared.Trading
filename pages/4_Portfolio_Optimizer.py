# Portfolio_optimizer.py

import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import yfinance as yf
import plotly.graph_objs as go
import plotly.express as px
import requests
import numpy as np
from utils.graph_utils import plot_performance, plot_pie

# Fonction pour calculer la performance historique du portefeuille
def calculate_portfolio_performance(tickers, weights, period='1y'):
    data = yf.download(tickers, period=period)['Adj Close']
    if isinstance(data, pd.Series):  
        data = data.to_frame()  # CAS OU IL Y A UN SEUL TICKER 
    returns = data.pct_change().dropna()
    weighted_returns = returns.multiply(weights, axis=1)
    portfolio_returns = weighted_returns.sum(axis=1)
    portfolio_cumulative = (1 + portfolio_returns).cumprod()
    return portfolio_cumulative, portfolio_returns

# Fonction permettant de récupérer le taux sans risque (10-year Treasury yield, de la FRED API)
def get_risk_free_rate(api_key="f1f1a2d3abcf1f08e76d3bc4fc1efd19"):
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
        response.raise_for_status()
        data = response.json()
        # Convesion en décimal
        return float(data['observations'][0]['value']) / 100
    except Exception as e:
        st.error(f"Error fetching risk-free rate: {e}")
        # Taux sans risque = 2%, par défaut
        return 0.02

def calculate_portfolio_metrics(weights, returns, cov_matrix, risk_free_rate):
    """ Calculate portfolio expected return, volatility, and Sharpe ratio. """
    weights = np.array(weights)
    portfolio_return = np.dot(returns, weights)
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_volatility if portfolio_volatility else 0
    return portfolio_return, portfolio_volatility, sharpe_ratio

def simulate_portfolios(returns, cov_matrix, risk_free_rate, num_portfolios):
    """ Generate random portfolios to simulate the efficient frontier. """
    num_assets = len(returns)
    results = np.zeros((num_portfolios, num_assets + 3))
    for i in range(num_portfolios):
        weights = np.random.random(num_assets)
        weights /= np.sum(weights)
        portfolio_return, portfolio_volatility, sharpe_ratio = calculate_portfolio_metrics(weights, returns, cov_matrix, risk_free_rate)
        results[i][:num_assets] = weights
        results[i][num_assets:num_assets+3] = [portfolio_return, portfolio_volatility, sharpe_ratio]
    return results

def plot_efficient_frontier(results, portfolio_weights, returns, cov_matrix):
    # Création du dataframe des portefeuilles
    portfolios = pd.DataFrame(results, columns=[f'Weight {i+1}' for i in range(len(results[0])-3)] + ['Return', 'Volatility', 'Sharpe Ratio'])
    
    # Conversion en pourcentage
    portfolios['Return'] *= 100
    portfolios['Volatility'] *= 100

    # Ajout du graphique des portefeuilles simulés
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=portfolios['Volatility'], y=portfolios['Return'],
        mode='markers',
        marker=dict(size=5, color=portfolios['Sharpe Ratio'], colorscale='Viridis', showscale=True),
        text=portfolios['Sharpe Ratio']
    ))

    # Ajout du portefeuille actuel
    portfolio_return, portfolio_volatility, _ = calculate_portfolio_metrics(portfolio_weights, returns.mean(), cov_matrix, get_risk_free_rate())
    fig.add_trace(go.Scatter(
        x=[portfolio_volatility * 100],
        y=[portfolio_return * 100],
        mode='markers',
        marker=dict(color='red', size=10),
        name='Current Portfolio'
    ))

    # Mise à jour des layouts
    fig.update_layout(
        title='Efficient Frontier with Current Portfolio',
        xaxis_title='Volatility (%)',
        yaxis_title='Expected Return (%)',
        legend_title='Portfolio Details',
        width=800,
        height=600
    )
    return fig
def main():
    st.title("Portfolio optimizer")
    st.write("Optimisez votre portefeuille en ajustant les poids des actifs pour maximiser le rendement et minimiser le risque.")

    if 'portfolio' in st.session_state and not st.session_state['portfolio'].empty:
        data = st.session_state['portfolio']
        portfolio_df = data  

        st.write("### Portefeuille actuel :")

        fig_table = go.Figure(data=[go.Table(
            header=dict(
                values=list(data.columns),
                fill_color='#0611ab',
                font=dict(color='white', size=14),
                align='center',
                height=40
            ),
            cells=dict(
                values=[data.Actions, data["Nom de l'Entreprise"], data['Poids (%)']],
                fill_color=['#f8f9fa']*len(data),
                font=dict(color='black', size=12),
                align='center',
                height=30
            )
        )])
        fig_table.update_layout(
            width=600,
            height=200,
            margin=dict(l=0, r=0, t=40, b=0)
        )
        st.plotly_chart(fig_table, use_container_width=True, key="optimisation_portfolio_table")

        total_weight = data['Poids (%)'].sum()
        average_weight = data['Poids (%)'].mean()
        max_weight = data['Poids (%)'].max()
        min_weight = data['Poids (%)'].min()

        #Rendement attendu (annualisé)
        tickers = data['Actions'].tolist()
        weights = np.array(data['Poids (%)'].tolist()) / 100

 
        if len(tickers) > 0:
            try:
                portfolio_cumulative, portfolio_returns = calculate_portfolio_performance(
                    tickers,
                    weights,
                    period='1y'
                )
                expected_return = portfolio_returns.mean() * 252  #252 jours de bourse par an

                #Volatilité (annualisée)
                volatility = portfolio_returns.std() * np.sqrt(252)

                #Ratio de Sharpe (avec un taux sans risque de 2%)
                risk_free_rate = 0.02
                sharpe_ratio = (expected_return - risk_free_rate) / volatility if volatility != 0 else np.nan

                st.write("### Statistiques du Portefeuille")
                metrics_labels = [
                    "Poids Total", "Poids Moyen", "Poids Maximum", "Poids Minimum",
                    "Rendement Attendu", "Volatilité", "Ratio de Sharpe"
                ]
                metrics_values = [
                    f"{total_weight:.2f}%", f"{average_weight:.2f}%", f"{max_weight:.2f}%", f"{min_weight:.2f}%",
                    f"{expected_return*100:.2f}%", f"{volatility*100:.2f}%", f"{sharpe_ratio:.2f}"
                ]
                metrics_descriptions = [
                    "La somme des poids doit être de 100%.", "", "", "",
                    "Rendement attendu annualisé.", "Volatilité annualisée du portefeuille.",
                    "Ratio de Sharpe (rendement ajusté au risque)."
                ]

                num_metrics = len(metrics_labels)
                cols = st.columns(num_metrics)

                for col, label, value, description in zip(cols, metrics_labels, metrics_values, metrics_descriptions):
                    with col:
                        st.metric(label, value)
                        if description:
                            st.caption(description)

                graph_cols = st.columns(2)

                with graph_cols[0]:
                    st.write("### Performance Historique du Portefeuille")
                    plot_performance(portfolio_cumulative) #Module pour les deux graphiques

                with graph_cols[1]:
                    st.write("### Répartition des Poids dans le Portefeuille")
                    portfolio_df_sorted = portfolio_df.sort_values(by='Poids (%)', ascending=False)
                    plot_pie(portfolio_df_sorted)  

                st.session_state['portfolio'] = data
                #st.success("✅ Le portefeuille a été enregistré pour une utilisation ultérieure.")

            except ValueError as ve:
                st.error(f"Erreur lors du calcul des performances du portefeuille : {ve}")
            except Exception as e:
                st.error(f"Une erreur est survenue lors de l'optimisation : {e}")
            
        st.write("### Optimisation de votre portefeuille avec MPT")
        st.write("Optimisez votre portefeuille d'investissement sur la base de la théorie moderne du portefeuille (MPT).")
        st.write("*Note à l'utilisateur* : Par défaut, l'historique utilisé est celui des 10 dernières années.")

        # Ajout de la possibilité pour l'utilisateur de définir le nombre de simulations
        num_simulations = st.slider("Nb de Simulations Souhaitées", min_value=1000, max_value=20000, step=100)

        # Option pour le TsR
        st.write("Options pour le Taux sans Risque (r) :")
        use_api_rate = st.button("API FRED")
        no_use_api_rate = st.button("Input Manuel")

        if use_api_rate:
            risk_free_rate = get_risk_free_rate()
            st.write(f"Taux sans Risque actuel : *r* = {risk_free_rate:.3%}")
        if no_use_api_rate:
            risk_free_rate = st.number_input("Rentrer le Taux sans Risque (en %)", min_value=0.0, max_value=15.0, value=2.0, step=0.01) / 100.0

        data = st.session_state['portfolio']
        tickers = data['Actions'].tolist()
        weights = np.array(data['Poids (%)'].tolist()) / 100
        stock_data = yf.download(tickers, period='10y')['Adj Close']
        returns = stock_data.pct_change().mean() * 252
        cov_matrix = stock_data.pct_change().cov() * 252

        # Simuler les portefeuilles
        results = simulate_portfolios(returns, cov_matrix, risk_free_rate, num_simulations)
        fig = plot_efficient_frontier(results, weights, returns, cov_matrix)
        st.plotly_chart(fig)

    else:
        st.info("Veuillez créer un portefeuille dans la section **Création de Portefeuille** avant de procéder à l'optimisation.")

if __name__ == "__main__":
    main()
