from flask import Flask, render_template, request, send_file
from google.cloud import texttospeech
import csv, random, os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "ersatzspaghetti-3593cff43659.json"

app = Flask(__name__)
client = texttospeech.TextToSpeechClient()

number = 0
pastas = []
with open("twitchgen.tsv") as fd:
    rd = csv.reader(fd, delimiter="\t", quotechar='"')
    for row in rd:
        pastas+=row


@app.route("/",methods=['GET', 'POST'])
def home():
    return render_template("defaultdance.html")

@app.route("/parse",methods=['GET', 'POST'])
def play():

    for file in os.listdir("static"):
        if file.endswith(".mp3"):
            os.remove("static/"+file)

    #get pasta
    text = random.choice(pastas)
    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    print(response)


    name = "static/temp"+str(random.randint(0,10000000))+".mp3"

    with open(name, "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')

    return render_template("playpage.html",words=text,track_ogg=name,track_mp3=name)


if __name__ == "__main__":
    app.run(debug=True)
