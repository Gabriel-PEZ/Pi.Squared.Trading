import streamlit as st
from streamlit_option_menu import option_menu  

st.set_page_config(
    page_title="π²Trading",
    page_icon="💹",
    layout="wide",
    initial_sidebar_state="expanded"
)

def local_css(css_text):
    st.markdown(f'<style>{css_text}</style>', unsafe_allow_html=True)

css = """
/* Palette de couleurs sobre */
/* Palette de couleurs améliorée */
:root {
    --primary-color: #1a1a1a; /* Noir profond */
    --secondary-color: #f0f2f6; /* Gris très clair */
    --accent-color: #6c757d; /* Gris doux */
    --text-color: #333333; /* Gris foncé pour le texte */
    --success-color: #28a745; /* Vert */
    --warning-color: #ffc107; /* Jaune */
    --error-color: #dc3545; /* Rouge */
    --font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    --finance-green: #0611ab; /* Vert 28a745 */
    --background-gradient: linear-gradient(135deg, #f0f2f6 0%, #d9e2ec 100%);
}


/* Styles généraux */
body {
    font-family: var(--font-family);
    color: var(--text-color);
    background-color: var(--secondary-color);
    margin: 0;
    padding: 0;
}

/* Titres */
h1, h2, h3 {
    text-align: center;
    color: var(--primary-color);
}

.pi {
    color: var(--text-color); /* Noir ou la couleur définie dans --text-color */   #CLASSE POUR PI 
}

.superscript {
    color: #0611ab; /* Vert personnalisé #28a745 */
    font-size: 0.8em; /* Taille ajustée pour le "²" */
    vertical-align: baseline; /* Alignement sur la ligne de base */             #CLASSE POUR ²
    margin-left: -0.1em; /* Rapprochement du "²" avec le "π" */
    position: relative; /* Permet de décaler l'élément */
    top: -0.3em; /* Décalage subtil vers le bas */
}

.trading {
    color: var(--text-color);
    position: relative;
    left: -8px; /* Ajustez cette valeur en pixels selon vos besoins */
}

/* Boutons */
.stButton>button {
    background-color: white; /* Fond blanc */
    color: black;            /* Texte noir */
    border: 1px solid #ccc; /* Bordure grise claire */
    border-radius: 4px;
    padding: 8px 16px;
    transition: background-color 0.2s, transform 0.1s;
    font-size: 14px;
}

.stButton>button:hover {
    background-color: #f4f2f2; /* Fond gris très clair au survol */
    transform: scale(1.02);     /* Légère augmentation de la taille */
}

/* Sidebar */
.sidebar .sidebar-content {
    background-color: var(--secondary-color);
    border-right: 1px solid var(--accent-color); /* Ajout d'une bordure droite */
}

/* Logo */
.sidebar .sidebar-content img {
    margin-bottom: 20px; /* Espacement sous le logo */
    border-radius: 10px;  /* Coins arrondis pour le logo */
}

/* Tables */
table {
    width: 100%;
    border-collapse: collapse;
}

th {
    background-color: var(--primary-color);
    color: white;
    padding: 10px;
    text-align: center;
}

td {
    padding: 8px;
    text-align: center;
    border-bottom: 1px solid #dddddd;
}

/* Metrics */
.metric-container {
    text-align: center;
}

/* Styles supplémentaires pour la nouvelle page d'accueil */
.title {
    color: var(--finance-green); 
    text-align: center;
    font-size: 50px; /* Larger font size */
    font-weight: bold;
    margin-top: 20px;
}

.subtitle {
    text-align: center;
    font-size: 24px;
    color: var(--primary-color);
}

/* Modification de la padding pour réduire les espaces entre les sections */
.section {
    padding: 40px 20px; /* Réduction de 60px à 40px */
    position: relative;
    overflow: hidden;
}

.section::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: url('https://images.unsplash.com/photo-1521790369241-9d3a45ecaf81?fit=crop&w=1350&q=80'); /* Exemple d'image de fond */
    background-size: cover;
    background-position: center;
    opacity: 0.1;
    z-index: -1;
    transform: translateY(-50%);
    transition: transform 0.5s ease-out;
}

.section.animate::before {
    transform: translateY(0);
}

.service-box {
    background-color: white;
    border: 2px solid var(--finance-green); 
    padding: 40px 20px; /* Adjusted padding for more vertical depth */
    display: flex;
    flex-direction: column; /* Changed for better alignment of content */
    align-items: center; /* Center content */
    border-radius: 10px; /* Rounded corners for aesthetics */
    transition: transform 0.3s, box-shadow 0.3s;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.service-box:hover {
    transform: translateY(-10px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}

.service-icon {
    font-size: 50px;
    margin-bottom: 20px;
    color: var(--finance-green);
}

.button, .arrow {
    background-color: var(--finance-green); /* Finance blue color */
    color: white;
    padding: 10px 24px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

.button:hover {
    background-color: #1e5a99; /* Une teinte plus foncée pour le hover */
}

.centered-column {
    display: flex;
    flex-direction: column;
    justify-content: center; /* Center the column content vertically */
}

/* Grid layout for services */
.services-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
    padding: 20px 0;
}

/* Animation on scroll using AOS library */
@import url('https://unpkg.com/aos@2.3.4/dist/aos.css');
"""

