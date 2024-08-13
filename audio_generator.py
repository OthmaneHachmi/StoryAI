import os
from typing import IO
from io import BytesIO
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs

class AudioGenerator:
    def __init__(self):

        self.client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))


    def generate_audio(self, text: str, voice) -> IO[bytes]:
        # Perform the text-to-speech conversion
        response = self.client.text_to_speech.convert(
            voice_id=voice,
            output_format="mp3_22050_32",
            text=text,
            model_id="eleven_multilingual_v2",
            voice_settings=VoiceSettings(
                stability=0.0,
                similarity_boost=1.0,
                style=0.0,
                use_speaker_boost=True,
            ),
        )

        # Create a BytesIO object to hold the audio data in memory
        audio_stream = BytesIO()

        # Write each chunk of audio data to the stream
        for chunk in response:
            if chunk:
                audio_stream.write(chunk)

        # Reset stream position to the beginning
        audio_stream.seek(0)

        # Return the stream for further use
        return audio_stream

