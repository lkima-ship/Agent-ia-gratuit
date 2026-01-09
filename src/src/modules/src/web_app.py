"""
Interface Web Streamlit
"""

import streamlit as st

def run_web_app():
    st.set_page_config(
        page_title="Assistant IA Gratuit",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 Assistant IA 100% Gratuit")
    st.write("Gérez vos emails, rendez-vous et messages vocaux automatiquement.")
    
    # Menu
    menu = st.sidebar.selectbox(
        "Navigation",
        ["Dashboard", "Emails", "Calendrier", "Vocal", "Configuration"]
    )
    
    if menu == "Dashboard":
        st.header("📊 Tableau de Bord")
        st.metric("📧 Emails traités", "156")
        st.metric("📅 RDV créés", "23")
        st.metric("⏱️ Temps économisé", "42h")
        
    elif menu == "Emails":
        st.header("📧 Gestion des Emails")
        st.text_area("Nouvel email à traiter:", height=200)
        if st.button("🤖 Générer réponse IA"):
            st.success("Réponse générée !")
            
    elif menu == "Calendrier":
        st.header("📅 Calendrier")
        st.date_input("Date du rendez-vous")
        st.time_input("Heure")
        st.text_input("Sujet")
        
    elif menu == "Vocal":
        st.header("🎤 Traitement Vocal")
        audio_file = st.file_uploader("Téléchargez un message vocal", type=['mp3', 'wav'])
        if audio_file and st.button("🎤 Transcrire"):
            st.success("Transcription en cours...")
            
    elif menu == "Configuration":
        st.header("⚙️ Configuration")
        api_key = st.text_input("Clé API Gemini", type="password")
        if st.button("💾 Sauvegarder"):
            st.success("Configuration sauvegardée !")

if __name__ == "__main__":
    run_web_app()