local_css(css)

# Inclure la bibliothèque AOS pour les animations
st.markdown("""
<link href="https://unpkg.com/aos@2.3.4/dist/aos.css" rel="stylesheet">
<script src="https://unpkg.com/aos@2.3.4/dist/aos.js"></script>
<script>
  AOS.init({
    duration: 1200,
  });
</script>
""", unsafe_allow_html=True)

st.markdown('''
        <h1 class="title">
            <span class="pi">π</span><span class="superscript">²</span>
            <span class="trading">Trading</span>
        </h1>
    ''', unsafe_allow_html=True)
st.markdown('<h2 class="subtitle">A new way of investing</h2>', unsafe_allow_html=True)

st.markdown('<div class="section" data-aos="fade-up">', unsafe_allow_html=True)
st.markdown("""
    <h2>Introduction</h2>
    <p>
    Welcome to π² Trading, your innovative partner in financial trading. Our platform offers advanced tools 
    designed to optimize your investment strategy, enhance your market insights, and improve portfolio performance.
    </p>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section" data-aos="fade-up">', unsafe_allow_html=True)
st.markdown("<h2>Services</h2>", unsafe_allow_html=True)
services = [
        {"name": "Stock Picking", "description": "", "icon": "📈"},
        {"name": "Portfolio Visualizer", "description": "", "icon": "📊"},
        {"name": "Portfolio Optimizer", "description": "Portfolio Optimizer permet aux utilisateurs de récupérer le portefeuille créé dans la section Portfolio Visualizer pour une analyse approfondie. Le portefeuille est résumé à travers un tableau récapitulatif des principales statistiques et un graphique illustrant la répartition des poids entre les entreprises. Ensuite, π² Trading calcule la frontière d’efficience à l’aide de la Modern Portfolio Theory pour optimiser les rendements. L’utilisateur peut définir le nombre de simulations (de 1 000 à 20 000) pour plus de précision et ajuster le taux sans risque, récupéré automatiquement par API ou saisi manuellement. La plateforme affiche ensuite la frontière d’efficience avec la position actuelle du portefeuille et propose un portefeuille optimal, soit pour minimiser la volatilité, soit pour maximiser le ratio Sharpe.", "icon": "⚙️"},
        {"name": "Beta π²", "description": "Beta π² est l’espace innovant de π² Trading, conçu pour les investisseurs curieux d’explorer de nouvelles opportunités et maximiser leurs stratégies. Cette section propose un générateur aléatoire de portefeuilles, idéal pour tester des idées originales et audacieuses. L’utilisateur sélectionne un indice de référence, un intervalle pour le nombre de titres à inclure (par exemple, entre 15 et 20) et le nombre de simulations souhaitées. La plateforme génère alors des portefeuilles aux pondérations aléatoires et identifie celui ayant affiché les meilleures performances sur les cinq dernières années. Avec enthousiasme, π² Trading permet de récupérer les composantes du portefeuille gagnant et d’accéder aux données clés habituelles, comme dans les autres sections, pour des décisions stratégiques éclairées.", "icon": "💰"}
    ]

num_services = len(services)
for i in range(0, num_services, 2):
    st.markdown('<div style="margin-bottom: 1px;">', unsafe_allow_html=True)
    cols = st.columns(2)
    for j in range(2):
        if i + j < num_services:
            service = services[i + j]
            with cols[j]:
                st.markdown(f"""
                    <div class='service-box'>
                        <div class='service-icon'>{service['icon']}</div>
                        <h3>{service['name']}</h3>
                        <p>{service['description']}</p>
                        <!-- Suppression du bouton "Choose" -->
                        <!--<button class='button'>Choose</button>-->
                    </div>
                    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)  
