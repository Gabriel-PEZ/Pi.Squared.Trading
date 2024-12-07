# Portfolio_optimizer.py

import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu  # Assurez-vous que streamlit_option_menu est installé
import yfinance as yf
import plotly.graph_objs as go
import plotly.express as px
import numpy as np  # type: ignore
from utils.graph_utils import plot_performance, plot_pie  # type: ignore

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
        else:
            st.info("Veuillez créer un portefeuille dans la section **Création de Portefeuille** avant de procéder à l'optimisation.")

if __name__ == "__main__":
    main()
