import io
import os
import solara
from pydub import AudioSegment

@solara.component
def TranscriptPage():
    uploaded_file, set_uploaded_file = solara.use_state(None)
    processed_file_url, set_processed_file_url = solara.use_state(None)

    def on_file(file):
        set_uploaded_file(file)
        solara.Markdown("**Processing audio file...**")
        process_and_store_audio(file)

    def infer_audio_format(file: dict) -> str:
        # Try MIME type first (e.g., 'audio/wav', 'audio/mpeg')
        if "type" in file and file["type"].startswith("audio/"):
            fmt = file["type"].split("/")[-1]
            # normalize 'mpeg' to 'mp3'
            if fmt == "mpeg":
                return "mp3"
            return fmt

        # Fallback to file extension
        ext = os.path.splitext(file["name"])[-1].lower().strip(".")
        return "mp3" if ext == "mpeg" else ext or "wav"  # default to wav

    def process_and_store_audio(file):
        audio_format = infer_audio_format(file)
        print(f"Detected format: {audio_format}")

        try:
            audio = AudioSegment.from_file(io.BytesIO(file["data"]), format=audio_format)
            print("AFTER loading audio")
        except Exception as e:
            solara.Error(f"Could not decode uploaded file: {e}")
            return

        # Example: trim to 5 seconds
        processed = audio[:5000]

        print("AFTER processing audio")
        # Export to mp3 or wav
        export_format = "mp3"
        output_basename = os.path.splitext(file["name"])[0]
        output_path = f"static/processed_{output_basename}.{export_format}"
        os.makedirs("static", exist_ok=True)
        processed.export(output_path, format=export_format)

        # Set URL for playback
        set_processed_file_url("/" + output_path)

    with solara.Column():
        solara.FileDrop(label="Upload audio file", on_file=on_file)

        if uploaded_file:
            solara.Markdown(f"**Uploaded:** {uploaded_file['name']}")

        if processed_file_url:
            solara.HTML(f"""
            <audio controls autoplay>
                <source src="{processed_file_url}" type="audio/mpeg">
                Your browser does not support the audio element.
            </audio>
            """)
