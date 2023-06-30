from queue import Empty
import re  # import Python's regex module


class RandomEvent:
    def __init__(self, event_type, characters):
        self.event_type = event_type
        self.characters = characters


class DialogueLine:

    def __init__(self, charName,emotion,line):
        self.character = charName
        self.emotion = emotion
        self.dialogue = line
        self.random_event = None

forbidden_words = [
    "retard",
    "retarded",
    "faggot",
    "fag",
    "nigger",
    "nigga",
    "n****",
    "rape",
    "coon",
    "Breonna Taylor",
    "George Floyd",
    "Trayvon martin",
    "Nazi",
    "transgender"
    "transsexual",
    "queer",
    "jew",
    "muslim",
    "muhammad",
    "allah",
    "kike",
    "racist",
    "homophobic"
    ]

def contains_forbidden_words(text):
    for word in forbidden_words:
        if word.lower() in text.lower():
            return True
    return False

class ScriptParser:

    ##[RANDOM EVENT = STROKE Shawn]
    def __init__(self, script, valid_names):
        self.script = script
        self.valid_script_names = valid_names
        self.lines = self.parse_lines(script,valid_names)

    def parse_lines(self, script, valid_names):
        lines = []
        dLines = []
        random_event = None
        script_lines = script.split('\n')

        for line in script_lines:
            parsed_line = self.parse_line(line, valid_names)
            if isinstance(parsed_line, DialogueLine):
                if random_event:
                    parsed_line.random_event = random_event
                    random_event = None  # Reset the random event
                dLines.append(parsed_line)
            elif isinstance(parsed_line, RandomEvent):
                random_event = parsed_line  # Save the random event for the next dialogue line

        # If there's still a random event left at the end, add it as a separate line
        #if random_event:
        #    dLines.append(random_event)

        self.lines = dLines
        return dLines

    def parse_line(self, line, valid_names):

        if re.search(r'\#?\[?RANDOM EVENT', line):
            line = re.sub(r'[#\[|\]]', '', line)  # Remove '#' and '[' and ']' from the line
            return self.parse_random_event(line)

        if line.startswith("#"):
        
            line = line[1:]  # remove the leading '#'
            name_end = line.find(' ')  # find the end of the name
            name = line[:name_end]  # extract the name

            if name not in valid_names:
                return None

            # Find the end of the emotion and check for the colon
            emotion_end = line.find(')')
            if line[emotion_end + 1] != ':':
                # Insert the colon
                line = line[:emotion_end + 1] + ':' + line[emotion_end + 1:]

            emotion_start = line.find('(') + 1  # find the start of the emotion
            emotion = line[emotion_start:emotion_end]  # extract the emotion

            dialogue_start = line.find(':') + 2  # find the start of the dialogue
            dialogue = line[dialogue_start:]  # extract the dialogue

            if contains_forbidden_words(dialogue) :
                raise Exception("Profanity check failed");

            # If dialogue contains brackets, extract the information and remove it
            if '[' in dialogue and ']' in dialogue:
                bracket_info = re.search('\[(.*?)\]', dialogue).group(1)  # extract info in brackets
                dialogue = re.sub('\[.*?\]', '', dialogue)  # remove everything within brackets
            else:
                bracket_info = None

            # If dialogue contains parentheses, remove everything within it
            if '(' in dialogue and ')' in dialogue:
                dialogue = re.sub('\(.*?\)', '', dialogue)

            return DialogueLine(name, emotion, dialogue)  # Return DialogueLine with bracket_info as an additional argument
        elif line.startswith("[RANDOM EVENT"):
            return self.parse_random_event(line)
        elif line.startswith("%"):
            self.summary = line[1:]
        else:
            return None



    def parse_random_event(self, line):
        if line.startswith("RANDOM EVENT = "):
            # remove the leading 'RANDOM EVENT = '
            line = line[len("RANDOM EVENT = "):]
        elif line.startswith("RANDOM EVENT="):
            # remove the leading 'RANDOM EVENT='
            line = line[len("RANDOM EVENT="):]
        else:
            return None

        line = line.strip()  # Remove leading/trailing whitespace

        event_end = line.find(' ')
        if event_end == -1:  # No characters were provided
            event_type = line
            characters = []
        else:
            event_type = line[:event_end]  # extract the event type
            characters = line[event_end+1:].split(' ')  # extract the characters

        return RandomEvent(event_type, characters)



    def getUnityScript(self):
        outputString = ""
        eventString = ""
        for dLine in self.lines:
            if dLine.random_event is not None:
                rEvent = dLine.random_event
                eventString = "[EVENT={} ".format(rEvent.event_type) + ",".join(rEvent.characters)  + "]";
                outputString += eventString + "\n"

            nameString = "[NAME={} #{}]".format(dLine.character, dLine.emotion)
            outputString += (nameString + "  " + dLine.dialogue + "\n")
        return outputString



