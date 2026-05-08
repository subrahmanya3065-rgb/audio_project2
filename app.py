import streamlit as st
from audio_recorder_streamlit import audio_recorder
from deep_translator import GoogleTranslator
from gtts import gTTS
import speech_recognition as sr
from io import BytesIO

# Get a list of supported languages for the dropdown
langs_dict = GoogleTranslator().get_supported_languages(as_dict=True)

def main():
    st.set_page_config(page_title="PragyanAI Translator", page_icon="🎙️")
    
    # Header Section
    st.title("🎙️ PragyanAI - VVIET Workshop")
    st.subheader("Real-time Speech-to-Speech Translation")
    
    # Sidebar for settings
    st.sidebar.header("Settings")
    target_lang = st.sidebar.selectbox("Select Target Language", list(langs_dict.keys()), index=list(langs_dict.keys()).index('hindi') if 'hindi' in langs_dict else 0)
    target_code = langs_dict[target_lang]

    # Audio Recording
    footer_container = st.container()
    with footer_container:
        audio_bytes = audio_recorder(
            text="Click the mic to speak",
            recording_color="#e8b62c",
            neutral_color="#6aa36f",
            icon_size="3x",
        )
    
    if audio_bytes:
        # Display the recorded audio
        st.audio(audio_bytes, format="audio/wav")
        
        with st.spinner("Processing your voice..."):
            try:
                # 1. Speech to Text (Transcribing)
                recognizer = sr.Recognizer()
                with sr.AudioFile(BytesIO(audio_bytes)) as source:
                    audio_data = recognizer.record(source)
                    # Use Google's speech recognition
                    text = recognizer.recognize_google(audio_data)
                    
                # Layout for results
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### Original Text")
                    st.success(text)

                # 2. Translation
                translated_text = GoogleTranslator(source='auto', target=target_code).translate(text)
                
                with col2:
                    st.markdown(f"### Translated ({target_lang})")
                    st.info(translated_text)

                # 3. Text to Speech (Synthesis)
                st.markdown("---")
                st.markdown("### 🔊 Audio Output")
                tts = gTTS(text=translated_text, lang=target_code)
                tts_fp = BytesIO()
                tts.write_to_fp(tts_fp)
                st.audio(tts_fp, format="audio/mp3")

            except sr.UnknownValueError:
                st.error("Sorry, I couldn't understand the audio. Please try speaking clearer.")
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
