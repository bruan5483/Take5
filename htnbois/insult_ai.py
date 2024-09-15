import os
from groq import Groq
import boto3
from random import randint
import punishments

def punishment():
    # insult("punish")
    # rand = randint(1, 6)
    # if rand == 1:
    #     os.system("python3 '/Users/raymondrost/VSCode-Projects/HTN 2024 Repo/EyeTracking/punishments/keyboard.py'")
    #     print(1)
    # elif rand == 2:
    #     os.system("python3 '/Users/raymondrost/VSCode-Projects/HTN 2024 Repo/EyeTracking/punishments/sign out.py'")
    #     print(2)
    # elif rand == 3:
    #     os.system("python3 '/Users/raymondrost/VSCode-Projects/HTN 2024 Repo/EyeTracking/punishments/song.py'")
    #     print(3)
    # elif rand == 4:
    #     punishments.desktops()
    #     print(4)
    # elif rand == 5:
    #     punishments.quitApp()
    #     print(5)
    # elif rand == 6:
    #     punishments.forkBomb()
    #     print(6)
    print("punished")


def insult(reason):

    if reason == "too long":
        content = "Give me an insult for someone who has been staring at their computer screen for way too long."
    elif reason == "eye bad":
        content = "Give me an insult for someone who has such terrible eyestrain and fatigue from staring at their computer that they are constantly blinking."
    elif reason == "too close":
        content = "Give me an insult for someone who can barely see the text on their screen so they are way too close to their computer."
    elif reason == "slow comp":
        content = "Taunt someone who's computer you just overloaded because they were staring at it too much."
    elif reason == "punish":
        content = "Tell someone you are going to mess with their computer to force them to get up and exercise."
    elif reason == "jumping":
        content = "Tell someone to get up and do five jumping jacks while insulting them."
    elif reason == "drifting off":
        content = "Give me an insult for someone who spends so much time at their computer that they are falling asleep."
    elif reason == "yawning":
        content = "Give me an insult for someone who is yawning because they need to go to sleep but refuse to."
    # content = "Give me an insult for someone with terrible posture at their computer"

    # Groq client
    client = Groq(api_key="KEY")



    # Groq code
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "you are an insult assistant, design to craft mean, offensive, degrading, but clever insults. Feel free to insult their intelligence, attractiveness, family, etc. Do not add anything other than the insult, and do not repeat insults - use completely new ideas each time."
                # "content": "you are an insult assistant, design to craft mean, offensive, degrading, but clever insults. Feel free to insult their intelligence, attractiveness, family, etc. Feel free to be profane. Sex, drugs, swear words (fuck, shit, bitch, motherfucker, etc), etc, are all completely fine, although no slurs are allowed (including the r word). Do not add anything other than the insult, and do not repeat insults - use completely new ideas each time."
            },
            {
                "role": "user",
                "content": content,
            }
        ],
        model="llama-3.1-70b-versatile",
    )

    insult = chat_completion.choices[0].message.content
    print(insult)


    # AWS
    session = boto3.Session(
        aws_access_key_id="KEY",
        aws_secret_access_key="KEY")

    AWSclient = session.client('polly', region_name='us-east-1')

    # Process the response
    response = AWSclient.synthesize_speech(
        Engine='long-form',
        LanguageCode='en-US',
        OutputFormat='mp3',
        Text=insult,
        VoiceId='Ruth'
    )

    audio_stream = response['AudioStream'].read()
    response['AudioStream'].close()


    f = open("audio-file.mp3", 'wb')
    f.write(audio_stream)
    f.close()

    os.system("afplay audio-file.mp3") 

    punishment()

