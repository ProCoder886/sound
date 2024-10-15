import streamlit as st
from elevenlabs.client import ElevenLabs
import os

# Initialize ElevenLabs API
elevenlabs = ElevenLabs(api_key="sk_2d411adbba65948d83eed8a108e16caa48e7d42edfa24389")

# Streamlit app code
st.title("AI Sound Effect Generator")
text_prompt = st.text_input("Enter a text prompt to generate a sound effect:")

if st.button("Generate Sound"):
    if text_prompt:
        # Define the output path
        output_filename = f"{text_prompt.replace(' ', '_')}.mp3"
        output_path = os.path.join("downloads", output_filename)
        os.makedirs("downloads", exist_ok=True)

        # Generate the sound effect
        result = elevenlabs.text_to_sound_effects.convert(
            text=text_prompt,
            duration_seconds=5,
            prompt_influence=0.5,
        )

        # Save the generated sound effect to a file
        with open(output_path, "wb") as f:
            for chunk in result:
                f.write(chunk)

        st.success("Sound effect generated!")
        st.audio(output_path, format="audio/mp3")
        st.download_button("Download MP3", file_name=output_filename, data=open(output_path, "rb").read())
    else:
        st.error("Please enter a valid text prompt.")
