
from curses import meta
from importlib import metadata
from site import getsitepackages
from GPTConvo import *
from VoiceGenerator import *
from ScriptParser import *
import threading
from LocalZipper import *
from StreamLabsClient import *
import os
import platform
from pathlib import Path
import signal
import json


localZipper = LocalFileZipper() 

def load_api_key(file_path):
    if not os.path.exists(file_path):
        print(f"File {file_path} not found.")
        return None

    with open(file_path, 'r') as file:
        return file.read().strip()


def get_api_key():
    if platform.system() == 'Linux':
        return load_api_key("/home/ubuntu/gptconvo/gptconvo/GPTSECRET.txt")
    elif platform.system() == 'Windows':
        return os.getenv("OPEN_AI_API_KEY")

def get_episode_number():
    file_path = "/home/ubuntu/gptconvo/gptconvo/episodeNumber.txt"
    
    # Ensure the directory exists, if not, create it
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # If the file does not exist, create it with the number '1'
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            file.write('1')
        return 1

    # If the file exists, read the number, increment and write it back
    with open(file_path, 'r') as file:
        episode_number = int(file.readline().strip())

    with open(file_path, 'w') as file:
        file.write(str(episode_number + 1))
    
    return episode_number

gptConvo = GPTConvo(get_api_key())
localZipper.deleteResults();

voiceGens = [
    VoiceGenerator(8000),
    VoiceGenerator(8001)
    # Add more voice generators if needed
]

voiceDispatcher = VoiceGeneratorManager(voiceGens)
kill_fuzzy_buddies = False

def signal_handler(sig, frame):
    global kill_fuzzy_buddies
    print('Received shutdown signal. Closing Fuzzy Buddies...')
    kill_fuzzy_buddies = True
    for voice in voiceGens:
        voice.killVoiceCloner();
    exit(0)

signal.signal(signal.SIGUSR1, signal_handler)

#====================================================================

import time
from concurrent.futures import ThreadPoolExecutor

def generate_scripts(queue):
    while not kill_fuzzy_buddies:
        try:
            if (queue.qsize() > 2):
                time.sleep(1)
                continue

            print("Generating Script")
            script, dono = gptConvo.callGPTForOneOffScript()
            parser = ScriptParser(script, gptConvo.scriptBuilder.charNames)
            unityScript = parser.getUnityScript()
            metaData = {}
            if dono is not None :
                metaData['donation'] = dono.to_dict()
            queue.put((parser.lines, unityScript, metaData))  # Add the lines and unityScript to the queue
            time.sleep(10)
        except Exception as ex:
            print(ex)
            time.sleep(1)


def process_scripts(queue):
    while not kill_fuzzy_buddies:
        if not queue.empty():
            lines, unityScript, metaData = queue.get()  # Get the lines and unityScript from the queue
            voiceDispatcher.run(lines)
            metaData['epNumber'] = get_episode_number();
            localZipper.zipFiles('/home/ubuntu/gptconvo/ai-voice-cloning/results',
                                 unityScript, 
                                 metaData, 
                                 [line.character for line in lines])
        else:
            time.sleep(1)  # Wait for 1 second before checking the queue again


# Use a thread-safe queue to hold the scripts
queue = queue.Queue()

# Use a ThreadPoolExecutor to run the tasks in separate threads
with ThreadPoolExecutor(max_workers=2) as executor:
    executor.submit(generate_scripts, queue)
    executor.submit(process_scripts, queue)


while threading.active_count() > 1:
    time.sleep(1)


