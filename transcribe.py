import whisper
import textwrap
import time

start_time = time.time()  # Startar tidtagningen (för referens om hur)


# Steg 1 
def transcribe_video(file_path):
    model = whisper.load_model("medium")  # Eller en annan modellstorlek som 'small', 'medium', 'large'
    result = model.transcribe(file_path)
    return result['text']

video_file = "ditt-filnamn.filtyp"  # Byt ut mot sökvägen till din ljudfil
transcribed_text = transcribe_video(video_file)

# Steg 2
def chunk_text(text, max_length=50): #Dela upp text i mindre bitar
    chunks = textwrap.wrap(text, max_length)
    return chunks

chunks = chunk_text(transcribed_text)

# Steg 3
def format_srt(chunks, char_per_second=15):  # tecken per sekund 
    srt_format = ""
    start_time = 0
    for i, chunk in enumerate(chunks, 1):
        # Uppskattar varaktigheten baserat på antalet tecken
        duration = len(chunk) / char_per_second
        end_time = start_time + duration

        # Formaterar tidsstämplarna för Youtube
        start_timestamp = f"{int(start_time//3600):02}:{int((start_time%3600)//60):02}:{int(start_time%60):02},000"
        end_timestamp = f"{int(end_time//3600):02}:{int((end_time%3600)//60):02}:{int(end_time%60):02},000"

        srt_format += f"{i}\n{start_timestamp} --> {end_timestamp}\n{chunk}\n\n"
        start_time = end_time

    return srt_format

srt_text = format_srt(chunks)
print(srt_text)

# Steg 4
with open("undertexter.srt", "w") as file:
    file.write(srt_text)

# Beräkna total tid
end_time = time.time() # Avsluta tidtagningen 
total_time_seconds = end_time - start_time
total_time_minutes = total_time_seconds / 60  # Konverterar tiden till minuter
print(f"Total tid för processen: {total_time_minutes:.2f} minuter")
