import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu  # Assurez-vous que streamlit_option_menu est installé
import yfinance as yf
import plotly.graph_objs as go
import plotly.express as px
import numpy as np

# Configuration de la page
st.set_page_config(
    page_title="π²Trading",
    page_icon="💹",
    layout="wide",
)

# Fonction pour obtenir le nom de l'entreprise à partir du ticker
def get_company_name(ticker):
    try:
        company = yf.Ticker(ticker).info.get('longName', 'N/A')
    except:
        company = 'N/A'
    return company

# Fonction pour calculer la performance historique du portefeuille
def calculate_portfolio_performance(tickers, weights, period='1y'):
    data = yf.download(tickers, period=period)['Adj Close']
    if isinstance(data, pd.Series):
        data = data.to_frame()
    returns = data.pct_change().dropna()
    weighted_returns = returns.multiply(weights, axis=1)
    portfolio_returns = weighted_returns.sum(axis=1)
    portfolio_cumulative = (1 + portfolio_returns).cumprod()
    return portfolio_cumulative, portfolio_returns

# Initialisation des listes dans session_state
if 'tickers' not in st.session_state:
    st.session_state.tickers = ['']
if 'weights' not in st.session_state:
    st.session_state.weights = [0.0]

# Fonction pour ajouter un actif
def add_asset():
    st.session_state.tickers.append('')
    st.session_state.weights.append(0.0)

# Fonction pour supprimer un actif
def remove_asset(index):
    del st.session_state.tickers[index]
    del st.session_state.weights[index]

# Création du menu horizontal en haut de la page
selected = option_menu(
    menu_title=None,  # Pas de titre pour le menu
    options=["Accueil", "Création de Portefeuille", "Actions", "Optimisation"],
    icons=["house", "briefcase", "graph-up", "gear"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#ffffff"},
        "icon": {"font-size": "18px"},  # Taille des icônes
        "nav-link": {
            "font-size": "18px",
            "text-align": "center",
            "margin": "0px",
            "color": "#2c3e50",  # Couleur du texte et des icônes pour les onglets non sélectionnés
            "--hover-color": "#eee",
        },
        "nav-link-selected": {
            "background-color": "#0d1680",
            "color": "#ffffff",  # Texte et icône en blanc pour l'onglet sélectionné
        },
    },
)

# Affichage du contenu en fonction du choix
if selected == "Accueil":
    # Personnaliser l'apparence
    def local_css(css_text):
        st.markdown(f'<style>{css_text}</style>', unsafe_allow_html=True)

    css = """
    h1 {
        text-align: center;
        color: #0d1680;
    }
    h2, h3 {
        text-align: center;
    }
    .st-button>button {
        background-color: #0d1680;
        color: white;
    }
    """
    local_css(css)

    # Contenu de la page d'accueil
    st.title("Bienvenue sur π²Trading")
    # st.image("chemin/vers/votre/logo.png", use_column_width=True)  # Décommentez et spécifiez le chemin si vous avez un logo
    st.markdown("## Votre plateforme d'analyse financière innovante")
    st.markdown("""
    **π²Trading** est votre solution complète pour analyser les marchés financiers et optimiser votre portefeuille d'investissement.
    """)

    st.markdown("### Nos fonctionnalités clés")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("#### 💹 Analyse du marché")
        st.write("Accédez aux dernières données du marché en temps réel.")
    with col2:
        st.markdown("#### 📈 Optimisation de portefeuille")
        st.write("Utilisez nos outils avancés pour maximiser vos rendements.")
    with col3:
        st.markdown("#### 🔍 Recherche d'actions")
        st.write("Explorez des analyses détaillées pour prendre les meilleures décisions.")

    st.markdown("### Prêt à démarrer ?")

    st.write("---")
    st.markdown("© 2024 π²Trading. Tous droits réservés.")
    st.markdown("📧 Contactez-nous : [contact@pi2trading.com](mailto:contact@pi2trading.com)")

