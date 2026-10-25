import whisper

from agents.base_agent import BaseAgent


class SpeechAgent(BaseAgent):
    """
    Speech-to-text agent using OpenAI Whisper.
    """

    def __init__(self):
        super().__init__("Speech Agent")

        print(f"Loading {self.name}...")

        # "small" is generally more accurate than "base",
        # but takes more time and memory.
        self.model = whisper.load_model("small")

        print(f"{self.name} loaded successfully!")

    def execute(self, video_path):
        """
        Transcribe the video's audio into text.
        """

        result = self.model.transcribe(
            video_path,
            task="transcribe",
            fp16=False,
            beam_size=5,
            temperature=0,
            verbose=False
        )

        print("Detected language:", result.get("language"))

        transcript = result.get("text", "").strip()

        return transcript


speech_agent = SpeechAgent()