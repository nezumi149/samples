import pygsheets
import speech_recognition as sr
import speech
import time

# Start a google project and set up service authorization
gc = pygsheets.authorize(service_file = './client_secret.json')
sh = gc.open('mysheet1')
wks = sh.sheet1 # default to sheet 1

debug = False

def set(row, column, value):
    wks.update_value((row, column), value)

def load_coordinates():
    positions = {}
    for row in wks.get_all_values('matrix','ROWS',False, False):
        '''TODO: should add type verification here?  rows[0] and [1] are ints,
        positions should be string'''
        positions[row[2]] = (int(row[0]),int(row[1]))
    return positions

def recognize_continuous():
    coordinate_set = load_coordinates()
    
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    while(True):
        time.sleep(0.1)
        transcriptions = speech.recognize_from_mic(recognizer, microphone)
        if debug:
            print(transcriptions)
        if not transcriptions["transcription"]:
            continue
        if speech.attempt_click(transcriptions):
            continue
        if speech.attempt_recording(transcriptions, wks):
            continue
        if speech.attempt_scroll(transcriptions):
            continue
        if speech.attempt_cards(transcriptions):
            continue

if __name__ == "__main__":
    recognize_continuous()
