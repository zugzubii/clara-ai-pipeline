import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def transcribe_audio(audio_filepath):
    """Converts audio file to text using Groq Whisper"""
    
    print(f"🎙️ Transcribing: {audio_filepath}")
    
    with open(audio_filepath, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-large-v3",
            file=audio_file,
            response_format="text"
        )
    
    print("✅ Transcription complete!")
    return transcription

def save_transcript(text, output_filepath):
    """Saves the transcript as a .txt file"""
    os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
    with open(output_filepath, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"✅ Transcript saved to: {output_filepath}")

if __name__ == "__main__":
    # Transcribe Ben's Electric audio
    audio_path = "../data/audio1975518882.m4a"
    output_path = "data/demo_ACC-001.txt"
    
    transcript = transcribe_audio(audio_path)
    save_transcript(transcript, output_path)
    
    print("\n--- TRANSCRIPT PREVIEW ---")
    print(transcript[:500])  # Show first 500 characters