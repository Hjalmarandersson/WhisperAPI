import whisper
import time

# Starta tidtagning
start_time = time.time()

# Ange sökvägen till din video
video_file = "video_file"

def transcribe_video(file_path, logprob_threshold=-2.5, temperature=0.0):
    model = whisper.load_model("model")
    # Anpassa logprob_threshold och temperature enligt behov
    result = model.transcribe(file_path, logprob_threshold=logprob_threshold, temperature=temperature)
    return result

# Transkribera videon med anpassade parametrar för mindre segment
transcription_result = transcribe_video(video_file)

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

def find_natural_break(text, approximate_index):
    # Justera för att inte gå utanför textsträngens gränser
    start_index = max(0, min(approximate_index, len(text) - 1))
    
    # Om vi redan är på ett mellanslag eller skiljetecken
    if text[start_index] in " .,;!?\n":
        return start_index
    
    # Sök bakåt från start_index
    for i in range(start_index, max(0, start_index - 10), -1):
        if text[i] in " .,;!?\n":
            return i
    # Sök framåt från start_index
    for i in range(start_index + 1, min(len(text), start_index + 10)):
        if text[i] in " .,;!?\n":
            return i
    return start_index  # Använd start_index om ingen paus hittas

# Max_duration är för hur lång en undertext får vara 8 = 8 sekunder. Längre tal passar vertikala videos.
def split_long_segments(segments, max_duration=8):
    new_segments = []
    for segment in segments:
        duration = segment['end'] - segment['start']
        if duration > max_duration:
            parts = int(duration / max_duration) + 1
            part_duration = duration / parts
            current_start_time = segment['start']

            for part in range(parts - 1):  # Hantera alla delar förutom den sista
                part_end_time = current_start_time + part_duration
                break_point = find_natural_break(segment['text'], len(segment['text']) // parts * (part + 1))
                new_segment = {
                    'start': current_start_time,
                    'end': part_end_time,
                    'text': segment['text'][:break_point].strip()
                }
                new_segments.append(new_segment)
                # Förbered texten för nästa segment
                segment['text'] = segment['text'][break_point:].strip()
                current_start_time = part_end_time
            
            # Lägg till det sista segmentet
            new_segments.append({
                'start': current_start_time,
                'end': segment['end'],
                'text': segment['text'].strip()
            })
        else:
            new_segments.append(segment)
    return new_segments


# Använd den modifierade listan av segment för att skapa SRT-filen
modified_segments = split_long_segments(transcription_result['segments'])
srt_text = format_srt(modified_segments)

# Spara SRT text till en fil
with open(video_file + "-" + "undertexter.srt", "w") as file:
    file.write(srt_text)

# Beräkna och skriv ut total tid för processen
total_time_seconds = time.time() - start_time
minutes = int(total_time_seconds // 60)
seconds = int(total_time_seconds % 60)
print(f"Total tid för processen: {minutes} minuter och {seconds} sekunder")
