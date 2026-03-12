import os
from pathlib import Path
from sarvamai import SarvamAI
from sarvamai.play import save
from agent.adk_client import ask_agent


def transcribe_audio(file_path: str) -> str:
    api_key = os.environ.get("SARVAM_API_KEY")
    if not api_key:
        raise RuntimeError("SARVAM_API_KEY not set")
    client = SarvamAI(api_subscription_key=api_key)
    with open(file_path, "rb") as f:
        response = client.speech_to_text.transcribe(
            file=f,
            model="saaras:v2.5",
        )
    return response.get("transcript", "")


def synthesize_voice(text: str, out_path: str) -> str:
    api_key = os.environ.get("SARVAM_API_KEY")
    if not api_key:
        raise RuntimeError("SARVAM_API_KEY not set")
    client = SarvamAI(api_subscription_key=api_key)
    audio = client.text_to_speech.convert(
        target_language_code="en-IN",
        text=text,
        model="bulbul:v2",
        speaker="anushka",
    )
    save(audio, out_path)
    return out_path


def handle_voice_query(file_path: str) -> str:
    transcript = transcribe_audio(file_path)
    answer = ask_agent(transcript) or "No response from agent."
    return answer


if __name__ == "__main__":
    print("NHRIS Sarvam Voice")
    audio_path = input("Audio file path: ").strip()
    if audio_path:
        answer = handle_voice_query(audio_path)
        print("Transcript + Answer:", answer)
        out = Path("data/alerts/voice_response.wav")
        out.parent.mkdir(parents=True, exist_ok=True)
        synthesize_voice(answer, str(out))
        print(f"Saved voice response -> {out}")
