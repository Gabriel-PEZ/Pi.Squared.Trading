import streamlit as st

st.set_page_config(
    page_title="π²Trading",
    page_icon="💹",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_css_file(css_file_path):
    with open(css_file_path, "r", encoding="utf-8") as f:
        css_content = f.read()
    return css_content

css_content = load_css_file("/home/onyxia/work/Pi.Squared.Trading/style/styles.css")

st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

#Bibliothèque pour l'animation de "survol" des boutons
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

intro = "Bienvenue sur π² Trading, la plateforme conçue pour transformer vos stratégies financières en véritables succès.\n\nAlliant technologie de pointe et accessibilité, π² Trading met entre vos mains des outils performants et intuitifs, parfaits pour les investisseurs débutants comme pour les experts souhaitant maximiser leur potentiel. Pensée pour offrir une expérience fluide, cette plateforme dynamique, développée sur Streamlit, se distingue par son interface moderne et conviviale, rendant chaque fonctionnalité simple d'accès et agréable à utiliser.\n\nÀ travers des modules innovants comme Stock Picking, Portfolio Visualizer, Portfolio Optimizer et Beta π², elle vous propose une boîte à outils complète pour analyser, créer, simuler et optimiser vos investissements avec précision. En s'appuyant sur des données fiables issues de sources reconnues telles que finance, π² Trading garantit une information à jour et pertinente, vous aidant à prendre des décisions éclairées. Grâce à l'intégration des théories financières modernes et des simulations avancées, vous pouvez explorer de nouvelles opportunités et perfectionner vos portefeuilles dans un environnement entièrement pensé pour répondre à vos besoins.\n\nRejoignez π² Trading dès maintenant et donnez une nouvelle dimension à vos investissements.\n\nπ² Trading : a new way of investing."

justified_intro = f"""
    <div style='text-align: justify; text-justify: inter-word;'>
        {intro}
    </div>
    """
st.markdown(justified_intro, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section" data-aos="fade-up">', unsafe_allow_html=True)
st.markdown("<h2>Services</h2>", unsafe_allow_html=True)
services = [
        {"name": "Stock Picking", "description": "La solution pour construire un portefeuille sur-mesure, avec des données fiables pour des décisions éclairées.", "icon": "📈"},
        {"name": "Portfolio Visualizer", "description": "Analysez votre portefeuille avec des outils visuels clairs et des insights puissants pour maximiser vos performances.", "icon": "📊"},
        {"name": "Portfolio Optimizer", "description": "Optimisez votre portefeuille grâce à la frontière d’efficience, pour maximiser vos rendements et réduire vos risques.", "icon": "⚙️"},
        {"name": "Beta π²", "description": "Notre espace innovation, anticipez les prix d'actions grâce à des prévisions avancées pour optimiser vos décisions d'investissement.", "icon": "💰"}
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

presentation = "Nous sommes deux étudiants de l’ENSAE Paris, animés par une passion commune pour l’analyse quantitative, la finance et la programmation orientée objet. Face à la complexité croissante des outils financiers et au coût élevé des plateformes réservées aux investisseurs institutionnels, nous avons décidé de développer une solution innovante. Notre objectif est de regrouper, au sein d’une seule plateforme, les fonctionnalités souvent payantes et fragmentées d’autres outils, afin de les rendre accessibles à des investisseurs individuels comme nous.\n\n Grâce à l’intégration de données fiables et actualisées en temps réel, notre plateforme aide les utilisateurs à optimiser leurs prises de décision, qu’il s’agisse de construire un portefeuille performant, d’anticiper les mouvements du marché ou d’évaluer des opportunités d’investissement. Nous croyons fermement que la finance doit être plus transparente, inclusive et accessible à tous. Avec π² Trading, nous voulons démocratiser l’accès à des outils financiers avancés et offrir une expérience utilisateur intuitive pour que chacun puisse investir avec confiance et efficacité."

justified_presenation = f"""
    <div style='text-align: justify; text-justify: inter-word;'>
        {presentation}
    </div>
    """
st.markdown(justified_presenation, unsafe_allow_html=True)

st.markdown("""
    <div style='text-align: center; margin-top: 20px; font-size: 18px;'>
        
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
