import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
from plotly import graph_objects as go
import plotly.express as px

# Charger les DataFrames préconstruits pour les indices boursiers
df_dax = pd.read_csv("/home/onyxia/work/Pi.Squared.Trading/Indices boursiers/dax_40.csv")
df_cac = pd.read_csv("/home/onyxia/work/Pi.Squared.Trading/Indices boursiers/cac_40.csv")
df_snp = pd.read_csv("/home/onyxia/work/Pi.Squared.Trading/Indices boursiers/snp_500.csv")

# DataFrames pour les indices boursiers
dataframes = {
    "United States": df_snp,
    "France": df_cac,
    "Germany": df_dax
}

# Charger les données géographiques pour la carte des indices
df_geo = px.data.gapminder()

# Fonction pour récupérer les données boursières et gérer les erreurs
def fetch_stock_data(tickers, start_date):
    stock_data = {}
    invalid_tickers = []
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(start=start_date)['Close']
            if hist.empty:
                invalid_tickers.append(ticker)
            else:
                stock_data[ticker] = hist
        except Exception:
            invalid_tickers.append(ticker)
    return pd.DataFrame(stock_data), invalid_tickers

# Fonction pour calculer la performance du portefeuille en pourcentage
def calculate_portfolio_performance(data, weights):
    normalized_data = data / data.iloc[0] * 100  # Normalisation des données
    portfolio_performance = (normalized_data * weights).sum(axis=1)  # Performance totale du portefeuille
    return portfolio_performance

def info_ticker(ticker):
    try:
        ticker_info = yf.Ticker(ticker).info
        return ticker_info
    except Exception as e:
        st.error("Erreur lors de la récupération des informations. Veuillez vérifier le ticker.")
        return None

# Fonction pour afficher les informations du ticker de manière structurée
def display_ticker_info(ticker_info):
    st.markdown("<h3 style='text-align: center;'>Informations de l'action</h3>", unsafe_allow_html=True)
    if ticker_info:
        st.write(f"**Nom complet**: {ticker_info.get('longName', 'N/A')}")
        st.write(f"**Prix actuel**: {ticker_info.get('currentPrice', 'N/A')} {ticker_info.get('currency', '')}")
        st.write(f"**Capitalisation boursière**: {ticker_info.get('marketCap', 'N/A')}")
        st.write(f"**Bêta (5 ans)**: {ticker_info.get('beta', 'N/A')}")
        st.write(f"**Dividende et rendement**: {ticker_info.get('dividendYield', 'N/A')}")
        st.write(f"**Date de bénéfices**: {ticker_info.get('earningsDate', 'N/A')}")
        st.write(f"**Secteur**: {ticker_info.get('sector', 'N/A')}")
        st.write(f"**Industrie**: {ticker_info.get('industry', 'N/A')}")
        st.write(f"**Site Web**: {ticker_info.get('website', 'N/A')}")

# Fonction pour afficher le graphique des cours de l'action avec Plotly
def display_stock_chart(ticker, start_date):
    stock = yf.Ticker(ticker)
    hist = stock.history(start=start_date)
    if hist.empty:
        st.warning("Pas de données de cours disponibles pour cette période.")
    else:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], mode='lines', name='Cours de clôture'))
        fig.update_layout(
            title=f"Cours de l'action {ticker}",
            xaxis_title="Date",
            yaxis_title="Prix de clôture",
            height=450,  # Hauteur du graphique ajustée
            width=700,   # Largeur du graphique ajustée
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)

def plot_index_chart(country):
    # Dictionnaire associant chaque pays à son ticker et à son nom d'indice
    tickers = {
        "France": {"ticker": "^FCHI", "name": "CAC 40"},  # CAC 40
        "United States": {"ticker": "^GSPC", "name": "S&P 500"},  # S&P 500
        "Germany": {"ticker": "^GDAXI", "name": "DAX"}  # DAX
    }
    
    country_data = tickers.get(country)
    if country_data:
        ticker = country_data["ticker"]
        index_name = country_data["name"]
        
        # Télécharger les données sur un an
        data = yf.download(ticker, period="1y")
        
        # Titre global avec le nom de l'indice
        st.title(f"Cours de l'indice {index_name}")

        # Afficher le graphique
        plt.figure(figsize=(10, 6))
        plt.plot(data.index, data['Close'], label=f"{index_name}", color="blue")
        plt.title(f"Cours de l'indice {index_name} sur la dernière année")
        plt.xlabel("Date")
        plt.ylabel("Cours de clôture")
        plt.legend()
        plt.grid(True)
        st.pyplot(plt)
    else:
        st.write("Aucun indice disponible pour ce pays.")

