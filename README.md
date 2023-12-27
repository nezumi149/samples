## Custom speech recognition package

Inspired by common uses of speech recognition in popular operating systems, this script aims to allow specific custom commands.  For example, the list of commands for Windows Speech can be found [here](https://support.microsoft.com/en-us/windows/windows-speech-recognition-commands-9d25ef36-994d-f367-a81a-a326160128c7).  For this project, four basic commands are used:

* 'Record' indicates a pixel of the screen to record for later use.
* 'Punch' indicates a click, but 'click' and 'quick' have very similar phonemes so 'punch' is used to eliminate ambiguity.
* 'Scroll' is a mouse wheel scroll
* Finally, 'Punch Card n' indicates a use within the MTGA app - click on the nth playable (highlighted) card in the app.

## Dependencies

Libaries used: pygsheets, speech_recognition, time, datetime, pywin32, pyautogui.  Additionally, users will need a google API authorization (referenced as client_secret.json)
