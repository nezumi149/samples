import utilities
from datetime import datetime
import pytz
import mtga
import gsheetssandbox

TIMEZONE = 'America/Juneau'
SCROLL_DISTANCE = 1400

numerals = ['zero','one', 'two', 'three', 'four','five','six','seven','eight','nine','ten','eleven','twelve','thirteen']
numbers = [str(i) for i in range(0,10)]

debug = False

'''recognize_from_mic()
Base speech recognition method, using google speech API
Source: https://realpython.com/python-speech-recognition/
'''
def recognize_from_mic(r, mic):
    with mic as source:
        r.adjust_for_ambient_noise(source)
        print('listening...')
        audio = r.listen(source)

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    try:
        response["transcription"] = r.recognize_google(audio, show_all=True)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"
        
    return response

'''accept_phrase()
@param phrase: string to match
@param transcriptions: transcription object from speech recognizer,contains
transcription / probability pairs
returns: True if there is an exact match in the transcriptions (any probability)
'''
def accept_phrase(phrase, transcriptions):
    if not transcriptions['success'] or not transcriptions['transcription']:
        return False
    for item in transcriptions['transcription']['alternative']:
        if item['transcript'] == phrase:
            return True
    return False

'''accept_prefix()
@param phrase: string to be accepted as a prefix of the transcription
@param transcriptions: transcription object from speech recognition
returns: for each phrase that is a case-insensitive starting substring (prefix)
in transcriptions, returns suffix
'''
def accept_prefix(phrase, transcriptions):
    if not transcriptions['success'] or not transcriptions['transcription']:
        return False
    suffixes = []
    for item in transcriptions['transcription']['alternative']:
        guess = item['transcript'].lower()
        if guess.startswith(phrase):
            suffixes.append(guess[len(phrase):])
    return suffixes

'''attempt_click()
@param transcriptions: transcription object from speech recognition
if transcription is found with prefix "punch " then we punch (click) the
corresponding button on the screen.  The button location is referenced
from google sheets
'''
def attempt_click(transcriptions):
    double_click = False
    suffixes = accept_prefix('punch ', transcriptions)
    if not suffixes:
        suffixes = accept_prefix('double punch ', transcriptions)
        double_click = True
    if not suffixes:
        return False

    # one or more suffixes - in otherwords, we need to click.  First, load new coordinate set
    coordinate_set = gsheetssandbox.load_coordinates()
    
    for suffix in suffixes:
        if suffix in coordinate_set:
            if double_click:
                utilities.leftDoubleClickCord(coordinate_set[suffix])
            else:
                utilities.leftClickCord(coordinate_set[suffix])
            return True
        
'''attempt_recording()
@param transcriptions: transcription object from speech recognition
@param wks: google worksheet to store name / coordinate pairs
if transcription is found with prefix "record " then we record the current
location to google sheets wish suffix as key
'''
def attempt_recording(transcriptions, wks):
    suffixes = accept_prefix('record ', transcriptions)
    if not suffixes:
        return False
    TZ = pytz.timezone(TIMEZONE)
    cord = utilities.get_cords()
    print("record")
    wks.insert_rows(0,1,[cord[0], cord[1], suffixes[0], datetime.now(TZ).strftime('%m/%d/%Y')])
    return True

'''attempt_scroll()
if transcription is found with prefix "scroll " then we do a scroll down.  Could
customize for scroll distance later.  Same as Windows Speech 'scroll up' and
'scroll down' commands.
'''
def attempt_scroll(transcriptions):
    suffixes = accept_prefix('scroll ', transcriptions)
    if not suffixes:
        return False
    if 'up' in suffixes:
        utilities.scroll(SCROLL_DISTANCE)
    if 'down' in suffixes:
        utilities.scroll(-1*SCROLL_DISTANCE)
    return True

'''attempt_cards()
if transcription is found with prefix "punch card " then based on the following
following positive integer, click the corresponding card in th  mtga client.
'''
def attempt_cards(transcriptions):
    suffixes = accept_prefix('punch card ', transcriptions)
    print(suffixes)
    for num in numbers:
        if num in suffixes:
            mtga.click_card_x(numbers.index(num))
            return True
    for num in numerals:
        if num in suffixes:
            mtga.click_card_x(numerals.index(num))
            return True
    return False

if __name__ == "__main__":
    pass