# Créer un menu horizontal avec des icônes
selected = option_menu(
    menu_title=None,
    options=["Page d'accueil", "Création du portefeuille", "Recherche", "Carte des indices", "Optimisation", "Pricing"],
    icons=["house", "book", "search", "globe", "briefcase", "heart"],
    menu_icon="cast", 
    default_index=0, 
    orientation="horizontal",
)

# Contenu des différentes pages
if selected == "Page d'accueil":
    # Page de présentation
    st.title("Bienvenue sur π² Trading")
    st.subheader("Optimisation Intelligente de Portefeuille")

    # Brève description
    st.write("""
    π² Trading est une plateforme intuitive qui vous aide à créer, analyser et optimiser vos portefeuilles financiers. 
    Découvrez comment maximiser vos investissements avec des outils avancés d’analyse et de gestion des risques.
    """)

    # Caractéristiques principales avec des colonnes pour chaque fonctionnalité
    st.write("### Caractéristiques principales")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.image("/home/onyxia/work/Pi.Squared.Trading/images_sites/creation_portefeuille.png", width=100)
        st.write("**Création de portefeuille**")
        st.write("Personnalisez et suivez la performance de votre portefeuille.")

    with col2:
        st.image("/home/onyxia/work/Pi.Squared.Trading/images_sites/map.png", width=100)
        st.write("**Carte des indices**")
        st.write("Explorez les indices boursiers à travers le monde.")

    with col3:
        st.image("/home/onyxia/work/Pi.Squared.Trading/images_sites/optimization.png", width=100)
        st.write("**Optimisation**")
        st.write("Maximisez vos gains avec des stratégies optimisées.")

    with col4:
        st.image("/home/onyxia/work/Pi.Squared.Trading/images_sites/pricing.png", width=100)
        st.write("**Pricing**")
        st.write("Évaluez vos produits financiers et analysez leur performance.")

    # Appel à l'action
    st.write("### Prêt à commencer ?")
    if st.button("Optimisez votre portefeuille dès maintenant"):
        selected = "Création du portefeuille"  # Redirection vers l'onglet "Création du portefeuille"

elif selected == "Création du portefeuille":
    st.title("Création de portefeuille")

    # Étape 1 : Saisie des tickers et des poids
    st.sidebar.header("Configuration du portefeuille")
    st.sidebar.write("Ajoutez les tickers d'actions et leurs poids ci-dessous (par exemple : AAPL, MSFT, GOOGL)")

    tickers = []
    weights = []

    # Permettre à l'utilisateur de saisir plusieurs tickers et les poids correspondants
    num_stocks = st.sidebar.number_input("Combien d'actions souhaitez-vous dans votre portefeuille ?", min_value=1, max_value=20, value=3)

    for i in range(num_stocks):
        ticker = st.sidebar.text_input(f"Action {i+1} :", value="", key=f"ticker_{i}")
        tickers.append(ticker.upper())
        weight = st.sidebar.number_input(f"Poids pour {ticker} (par ex. 0.5 pour 50%) :", min_value=0.0, max_value=1.0, value=0.2, key=f"weight_{i}")
        weights.append(weight)

    # S'assurer que la somme des poids fait 1
    total_weight = sum(weights)

    # Étape 2 : Sélectionner la date de début d'investissement
    start_date = st.sidebar.date_input("Date de début :", pd.to_datetime("2024-01-01"))

    # Affichage du tableau récapitulatif du portefeuille
    st.subheader("Aperçu du portefeuille")
    portfolio_data = pd.DataFrame({
        "Action": tickers,
        "Poids": weights
    })
    st.table(portfolio_data)

    if total_weight != 1.0:
        st.sidebar.error(f"Erreur : La somme des poids doit être égale à 1. Somme actuelle : {total_weight:.2f}")
    else:
        # Récupérer les données des actions et traiter les tickers invalides
        stock_data, invalid_tickers = fetch_stock_data(tickers, start_date)

        if invalid_tickers:
            st.error(f"Tickers invalides : {', '.join(invalid_tickers)}. Veuillez vérifier les symboles.")
        elif not stock_data.empty:
            # Calcul de la performance du portefeuille
            portfolio_performance = calculate_portfolio_performance(stock_data, weights)

            # Afficher la performance du portefeuille sous forme de graphique
            st.subheader("Performance du portefeuille (en %)")
            plt.figure(figsize=(10, 6))
            plt.plot(portfolio_performance.index, portfolio_performance, label="Performance du portefeuille", color="blue")
            plt.title("Performance du portefeuille dans le temps")
            plt.xlabel("Date")
            plt.ylabel("Valeur du portefeuille (%)")
            plt.grid(True)
            st.pyplot(plt)
        else:
            st.error("Aucune donnée trouvée pour les tickers ou la date de début sélectionnée.")

