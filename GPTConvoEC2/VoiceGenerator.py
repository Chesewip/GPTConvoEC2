from gradio_client import Client
from ScriptParser import *
import threading
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
from typing import List
import time
import subprocess
import requests


class VoiceGenerator:

    def __init__(self, port):

        self.url = "http://127.0.0.1:" + str(port)
        self.port = port
        self.launchNewVoiceCloner(port)

        self.input_prompt = ""
        self.line_delimiter = "\\n"
        self.emotion = None
        self.custom_emotion = None
        self.voice = "Random"
        self.microphone_source = None
        self.voice_chunks = 1
        self.candidates = 1
        self.seed = None
        self.samples = 2
        self.iterations = 16
        self.temperature = 1.0
        self.diffusion_samplers = "DDIM"
        self.pause_size = 8
        self.cvvp_weight = 0
        self.top_p = 0.8
        self.diffusion_temperature = 1
        self.length_penalty = 7.0
        self.repetition_penalty = 5.0
        self.conditioningfree_k = 2
        self.experimental_flags = ["Conditioning-Free"]
        self.use_original_latents_method_ar = False
        self.use_original_latents_method_diffusion = False
        self.api = "/generate"

    def is_gradio_alive(self):
        try:
            response = requests.get(self.url)
            return response.status_code == 200
        except:
            return False

    def generateLines(self, lines, voice):
        for line in lines:
            self.generateLine(line, voice)

    def generateLine(self, text, voice):

        if self.is_gradio_alive() == False:
            self.launchNewVoiceCloner(self.port)
            self.client = Client(self.url)

        if voice == "Gabbi":
            self.seed = 1;
        else:
            self.seed = None;

        if text == "":
            return

        try:
            result = self.client.predict(
            text,
            self.line_delimiter,
            self.emotion,
            self.custom_emotion,
            voice,
            self.microphone_source,
            self.voice_chunks,
            self.candidates,
            self.seed,
            self.samples,
            self.iterations,
            self.temperature,
            self.diffusion_samplers,
            self.pause_size,
            self.cvvp_weight,
            self.top_p,
            self.diffusion_temperature,
            self.length_penalty,
            self.repetition_penalty,
            self.conditioningfree_k,
            self.experimental_flags,
            self.use_original_latents_method_ar,
            self.use_original_latents_method_diffusion,
            api_name = self.api
        )
            print("File Generated")
        except:
            print("File Generated, return failed though?")


    def launchNewVoiceCloner(self, port):
        print("Starting New Voice Cloner")
        try:
            self.client = Client(self.url)
            print("Server already active")
        except:
            command = ['bash', '-c', f'cd /home/ubuntu/gptconvo/ai-voice-cloning && ./start.sh --port {port}']
            process = subprocess.Popen(command)
    
            # Give the process some time to start
            time.sleep(50)
            self.client = Client(self.url)


import threading
import queue

class VoiceGeneratorWorker:
    def __init__(self, voiceGen):
        self.voiceGen = voiceGen
        self.queue = queue.Queue()
        self.thread = None

    def add_line(self, line):
        self.queue.put(line)

    def _run(self):
        while True:
            line = self.queue.get()  # Blocks until a line is available
            if line is None:  # We send None to signal the worker to stop
                break
            self.voiceGen.generateLine(line.dialogue, line.character)

    def run(self):
        self.thread = threading.Thread(target=self._run)
        self.thread.start()


class VoiceGeneratorManager:
    def __init__(self, voiceGens):
        # Create the workers
        self.workers = [VoiceGeneratorWorker(voiceGen) for voiceGen in voiceGens]
        self.char_to_worker = {}

    def assign_character_to_worker(self, character):
        if character not in self.char_to_worker:
            # Assign the character to the worker with the least characters so far
            self.char_to_worker[character] = min(self.workers, key=lambda worker: len([c for c, w in self.char_to_worker.items() if w == worker]))

    def dispatchGenerators(self, dialogueLines):
        # Start the worker threads
        for worker in self.workers:
            worker.run()

        # Assign characters to workers
        for line in dialogueLines:
            self.assign_character_to_worker(line.character)

        # Dispatch lines to workers
        for line in dialogueLines:
            worker = self.char_to_worker[line.character]
            worker.add_line(line)

        # When done, add None to signal the workers to stop
        for worker in self.workers:
            worker.queue.put(None)

        # Wait for all workers to finish
        for worker in self.workers:
            worker.thread.join()


    def run(self, dialogueLines):
        self.dispatchGenerators(dialogueLines)






