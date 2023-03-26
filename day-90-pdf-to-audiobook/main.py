import os
import requests
from pdfminer.high_level import extract_text
from pdfminer.pdfparser import PDFSyntaxError

# Constant for PDF parsing
PDF_FILE_PATH = "_machine-learning-models.pdf"
# Constants for text-to-speech processing
BASE_URL = "https://api.voicerss.org/"  # using Voice RSS API
VOICERSS_API_KEY = os.environ.get("VOICERSS_API_KEY")
LANG = "en-us"
AUDIO_CODEC = "MP3"
TEXT_SECTION_SIZE = 1000


class TTSClient:
    """ Text-to-speech client to handle interaction with Voice RSS API """
    def __init__(self, lang, codec, voice=None):
        self.base_params = {
            "hl": lang,
            "c": codec
        }
        if voice:
            self.base_params["voice"] = voice

    def convert_text(self, text_to_convert):
        """ Convert text to audio binary by making request to Voice RSS API """
        tts_params = self.base_params
        tts_params["key"] = VOICERSS_API_KEY
        tts_params["src"] = text_to_convert
        response = http_get_request(tts_params)
        return response.content


# Helper functions
def http_get_request(params):
    """ Make HTTP GET request """
    response = requests.get(
        BASE_URL,
        params=params
    )
    response.raise_for_status()
    return response


def convert_text_to_speech(text):
    """ Call function to convert text to audio binary; raise any errors """
    try:
        return tts_client.convert_text(text)
    # catch all HTTP/connectivity exceptions from requests module
    except (requests.exceptions.HTTPError, requests.exceptions.RequestException) as e:
        raise SystemExit(e)


# Instantiate API client
tts_client = TTSClient(LANG, AUDIO_CODEC)
try:
    # Extract text to be synthesized from PDF
    all_text = extract_text(PDF_FILE_PATH)
except FileNotFoundError:
    raise SystemExit("Error: File not found. Make sure you are passing in a valid PDF file as input.")
except PDFSyntaxError:
    raise SystemExit("Error: Not a valid PDF file.")

audio = b''  # initialize empty byte string
idx = 0
# loop through text in chunks of size TEXT_SECTION_SIZE to avoid URI too long errors
while idx < len(all_text):
    text_section = all_text[idx:idx+TEXT_SECTION_SIZE]
    audio += convert_text_to_speech(text_section)
    idx += TEXT_SECTION_SIZE

# Write binary audio data to mp3 file
with open('output.mp3', 'wb') as out:
    out.write(audio)
    print('Done writing audio content to file "output.mp3"')