elif selected == "Recherche":
    st.title("Recherche d'une action")
    
    # Champ de saisie pour entrer le ticker
    ticker = st.text_input("Entrez le ticker de l'action (ex: TSLA pour Tesla) :")
    
    # Sélection de la date de début pour le graphique des cours
    start_date = st.date_input("Sélectionnez la date de début pour le graphique :", pd.to_datetime("2023-01-01"))
    
    # Vérifier que le ticker est saisi
    if ticker:
        # Mise en page avec deux colonnes, graphique à gauche et informations à droite
        col1, col2 = st.columns([3, 2])  # Ajuste les proportions pour équilibrer l'espace
        
        # Afficher le graphique du cours de l'action dans la première colonne
        with col1:
            st.markdown("<h3 style='text-align: center;'>Graphique du cours de l'action</h3>", unsafe_allow_html=True)
            display_stock_chart(ticker, start_date)
        
        # Afficher les informations du ticker dans la deuxième colonne
        with col2:
            ticker_info = info_ticker(ticker)
            if ticker_info:
                display_ticker_info(ticker_info)
            else:
                st.write("Aucune information disponible pour ce ticker.")

elif selected == "Carte des indices":
    st.title("Carte des indices boursiers par pays")

    # Champ de recherche pour filtrer les pays
    search_value = st.text_input("Rechercher un pays", "")

    # Créer et afficher la carte du monde avec les indices boursiers
    fig = px.choropleth(df_geo, locations="iso_alpha", hover_name="country",
                        projection="natural earth", color_continuous_scale=["#003f5c", "#58508d", "#bc5090", "#ff6361", "#ffa600"],
                        title="Carte des indices boursiers par pays")
    fig.update_layout(
        margin={"r": 0, "t": 50, "l": 0, "b": 0},
        geo=dict(showframe=False, showcoastlines=False, projection_type='natural earth',
                 landcolor="lightgray", oceancolor="lightblue", showocean=True, bgcolor='rgb(20, 24, 54)'),
        title_font_color='white', paper_bgcolor='rgb(20, 24, 54)', plot_bgcolor='rgb(20, 24, 54)', font_color='white'
    )
    st.plotly_chart(fig)

    # Si l'utilisateur entre un nom de pays, afficher le DataFrame et le graphique de l'indice
    if search_value:
        filtered_df = df_geo[df_geo['country'].str.contains(search_value, case=False)]
        if not filtered_df.empty:
            country_name = filtered_df['country'].values[0]
            st.write(f"**Pays sélectionné : {country_name}**")
            if country_name in dataframes:
                df_selected = dataframes[country_name]
                st.dataframe(df_selected)
                
                # Afficher le graphique de l'indice correspondant
                plot_index_chart(country_name)
            else:
                st.write("Aucune donnée disponible pour ce pays.")
        else:
            st.write("Aucun pays trouvé avec ce nom.")

elif selected == "Optimisation":
    st.write("Optimisez votre portefeuille.")

elif selected == "Pricing":
    st.write("Pricez vos produits.")