# Take5
A project built during Hack the North 2024. Completed in a 36-hour period using AI facial landmark tracking.

## Setup
1. Install the following dependencies:
```
pip install -q mediapipe
pip install pynput
pip install mouse
pip install ctypes
pip install pyautogui
pip install playsound
pip install pygame
pip install pystray
pip install pillow
```
2. Clone the GitHub repository : ```git clone https://github.com/b3ruan5483/Take5.git```

3. Run main.py.

4. Click the app on the tray!


## Inspiration
Our generation, ourselves included, spend copious amounts of time in front of our computers. It’s not a good habit to have, but simply put, building the self-control to wrench oneself away from the screen is quite boring!

## What it does
Take5 is an innovative app that records the user’s movements when browsing and identifies instances of subpar browsing behaviour - leaning in too far, straining your eyes, staying at your computer too long - and corrects the user through a variety of possible penalties. All the while, an AI bot will verbally inform users whenever they demonstrate signs of poor posture, further teaching users to build good browsing habits. Additionally, the app uses facial landmark data to predict if the user yawns or closes their eyes for a prolonged period and recommends that the user take a break whenever such an instance is detected.

## How we built it
| Tool 				| Description 			|
| ------ 				| ---------------- 		|
| OpenCV 			| Camera recording.      |
| MediaPipe 			| Face tracking           	|
| Numpy			| Calculating co-ordinates	|
| Pystray 			| Tray application 		|
| Pynput 			| Mouse & keyboard control	|
| Threading			| Running tray application	|
| Python Imaging Library 	| Application visuals		|
| Time				| Tracking elapsed time	|
| Pyautogui			| Mouse & keyboard actions	|
| Ctypes			| Locking computer		|
| Pygame			| Playing audio			|
| Math				| Calculating distances	|
| Groq				| Text generation		|
| AWS				| Text-to-speech		|

## Challenges we ran into
1. Devpost deleted our first markdown submission 
2. Struggled with a variety of mouse modules, including pynput and mouse
3. Accessing the wrong camera - MacBooks can access iPhone cameras
4. Debugging global state storage systems was a pain
5. Coming up with an idea

## Accomplishments that we're proud of
1. Creating an algorithm to calculate the user’s distance from the screen based on just webcam footage. 
2. Creating an AI bot using Groq and AWS in about an hour

## What we learned
1. Various new technologies, including the specific mediapipe solutions, Groq, and PyAutoGUI.
2. The art of pivoting to better ideas, even if that means starting over.

## What's next for Take5
Further implementation of a chatbot which gives advice about healthy habits while studying. More variety of punishments and punishable behaviours.
