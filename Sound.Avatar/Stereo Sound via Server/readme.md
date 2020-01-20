# Sound_Avatar.py

## System Overview
![Diagram](src/SoundSocketDiagram.JPG)

## requirement
-  Miniconda : https://docs.conda.io/en/latest/miniconda.html 
-  Create env Python 3.6 : "conda create -n myenv python=3.6"
- PyAudio : "pip install PyAudio"

## How to install pyaudio:
Follow this: https://pypi.org/project/PyAudio/

## How to use this: 
1. Wait for the server open. [User must setting the serverAddressPort ("IP")](first parameter) 
- python Sound_Client.py [12.34.56.78] [Input Index] [Output Index]
- python Sound_Client.py [12.34.56.78] 0 ## Default
- python Sound_Client.py [12.34.56.78] # SetDevice in Program
2. Run program

## Warning!!!!!
Don't forget to check and change *server* IP every time.[Change at 1st parameter)]

# Stereo Cable Structure
![Diagram](src/Stereo_CABLE_STRUCTURE_XPrize.JPG)

## Stereo Cable info
Separate Channels of Microphone by get sound signal from tip of (TS and TRS)Mic and put that signal to Right and Left(Tip and Ring of TRS Male Jack

*** You can use Earbuds or Headset instead Mics.
