# Portfolio_optimizer.py

import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import yfinance as yf
import plotly.graph_objs as go
import plotly.express as px
import requests
import numpy as np

def main():
    
    #CSS pour ajuster la largeur de la zone de contenu
    st.markdown(
        """
        <style>
        div.block-container {
            max-width: 90%;
            margin: auto;
            padding: 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("Beta π² Trading")

    description = "Beta π² est l’espace innovant de π² Trading, conçu pour les investisseurs curieux d’explorer de nouvelles opportunités et maximiser leurs stratégies. Cette section propose un générateur aléatoire de portefeuilles, idéal pour tester des idées originales et audacieuses. L’utilisateur sélectionne un indice de référence, un intervalle pour le nombre de titres à inclure (par exemple, entre 15 et 20) et le nombre de simulations souhaitées. La plateforme génère alors des portefeuilles aux pondérations aléatoires et identifie celui ayant affiché les meilleures performances sur les cinq dernières années. Avec enthousiasme, π² Trading permet de récupérer les composantes du portefeuille gagnant et d’accéder aux données clés habituelles, comme dans les autres sections, pour des décisions stratégiques éclairées."

    justified_description = f"""
    <div style='text-align: justify; text-justify: inter-word;'>
        {description}
    </div>
    """
    st.markdown(justified_description, unsafe_allow_html=True)

    st.write("")

if __name__ == "__main__":
    main()