st.markdown('</div>', unsafe_allow_html=True)  

st.markdown('<div class="section" data-aos="fade-up">', unsafe_allow_html=True)
st.markdown("<h2 style='margin-bottom: 40px;'>Qui sommes-nous ?</h2>", unsafe_allow_html=True) 

st.markdown("""
    <div style="display: flex; justify-content: center; gap: 60px; align-items: flex-start; margin-bottom: 20px; flex-wrap: wrap;">
        <div style="width: 200px; display: flex; flex-direction: column; justify-content: center; align-items: center;">
            <img src="https://github.com/pieropls/Pi.Squared.Trading/blob/main/PieroV3.jpg?raw=true" 
                 style="width: 100%; height: auto; object-fit: contain; border-radius: 10px;" 
                 alt="Piero PELOSI - Co-founder and CEO">
            <p style="font-style: italic; margin-top: 10px;">Piero PELOSI</p>
        </div>
        <div style="width: 200px; display: flex; flex-direction: column; justify-content: center; align-items: center;">
            <img src="https://github.com/pieropls/Pi.Squared.Trading/blob/main/GabrielV3.jpg?raw=true" 
                 style="width: 100%; height: auto; object-fit: contain; border-radius: 10px;" 
                 alt="Gabriel PEZENNEC - Co-founder and CTO">
            <p style="font-style: italic; margin-top: 10px;">Gabriel PEZENNEC</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

 
st.markdown("""
    <div style='text-align: center; margin-top: 20px; font-size: 18px;'>
        Nous sommes des étudiants à l'ENSAE Paris, passionnés par l'analyse quantitative, la finance et les technologies innovantes. Notre objectif est de transformer les stratégies d'investissement grâce à des outils financiers avancés.
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  


st.markdown('<div class="section" data-aos="fade-up">', unsafe_allow_html=True)
st.markdown("<h2>Contact Us</h2>", unsafe_allow_html=True)
with st.form(key='contact_form', clear_on_submit=True): 
    col1, col2 = st.columns([1, 4])
    with col1:
        name = st.text_input("First Name", '', help="Enter your first name", placeholder="John")
        last_name = st.text_input("Last Name", '', help="Enter your last name", placeholder="Doe")
    with col2:
        email = st.text_input("Email", '', help="Enter your email address", placeholder="example@mail.com")
        phone = st.text_input("Phone", '', help="Enter your phone number", placeholder="123-456-7890")
        
    message = st.text_area("Message", '', help="Enter your message here", placeholder="Your message here...")

    submit_button = st.form_submit_button("Send")

    if submit_button:
        if name and email:  
            st.success("Thank you for your message!")
                
        else:
            st.error("Please fill in all required fields (First Name and Email are mandatory).")
st.markdown('</div>', unsafe_allow_html=True) 