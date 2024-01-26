import whisper
import time

# Ange sökvägen till din video
video_file = "ditt-filnamn.filtyp"

def transcribe_video(file_path):
    model = whisper.load_model("medium")
    result = model.transcribe(file_path)
    return result

def format_srt(segments):
    srt_format = ""
    counter = 1

    for segment in segments:
        start_time = segment['start']
        end_time = segment['end']
        text = segment['text']

        # Formatera tidsstämplarna
        start_timestamp = time.strftime('%H:%M:%S,', time.gmtime(start_time)) + f"{int(start_time % 1 * 1000):03}"
        end_timestamp = time.strftime('%H:%M:%S,', time.gmtime(end_time)) + f"{int(end_time % 1 * 1000):03}"

        srt_format += f"{counter}\n{start_timestamp} --> {end_timestamp}\n{text.strip()}\n\n"
        counter += 1

    return srt_format

# Starta tidtagning
start_time = time.time()

# Transkribera videon
transcription_result = transcribe_video(video_file)

# Skapa SRT text från transkriptionens segment
srt_text = format_srt(transcription_result['segments'])

# Spara SRT text till en fil
with open("undertexter.srt", "w") as file:
    file.write(srt_text)

# Beräkna och skriv ut total tid för processen
total_time_seconds = time.time() - start_time
print(f"Total tid för processen: {total_time_seconds / 60:.2f} minuter")
