## Transkribera med Whisper API

### Steg 1 - Se till att du har Python installerat på din dator
Kör `python3 --version` i terminalen

### Steg 2 - Installera bödvändiga bibliotek
Du hittar allt som behövs på [Whisper API's git](https://github.com/openai/whisper)

### Steg 3 - Skriv in ditt filnamn (se till att filen är i samma mapp som skriptet)
`video_file = "ditt-filnamn.filtyp"` 
`model = whisper.load_model("medium")`

### Steg 4 - Kör `python3 transcribe.py` i terminalen