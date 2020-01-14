# Sound_Avatar.py

## System Overview
![Diagram](src/SoundSocketDiagram.JPG)

## requirement
-  Miniconda : https://docs.conda.io/en/latest/miniconda.html 
-  Create env Python 3.6 : "conda create -n myenv python=3.6"
- PyAudio : "pip install PyAudio"

## How to install pyaudio:
Follow this: https://stackoverflow.com/questions/52283840/i-cant-install-pyaudio-on-my-python-how-to-do-it/55630212

## How to use this: 
1. Wait for the server open. [User must setting the serverAddressPort ("IP")](first parameter) 
- Ex: python Sound_Server.py 1.2.3.4
2. Run the Communication Module Client Code.
3. Finish XD !!!!

## Warning!!!!!
Don't forget to check and change *server* IP every time.[Change at 1st parameter)]

# Stereo Cable Structure
![Diagram](src/Strereo CABLE STRUCTURE_ Xprize.JPG)

## Stereo Cable info
Separate Channels of Microphone by get sound signal from tip of (TS and TRS)Mic and put that signal to Right and Left(Tip and Ring of TRS Male Jack
- Warning : This cable doesn't Support TRRS Mic
