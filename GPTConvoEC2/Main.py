
from GPTConvo import *
from VoiceGenerator import *
from ScriptParser import *
import threading
from LocalZipper import *
from StreamLabsClient import *
import os
import platform
from pathlib import Path


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


gptConvo = GPTConvo(get_api_key())
localZipper.deleteResults();

voiceGens = [
    VoiceGenerator(8000),
    VoiceGenerator(8001)
    # Add more voice generators if needed
]

voiceDispatcher = VoiceGeneratorManager(voiceGens)


#====================================================================

import time
from concurrent.futures import ThreadPoolExecutor

def generate_scripts(queue):
    while True:
        try:
            print("Generating Script")
            if (queue.qsize() > 2):
                time.sleep(30)
            script = gptConvo.callGPTForOneOffScript()
            parser = ScriptParser(script, gptConvo.scriptBuilder.charNames)
            unityScript = parser.getUnityScript()
            queue.put((parser.lines, unityScript))  # Add the lines and unityScript to the queue
            time.sleep(10)
        except Exception as ex:
            print(ex)
            time.sleep(1)


def process_scripts(queue):
    while True:
        if not queue.empty():
            lines, unityScript = queue.get()  # Get the lines and unityScript from the queue
            voiceDispatcher.run(lines)
            localZipper.zipFiles('/home/ubuntu/gptconvo/ai-voice-cloning/results',unityScript, [line.character for line in lines])
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


