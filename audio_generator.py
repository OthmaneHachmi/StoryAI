import os
from io import BytesIO
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv

class AudioGenerator:
    def __init__(self):
        load_dotenv()
        self.client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

    def generate_audio(self, text: str, voice: str) -> BytesIO:
        """Convert text to speech. Returns a BytesIO audio stream."""
        try:
            response = self.client.text_to_speech.convert(
                voice_id=voice,
                output_format="mp3_22050_32",
                text=text,
                model_id="eleven_multilingual_v2",
                voice_settings=VoiceSettings(
                    stability=0.4,
                    similarity_boost=0.9,
                    style=0.0,
                    use_speaker_boost=True,
                ),
            )

            audio_stream = BytesIO()
            for chunk in response:
                if chunk:
                    audio_stream.write(chunk)
            audio_stream.seek(0)
            return audio_stream

        except Exception as e:
            raise RuntimeError(f"Audio generation failed: {str(e)}")