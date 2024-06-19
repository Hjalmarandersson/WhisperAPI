## Transkribera med Whisper API

Kolla [min video](https://youtu.be/3tXxC_jLwW8) om Whisper API


### Steg 1 - Se till att du har Python installerat på din dator
Kör `python3 --version` i terminalen

### Steg 2 - Installera nödvändiga bibliotek
Du hittar allt som behövs på [Whisper API's git](https://github.com/openai/whisper)

### Steg 3 - Ändra variabler
`video_file` = ditt-filnamn.filtyp
`model` = small, medium, large
`max_duration` = anger den maximala längden i sekunder för varje undertextsegment från videon, med standardvärdet 8 sekunder.

### Steg 4 - Kör `python3 transcribe.py` i terminalen