import streamlit as st

def main():
    st.set_page_config(page_title="π² Trading", page_icon=":chart_with_upwards_trend:", layout='wide')

    # CSS for styling
    st.markdown("""
    <style>
    .title {
        color: #2E86C1; /* Finance blue color */
        text-align: center;
        font-size: 50px; /* Larger font size */
        font-weight: bold;
    }
    .title2 {
        color: #2E86C1; /* Finance blue color */
        text-align: center;
        font-size: 24px; /* Larger font size */
        font-weight: bold;
    }
    .subtitle {
        text-align: center;
    }
    .service-box {
        border: 2px solid #2E86C1; /* Border to make it look like a square */
        padding: 100px 20px; /* Adjusted padding for more vertical depth */
        display: flex;
        flex-direction: column; /* Changed for better alignment of content */
        align-items: center; /* Center content */
        border-radius: 10px; /* Rounded corners for aesthetics */
    }
    .button, .arrow {
        background-color: #2E86C1; /* Finance blue color */
        color: white;
        padding: 10px 24px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }
    .centered-column {
        display: flex;
        flex-direction: column;
        justify-content: center; /* Center the column content vertically */
    }
    </style>
    """, unsafe_allow_html=True)

    # Header section with custom styles
    st.markdown('<h1 class="title">π² Trading</h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="subtitle">A new way of investing</h2>', unsafe_allow_html=True)

    # Introduction to the platform
    st.subheader("Introduction")
    st.write("""
    Welcome to π² Trading, your innovative partner in financial trading. Our platform offers advanced tools 
    designed to optimize your investment strategy, enhance your market insights, and improve portfolio performance.
    """)

    # Our services
    st.subheader("Services")
    services = ["Stock Picking", "Portfolio Visualizer", "Portfolio Optimizer", "Pricing"]
    service_descriptions = {
        "Stock Picking": "Optimize your stock selections with our advanced analytics.",
        "Portfolio Visualizer": "Visualize your investment spread and analyze performance metrics.",
        "Portfolio Optimizer": "Maximize your portfolio's performance based on modern financial theories.",
        "Pricing": "Competitive pricing strategies tailored for different investment levels."
    }

    # Navigation and selection handling
    current_index = st.session_state.get('current_index', 0)

    # Layout for navigation and service display
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        if st.button("←", key="left"):
            st.session_state.current_index = (current_index - 1) % len(services)

    with col2:
        st.markdown(f"<div class='service-box'><h2 class='title2'>{services[current_index]}</h2>{service_descriptions[services[current_index]]}<br><button class='button'>Choose</button></div>", unsafe_allow_html=True)

    with col3:
        if st.button("→", key="right"):
            st.session_state.current_index = (current_index + 1) % len(services)

    # Who We Are section with adjusted column sizes for image and description
    st.subheader("Who we are ?")
    # Section for Piero PELOSI
    col1, col2 = st.columns([1, 3]) 
    with col1:
        # Embed and style the image with border-radius and center alignment
        st.markdown("""
        <div style="text-align: center; margin-bottom: 20px;">
            <img src="https://github.com/pieropls/Pi.Squared.Trading/blob/main/Piero.jpg?raw=true" 
            style="width: 160px; border-radius: 10px;" alt="Piero PELOSI - Co-founder and CEO">
            <p style="margin-top: 10px;">Piero PELOSI - Co-founder and CEO</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        **Piero PELOSI**, *Co-founder and CEO*  
        Piero PELOSI co-founded π² Trading with a vision to transform investment strategies through innovative financial technologies. As the CEO, Piero combines his deep understanding of global financial markets with a passion for progressive financial tools to steer the company toward unprecedented growth. 
        Piero's strategic foresight has been pivotal in shaping π² Trading's development, positioning it as a leader in the trading industry. His expertise in market analysis, coupled with an acute business acumen, has enabled π² Trading to offer superior investment solutions that are both effective and user-friendly.
        Under Piero's leadership, π² Trading has achieved substantial milestones in financial performance and client engagement. He champions a client-centered approach, ensuring that all product developments and innovations directly align with client needs and emerging market trends. This strategy has not only driven the company’s expansion but also solidified its reputation as a trustworthy and innovative investment partner.
        Piero's commitment to excellence and his relentless pursuit of quality are reflected in every aspect of the company’s operations, from client interaction to the comprehensive trading platforms offered by π² Trading. His leadership fosters a culture of integrity and dedication, ensuring that the team remains focused on the core mission of delivering outstanding financial results for its clients.
        """, unsafe_allow_html=True)

    st.markdown("---")  # Adding a horizontal line for separation

    # Section for Gabriel PEZENNEC
    col1, col2 = st.columns([1, 3])
    with col1:
        # Embed and style the image with border-radius and center alignment
        st.markdown("""
        <div style="text-align: center; margin-bottom: 20px;">
            <img src="https://github.com/pieropls/Pi.Squared.Trading/blob/main/Gabriel.jpg?raw=true" 
            style="width: 160px; border-radius: 10px;" alt="Gabriel PEZENNEC - Co-founder and CTO">
            <p style="margin-top: 10px;">Gabriel PEZENNEC - Co-founder and CTO</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        **Gabriel PEZENNEC**, *Co-founder and CTO*  
        Gabriel Pezennec, a dynamic co-founder and the Chief Technology Officer at π² Trading, brings a wealth of knowledge and innovation to the forefront of financial technology. With a robust background in computer science and extensive experience in software development, Gabriel has been instrumental in architecting the technical strategies that propel π² Trading ahead of industry trends.
        Under his technical leadership, π² Trading has developed cutting-edge trading algorithms and platforms that integrate advanced data analytics to provide real-time financial insights. Gabriel's commitment to technological excellence and his forward-thinking approach to development have established a strong foundation for scalable solutions, enabling the firm to adapt swiftly to the ever-evolving market conditions.
        His visionary leadership in technology not only enhances operational efficiencies but also ensures that the firm's offerings are secure, reliable, and at the forefront of the financial technology sector. Gabriel’s hands-on approach in leading the technology team fosters an environment of innovation and continuous improvement, ensuring that π² Trading remains at the cutting edge of the trading industry.
        """, unsafe_allow_html=True)

    # Contact us form
    st.subheader("Contact Us")
    with st.form(key='contact_form', clear_on_submit=True):  # Add clear_on_submit if you want to clear the form after submit
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
            if name and email:  # Check mandatory fields
                st.success("Thank you for your message!")
            else:
                st.error("Please fill in all required fields (First Name and Email are mandatory).")


if __name__ == "__main__":
    main()
