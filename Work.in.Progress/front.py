import streamlit as st

# Initialize the session states for navigation and theme
if 'service_index' not in st.session_state:
    st.session_state.service_index = 0
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'  # Default theme is light

# Toggle the theme
def toggle_theme():
    st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'

# Load CSS based on the current theme
def load_css(theme):
    background_color = '#FFFFFF' if theme == 'light' else '#000000'
    text_color = '#000000' if theme == 'light' else '#FFFFFF'
    title_color = '#0047ab' if theme == 'light' else '#87ceeb'
    arrow_color = '#000000' if theme == 'dark' else '#FFFFFF'
    button_background = '#FFFFFF' if theme == 'dark' else '#000000'
    
    return f"""
        <style>
            html, body, .stApp {{
                background-color: {background_color};
                color: {text_color};
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            }}
            .content {{
                border: 2px solid {text_color};
                border-radius: 5px;
                padding: 40px;
                margin: 20px;
                color: {text_color};
                text-align: center;
            }}
            .btn, .stButton>button {{
                background-color: {button_background};
                color: {arrow_color};
                padding: 8px 16px;
                border: 2px solid {arrow_color};
                border-radius: 5px;
                cursor: pointer;
                font-size: 18px;
                display: inline-block;
            }}
            .toggle {{
                position: fixed;
                top: 10px;
                right: 10px;
                font-size: 24px;
                background: none;
                border: none;
                cursor: pointer;
                color: {arrow_color};
            }}
            h1 {{
                text-align: center;
                color: {title_color};
            }}
        </style>
    """

# Function to navigate between services
def navigate(direction):
    if direction == 'next' and st.session_state.service_index < len(services) - 1:
        st.session_state.service_index += 1
    elif direction == 'prev' and st.session_state.service_index > 0:
        st.session_state.service_index -= 1

# Services data
services = [
    ("Portfolio Creation", "Create diversified portfolios tailored to your financial goals."),
    ("Market Indices", "Explore market indices to gauge general market trends."),
    ("Optimization", "Optimize your portfolio for maximum efficiency and risk management."),
    ("Pricing", "Advanced pricing models to value financial instruments accurately.")
]

def main():
    st.markdown(load_css(st.session_state.theme), unsafe_allow_html=True)

    # Theme toggle button in the top right
    if st.button("☀️" if st.session_state.theme == 'light' else "🌙", key='theme_button'):
        toggle_theme()

    # Centered title
    st.markdown(f"<h1>π² Trading</h1>", unsafe_allow_html=True)

    # Display current service
    service = services[st.session_state.service_index]
    service_title, service_desc = service
    st.markdown(f"<div class='content'><h2>{service_title}</h2><p>{service_desc}</p><button class='btn'>Access {service_title}</button></div>", unsafe_allow_html=True)

    # Navigation buttons
    col1, col2, col3 = st.columns([1, 6, 1])
    with col1:
        if st.session_state.service_index > 0:
            st.button("←", on_click=navigate, args=('prev',), key='prev_button')
    with col3:
        if st.session_state.service_index < len(services) - 1:
            st.button("→", on_click=navigate, args=('next',), key='next_button')

if __name__ == "__main__":
    main()