elif selected == "Création de Portefeuille":
    st.title("Création de Portefeuille")
    st.write("Veuillez entrer les actifs que vous souhaitez inclure dans votre portefeuille ainsi que les poids associés.")

    # Initialisation des compteurs et listes de suppression
    if 'asset_count' not in st.session_state:
        st.session_state.asset_count = 1
    if 'to_remove' not in st.session_state:
        st.session_state.to_remove = []

    # Fonction pour ajouter un actif
    def add_asset():
        st.session_state.asset_count += 1

    # Fonction pour supprimer un actif
    def remove_asset(index):
        st.session_state.to_remove.append(index)


    # Bouton pour ajouter un actif
    st.button("Ajouter un actif", on_click=add_asset)

    # Afficher les champs d'entrée pour chaque actif
    for i in range(st.session_state.asset_count):
        if i in st.session_state.to_remove:
            continue
        cols = st.columns([2, 2, 1])
        with cols[0]:
            st.text_input(f"Ticker {i+1}", key=f"ticker_{i}", placeholder="Ex: AAPL")
        with cols[1]:
            st.number_input(f"Poids {i+1} (%)", key=f"weight_{i}", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
        with cols[2]:
            if st.button("Supprimer", key=f"remove_{i}"):
                remove_asset(i)
                st.experimental_rerun()

    # Bouton pour valider et traiter le portefeuille
    if st.button("Valider le Portefeuille"):
        tickers = []
        weights = []
        for i in range(st.session_state.asset_count):
            ticker = st.session_state.get(f"ticker_{i}", "").strip().upper()
            weight = st.session_state.get(f"weight_{i}", 0.0)
            if ticker:
                tickers.append(ticker)
                weights.append(weight)
        
        # Créer le DataFrame du portefeuille
        df = pd.DataFrame({
            'Ticker': tickers,
            'Poids (%)': weights
        })

        # Vérification des poids
        total_weight = df['Poids (%)'].sum()
        if total_weight == 0:
            st.error("La somme des poids est égale à 0%. Veuillez entrer des poids valides.")
            st.stop()

        # Convertir les poids en float
        try:
            df['Poids (%)'] = df['Poids (%)'].astype(float)
        except ValueError:
            st.error("Veuillez entrer des valeurs numériques valides pour les poids.")
            st.stop()

        # Vérification des poids positifs
        if (df['Poids (%)'] <= 0).any():
            st.error("Tous les poids doivent être strictement positifs.")
            st.stop()
        else:
            # Vérification que la somme des poids est égale à 100%
            if total_weight != 100.0:
                st.warning(f"⚠️ La somme des poids est de {total_weight:.2f}%. Elle doit être égale à 100%.")
                normalize = st.checkbox("Voulez-vous normaliser les poids automatiquement ?", key="normalize_validation")
                if normalize:
                    df['Poids (%)'] = df['Poids (%)'] * 100 / total_weight
                    total_weight = df['Poids (%)'].sum()
                    st.success("Les poids ont été normalisés.")
            else:
                st.success("✅ La somme des poids est égale à 100%.")

        # Vérification des tickers valides et récupération des noms d'entreprises
        valid_tickers = []
        invalid_tickers = []
        company_names = []

        for ticker in df['Ticker']:
            if ticker:  # Vérifier que le ticker n'est pas vide
                try:
                    company_name = get_company_name(ticker)
                    if company_name != 'N/A':
                        valid_tickers.append(ticker.upper())
                        company_names.append(company_name)
                    else:
                        invalid_tickers.append(ticker)
                except Exception as e:
                    invalid_tickers.append(ticker)
                    st.error(f"Erreur lors de la vérification du ticker {ticker}: {e}")

        if invalid_tickers:
            st.error(f"Les tickers suivants ne sont pas valides ou les données ne sont pas disponibles : {', '.join(invalid_tickers)}")
            st.stop()
        elif not valid_tickers:
            st.error("Aucun ticker valide n'a été fourni.")
            st.stop()
        else:
            # Créer le portefeuille avec le nom des entreprises
            portfolio = {
                'Actions': valid_tickers,
                'Nom de l\'Entreprise': company_names,
                'Poids (%)': [df.loc[df['Ticker'] == ticker, 'Poids (%)'].values[0] for ticker in valid_tickers]
            }
            portfolio_df = pd.DataFrame(portfolio)
            portfolio_df.index = range(1, 1 + len(valid_tickers))

            # Calculer des métriques globales
            total_weight = portfolio_df['Poids (%)'].sum()
            average_weight = portfolio_df['Poids (%)'].mean()
            max_weight = portfolio_df['Poids (%)'].max()
            min_weight = portfolio_df['Poids (%)'].min()

            # Calcul des nouvelles statistiques
            # Calcul du rendement attendu (annualisé)
            portfolio_cumulative, portfolio_returns = calculate_portfolio_performance(
                valid_tickers, 
                np.array(portfolio_df['Poids (%)'].tolist()) / 100, 
                period='1y'
            )
            expected_return = portfolio_returns.mean() * 252  # 252 jours de bourse par an

            # Calcul de la volatilité (annualisée)
            volatility = portfolio_returns.std() * np.sqrt(252)

            # Calcul du ratio de Sharpe (avec un taux sans risque de 2%)
            risk_free_rate = 0.02
            sharpe_ratio = (expected_return - risk_free_rate) / volatility if volatility != 0 else np.nan

            # Afficher les éléments séquentiellement
            st.write("### Votre portefeuille :")
            st.write("#### Tableau Récapitulatif")
            fig_table = go.Figure(data=[go.Table(
                header=dict(
                    values=list(portfolio_df.columns),
                    fill_color='#0d1680',  # Couleur d'arrière-plan des en-têtes (bleu marine)
                    font=dict(color='white', size=16),  # Taille de la police augmentée
                    align='center',
                    height=50  # Hauteur des en-têtes augmentée
                ),
                cells=dict(
                    values=[portfolio_df.Actions, portfolio_df["Nom de l'Entreprise"], portfolio_df['Poids (%)']],
                    fill_color=[['#f2f2f2']*len(portfolio_df), ['#f2f2f2']*len(portfolio_df), ['#e6f7ff']*len(portfolio_df)],
                    font=dict(color='black', size=14),  # Taille de la police augmentée
                    align='center',
                    height=35  # Hauteur des cellules augmentée
                )
            )])
            fig_table.update_layout(
                width=800,  # Augmenter la largeur du tableau
                height=200,  # Augmenter la hauteur du tableau
                margin=dict(l=0, r=0, t=50, b=0)
            )
            st.plotly_chart(fig_table, use_container_width=True)

            # Afficher les statistiques du portefeuille
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

            # Créer des colonnes pour afficher les métriques en ligne et les centrer
            num_metrics = len(metrics_labels)
            cols = st.columns(num_metrics)

            for col, label, value, description in zip(cols, metrics_labels, metrics_values, metrics_descriptions):
                with col:
                    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
                    st.metric(label, value)
                    st.caption(description)
                    st.markdown("</div>", unsafe_allow_html=True)

            # Créer deux colonnes pour les graphiques côte à côte
            graph_cols = st.columns(2)

            with graph_cols[0]:
                st.write("### Performance Historique du Portefeuille")

                # Créer le graphique de performance historique avec Plotly
                fig_performance = go.Figure()
                fig_performance.add_trace(go.Scatter(
                    x=portfolio_cumulative.index,
                    y=portfolio_cumulative.values,
                    mode='lines',
                    name='Performance du Portefeuille',
                    line=dict(color='#0d1680')
                ))

                fig_performance.update_layout(
                    title='Performance Historique du Portefeuille',
                    xaxis_title='Date',
                    yaxis_title='Valeur Cumulative',
                    template='plotly_white',
                    height=400
                )

                st.plotly_chart(fig_performance, use_container_width=True)

            with graph_cols[1]:
                st.write("### Répartition des Poids dans le Portefeuille")
                fig_pie = go.Figure(data=[go.Pie(
                    labels=portfolio_df['Actions'],
                    values=portfolio_df['Poids (%)'],
                    hole=.3,
                    textinfo='percent+label',
                    insidetextorientation='radial',
                    marker=dict(colors=px.colors.qualitative.Pastel)  # Palette de couleurs harmonieuse
                )])
                fig_pie.update_layout(
                    title_text='Répartition des Poids dans le Portefeuille',
                    annotations=[dict(text='Portefeuille', x=0.5, y=0.5, font_size=20, showarrow=False)],
                    showlegend=True,
                    height=400
                )
                st.plotly_chart(fig_pie, use_container_width=True)

            # Stocker le portefeuille dans session_state
            st.session_state['portfolio'] = portfolio_df
            st.success("Le portefeuille a été enregistré pour une utilisation ultérieure.")


elif selected == "Actions":
    st.title("Actions")
    st.write("Ici, vous pouvez consulter les actions disponibles...")

    # Saisie du ticker par l'utilisateur
    ticker = st.text_input("Entrez le ticker de l'action (par exemple, AAPL pour Apple) :")

    # Sélection de la période
    period_options = ['1 mois', '3 mois', '6 mois', '1 an', '2 ans', '5 ans', 'Max']
    period_mapping = {
        '1 mois': '1mo',
        '3 mois': '3mo',
        '6 mois': '6mo',
        '1 an': '1y',
        '2 ans': '2y',
        '5 ans': '5y',
        'Max': 'max'
    }
    period_choice = st.selectbox("Sélectionnez la période :", period_options, index=0)
    period = period_mapping[period_choice]

    # Vérifier si le ticker n'est pas vide
    if ticker:
        try:
            # Récupérer les données boursières
            stock = yf.Ticker(ticker)
            data = stock.history(period=period)

            # Récupérer les informations supplémentaires sur l'action
            info = stock.info

            # Vérifier si les données sont disponibles
            if not data.empty:
                # Afficher des informations détaillées sur l'action
                st.subheader(f"Informations sur {ticker.upper()}")

                # Organiser les informations en colonnes
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Entreprise", info.get('longName', 'N/A'))
                    st.metric("Secteur", info.get('sector', 'N/A'))
                with col2:
                    st.metric("Industrie", info.get('industry', 'N/A'))
                    market_cap = info.get('marketCap', None)
                    if market_cap:
                        # Formatage de la capitalisation boursière
                        if market_cap >= 1e12:
                            market_cap_formatted = f"{market_cap / 1e12:.2f} T"
                        elif market_cap >= 1e9:
                            market_cap_formatted = f"{market_cap / 1e9:.2f} B"
                        elif market_cap >= 1e6:
                            market_cap_formatted = f"{market_cap / 1e6:.2f} M"
                        else:
                            market_cap_formatted = f"${market_cap:,}"
                        st.metric("Capitalisation Boursière", f"${market_cap_formatted}")
                    else:
                        st.metric("Capitalisation Boursière", 'N/A')
                with col3:
                    trailing_pe = info.get('trailingPE', 'N/A')
                    st.metric("Ratio P/E", f"{trailing_pe}" if trailing_pe != 'N/A' else 'N/A')
                    dividend_yield = info.get('dividendYield', None)
                    if dividend_yield is not None:
                        st.metric("Rendement Dividende", f"{dividend_yield * 100:.2f}%")
                    else:
                        st.metric("Rendement Dividende", 'N/A')

                # Afficher un résumé de l'entreprise avec justification
                st.markdown("### Résumé de l'entreprise")
                summary = info.get('longBusinessSummary', 'Aucun résumé disponible.')
                justified_summary = f"""
                <div style='text-align: justify; text-justify: inter-word;'>
                    {summary}
                </div>
                """
                st.markdown(justified_summary, unsafe_allow_html=True)

                # Créer le candlestick chart
                fig = go.Figure(data=[go.Candlestick(
                    x=data.index,
                    open=data['Open'],
                    high=data['High'],
                    low=data['Low'],
                    close=data['Close'],
                    increasing_line_color='green',
                    decreasing_line_color='red'
                )])

                fig.update_layout(
                    title=f"Cours de l'action {ticker.upper()} sur {period_choice}",
                    xaxis_title='Date',
                    yaxis_title='Prix',
                    width=1000,   # Largeur du graphique en pixels
                    height=700,
                    xaxis_rangeslider_visible=True,
                    template='plotly_white'
                )

                # Afficher le graphique
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.error("Les données pour ce ticker ne sont pas disponibles.")
        except Exception as e:
            st.error(f"Une erreur est survenue : {e}")

elif selected == "Optimisation":
    st.title("Optimisation")
    st.write("Ici, vous pouvez optimiser votre portefeuille...")

    if 'portfolio' in st.session_state:
        data = st.session_state['portfolio']
        st.write("### Portefeuille actuel :")
        # Afficher le tableau stylisé avec Plotly
        fig_table = go.Figure(data=[go.Table(
            header=dict(
                values=list(data.columns),
                fill_color='#0d1680',
                font=dict(color='white', size=16),
                align='center',
                height=50
            ),
            cells=dict(
                values=[data.Actions, data["Nom de l'Entreprise"], data['Poids (%)']],
                fill_color=[['#f2f2f2']*len(data), ['#f2f2f2']*len(data), ['#e6f7ff']*len(data)],
                font=dict(color='black', size=14),
                align='center',
                height=35
            )
        )])
        fig_table.update_layout(
            width=800,
            height=200,
            margin=dict(l=0, r=0, t=50, b=0)
        )
        st.plotly_chart(fig_table, use_container_width=True)

        # Calculer des métriques globales
        total_weight = data['Poids (%)'].sum()
        average_weight = data['Poids (%)'].mean()
        max_weight = data['Poids (%)'].max()
        min_weight = data['Poids (%)'].min()

        # Calcul des nouvelles statistiques
        # Calcul du rendement attendu (annualisé)
        portfolio_cumulative, portfolio_returns = calculate_portfolio_performance(
            data['Actions'].tolist(), 
            np.array(data['Poids (%)'].tolist()) / 100, 
            period='1y'
        )
        expected_return = portfolio_returns.mean() * 252  # 252 jours de bourse par an

        # Calcul de la volatilité (annualisée)
        volatility = portfolio_returns.std() * np.sqrt(252)

        # Calcul du ratio de Sharpe (avec un taux sans risque de 2%)
        risk_free_rate = 0.02
        sharpe_ratio = (expected_return - risk_free_rate) / volatility if volatility != 0 else np.nan

        # Afficher les métriques en ligne
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

        # Créer des colonnes pour afficher les métriques en ligne et les centrer
        num_metrics = len(metrics_labels)
        cols = st.columns(num_metrics)

        for col, label, value, description in zip(cols, metrics_labels, metrics_values, metrics_descriptions):
            with col:
                st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
                st.metric(label, value)
                st.caption(description)
                st.markdown("</div>", unsafe_allow_html=True)

        # Créer deux colonnes pour les graphiques côte à côte
        graph_cols = st.columns(2)

        with graph_cols[0]:
            st.write("### Performance Historique du Portefeuille")

            # Créer le graphique de performance historique avec Plotly
            fig_performance = go.Figure()
            fig_performance.add_trace(go.Scatter(
                x=portfolio_cumulative.index,
                y=portfolio_cumulative.values,
                mode='lines',
                name='Performance du Portefeuille',
                line=dict(color='#0d1680')
            ))

            fig_performance.update_layout(
                title='Performance Historique du Portefeuille',
                xaxis_title='Date',
                yaxis_title='Valeur Cumulative',
                template='plotly_white',
                height=400
            )

            st.plotly_chart(fig_performance, use_container_width=True)

        with graph_cols[1]:
            st.write("### Répartition des Poids dans le Portefeuille")
            fig_pie = go.Figure(data=[go.Pie(
                labels=data['Actions'],
                values=data['Poids (%)'],
                hole=.3,
                textinfo='percent+label',
                insidetextorientation='radial',
                marker=dict(colors=px.colors.qualitative.Pastel)  # Palette de couleurs harmonieuse
            )])
            fig_pie.update_layout(
                title_text='Répartition des Poids dans le Portefeuille',
                annotations=[dict(text='Portefeuille', x=0.5, y=0.5, font_size=20, showarrow=False)],
                showlegend=True,
                height=400
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        # Placeholder pour l'optimisation
        st.write("#### Optimisation du portefeuille")
        st.write("Fonctionnalités d'optimisation à venir...")
    else:
        st.info("Veuillez créer un portefeuille dans la section 'Création de Portefeuille' avant de procéder à l'optimisation.")



