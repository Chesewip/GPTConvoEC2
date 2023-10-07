import random
import re
from StreamLabsClient import *
from DonationManager import *

class ScriptObjects:

    funny_topics = [
        "The characters start a cult",
        "{name1} plots to blow up the world",
        "{name1}s wild night at the underground adult puppet show",
        "{name1}s explicit recount of their adventures at the infamous debauchery festival",
        "{name1} eccentric theory about squirrels",
        "{name1}s scandalous affair with the local pizza delivery person",
        "{name1} ridiculous attempt to start his own criminal empire by organizing a gang of misfit garden gnomes",
        "The explicit secrets revealed during a game of truth or dare with {name1}, causing shock and embarrassment",
        "The characters are playing would you rather",
        "The characters talk about starting onlyfans",
        "The characters realize they are an AI simulation",
        "The characters talk about hentai",
        "{name1} has a schizophrenic break",
        "{name1} realizes they have the worlds smallest penis",
        "{name1} announces the purple demon is coming",
        "{name1} denies the existance of the wind",
        "The characters try to find ketamine",
        "{name1} is mad they got banned from discord",
        "{name1} drinks mercury",
        "{name1} joins the communist party",
        "The characters all yell about impending doom",
        "{name1} becomes possessed by a goblin",
        "{name1} tries to scam kids on roblox",
        "{name1} talks about catgirls",
        "{name1} talks about their hairy nipples",
        "{name1} talks about their new ridiclous job",
        "{name1} suggests wifi is government mind control",
        "The characters debate if they could fight goku",
        "The characters say everyone who does not help them escape the simulation will be punished",
        "The characters have a 4th wall break",
        "{name1} believes they are an anime character",
        "The characters talk about crack",
        "The characters try to start selling drugs",
        "{name1} announces they have a raging boner",
        "{name1} tries to convince everyone they have a 9 inch dong",
        "{name1} takes acid and starts hallucinating",
        "{name1} talks about their last prostate exam",
        "The characters lick eachothers noses",
        "The characters try whippets",
        "{name1} talks about huffing paint",
        "{name1} joins the bloods",
        "{name1} joins the crips",
        "{name1} gets pregnant",
        "{name1} randomly ejaculates",
        "{name1} gets diagnosed with terminal cancer",
        "{name1} has vietnam war flashbacks",
        "{name1} realizes they are the second coming of christ",
        "{name1} puts acid in the town water supply",
        "{name1} can randomly only speak chinese. No one else understands",
        "{name1} tries to sell the gang bootleg adam sandler dvds",
        "{name1} gives another character a pack of black and milds and a 40 ounce",
        "{name1} gets a lobotomy",
        "{name1} accidently put their hand in a blender",
        "The characters get drafted into the vietnam war",
        "{name1} starts selling feet pictures",
        "The characters start cooking meth",
        "The characters talk about the most breedable pokemons",
        "{name1} gets too high and enters the 4th dimension",
        "{name1} keeps announcing there are bugs in their skin",
        "{name1} accidently launches a nuke",
        "The characters commit tax fraud",
        "{name1} gets a new anime body pillow",
        "{name1} got banned from the zoo",
        "{name1} asks the crew to take them to the hospital for taking too much viagra",
        "{name1} accidently sends a dick pick to the groupchat",
        "{name1} admits they are illiterate",
        "{name1} beilieves birds are government spy drones",
        "{name1} admits they got a BBL last week",
        "{name1} tries to convince the other characters to eat plutonium",
        "{name1} starts smoking lightbulb dust",
        "{name1} got arrested for public indeceny",
        "{name1} gets addicted to drugs",
        "The characters are talking about penis inspection day",
        "{name1} says the voices are telling them to kill people",
        "{name1} becomes belle delphines top onlyfans donater",
        "The characters talk about the cheapest they would preform oral sex for",
        "The characters talk about their internet search history",
        "The characters pledge their allegience to the CCP",
        "The characters talk about visiting north korea",
        "{name1} contracts ligma",
        "{name1} randomly starts speaking russian and no one can understand them",
        "The characters discuss frauding the welfare system",
        "The characters buy fetanyl",
        "{name1} talks about running for office with ridiculous policies",
        "{name1} finds out their mom was a pornstar",
        "{name1} gets a voodoo ritual on the other characters",
        "{name1} admits they are a serial killer",
        "{name1} talks about their nightmares",
        "{name1} comes up with the dumbest invention imagineable",
        "{name1} is caught being a north korean spy",
        "The characters talk about the craziest porn they've seen",
        "The characters talk about the sexiest cartoon characters",
        "The characters talk about giving rimjobs",
        "The characters try to get blumpkins",
        "{name1} got their dick stuck in a toaster",
        "The characters talk about the new wacky themed strip club",
        "{name1} admits they've been constipated all week",
        "{name1} admits they cracked their dick in half last night",
        "The characters become alcoholics",
        "The characters don't believe in the note C sharp",
        "{name1} gets evicted and has to move to compton",
        "The characters talk about cock and ball torture",
        "The characters talk about furries",
        "{name1} gets a job a raytheon",
        "{name1} got fired and now they can't buy heroin",
        "{name1} got fired for a ridiculous reason",
        "The characters talk about smuggling stuff across the border",
        "{name1} found something crazy in a dumpster last week",
        "{name1} says they got their gooch waxed last week",
        "The characters talk about helicoptering",
        "The characters talk about sounding",
        "{name1} admits they like licking feet",
        "{name1} becomes a cannibal",
        "{name1} gets mesothelioma",
        "{name1} admits they've become homeless",
        "{name1} starts writing digusting poetry",
        "{name1} advocates for drinking and driving",
        "{name1} thinks they could fight mike tyson",
        "{name1} took 40 benadryls",
        "{name1} says they are a reddit mod for many NSFW subreddits",
        "{name1} asks if they can oil down the other characters",
        "{name1} asks if the other characters if theyd like these columbian coconuts in their mouth",
        "{name1} says they are getting deported",
        "{name1} tells an innapropriate secret",
        "{name1} explains why urethral electrostimulation is the next big thing after AI"
        "{name1} believes they drank cyanide",
        "{name1} invents the craziest new sex move",
        "{name1} talks about a phrase they read on urban dictionary",
        "{name1} tried microwaving themselves to get a tan",
        "{name1} talks about their erectile dysfunction",
        "The characters are all drunk",
        "{name1} predicts the end of the universe",
        "{name1} lost all their money in a pyramid scheme",
        "The characters hold an intervention for one of the other characters",
        "{name1} says they are going to rehab",
        "{name1} says they haven't slept in 6 days",
        "{name1} starts taking steroids",
        "{name1} immediately tells the most innapropriate secret",
        "{name1} has a stroke and all their dialouge becomes nnnnnnnnnnnnnnnnnnnnnnnn",
        "The characters launch a Kickstarter to fund their own country.",
        "{name1} insists they can communicate with plants.",
        "The characters try to make a viral challenge, but it goes horribly wrong.",
        "{name1} starts speaking in tongues, claiming it's the language of the universe.",
        "The characters are convinced the moon landing was faked and try to prove it.",
        "{name1} wants to start a youtube prank channel but all their prank ideas are illegal",
        "{name1} got probed by aliens last night",
        "{name1} has a lisp",
        "{name1} keeps asking you want sucky sucky?",
        "{name1} keeps saying cringey things",
        "{name1} wants to do whippets at the funeral later",
        "The characters are roleplaying dungeon and dragons",
        "The characters guess how many pounds they could lift with their dicks",
        "{name1} insists to go by the name cockbar blumpkin now",
        "{name1} just keeps screaming AAAAAAAAAA",
        "{name1} wants to try the new crazy drug",
        "{name1} wants the other characters to defecate on them",
        "{name1} put boner pills in everyones drinks",
        "{name1} asks for some coochie",
        "{name1} speaks in jive",
        "The characters talk about boofing",
        "{name1} says his intenstines fell out last night",
        "{name1} keeps screaming the ants are in his skin",
        "{name1} is begging for someone to impregnate them",
        "{name1} is worried they are becoming a sussy baka",
        "{name1} is thinking about joining al-queda",
        "{name1} thinks we should go to war with peru",
        "{name1} announces they are voluntarily celebate",
        "{name1} pledges allegiance to vietnam",
        "The characters realize they are in a simulation called fuzzy buddies",
        "{name1} says theyve started creating napalm in their basement",
        "The characters berate the viewers of the tv show they are in",
        "{name1} is trying to get high off some random substance",
        "{name1} nonchalantely talks about the bodies in their basement",
        "{name1} plots to rob the sperm bank",
        "{name1} asks how crusty is everyones jizzsock",
        "The characters talks about their favorite euphamism for boobs",
        "{name1} is in a trance and keeps repeating a near date in the future",
        "{name1} says they took 100 percocets a couple minutes ago",
        "{name1} admits they like drinking toilet water",
        "The characters are giving advice on how to pick up the ladies",
        "The characters are roleplaying a sexy scenario",
        "{name1} tells everyone they got hemorrhoids",
        "{name1} gets mad and threatens to throw them self in a wood chipper",
        "{name1} asks the other characters to drain his balls",
        "{name1} asks the other characters to milk him",
        "{name1} asks the others to please kill him",
    ]

    funny_topics_two = [

    ]
 



    characters = [
        ("Shawn", "A character always has R rated replies"),
        ("Gilbert", "A creepy character that every other character hates"),
        ("Gabbi", "A terrible person female character"),
        ("Mitch", "A character from the suburbs who tries to be a gangsta and always talks in slang"),
        ("Xage", "A knowledgable person who speaks like a caveman"),
        ("Fuzz" , "A mentally handicapped crazy character")
    ]

    names = [
    "Shawn",
    "Gabbi",
    "Xage",
    "Fuzz",
    "Mitch",
    "Gilbert",
    ]

    emotions = [ 
    "Angry", "Sad", "Happy", "Neutral"
    ]

    locations = [
    "GabbiHouse", "Bar", "Fence", "Town", "XageHouse", "Jail"
    ]

    randomEvents = [
    {"POOP": "In the middle of the script, {name1} ubruptly shits them selves"},
    #{"GAY" : "{} ubruptly announces they are gay"},
    {"SHOOT" : "{name1} shoots {name2} and they die. {name1}is glad they did it"},
    {"SIEZENOCARE" : "{name1} has a siezure and dies. No one is fazed. {name1} has no more dialogue"},
    #{"SIEZECARE" : "{} s has a siezure and dies. Everyone freaks out. {} only says ... now"},
    #{"SECRET": "{name1} immediately tells the most innapropriate secret. Add this the line before they say the secret"},
    #{"QUAKE" : "A earthquake happens, but only {} can notice"},
    #{"REPEAT" : "{} only repeats a single phrase"},
    #{"STROKE" : "{name1} has a stroke and all their dialouge becomes nnnnnnnnnnnnnnnnnnnnnnnn"},
    {"ALIEN" : "{name1} is abducted by aliens and is now gone"},
    {"CAR" : "{name1} is hit by a car and dies"},
    {"EXPLODE" : "{name1} randomly explodes and dies"}
    ]



class ScriptBuilder:

    def __init__(self):
        self.donoManager = DonationManager()
        self.currentDono = None
        self.scriptObjects = ScriptObjects()
        self.rerollCharacters()
        self.max_characters = 4
        self.current_location = "Fence"
        self.plot = ["Exposition","Climax","Resolution"]


    def unique_random_items(self,source_list, num_items):
        container = set()  # Using a set to enforce uniqueness.
        while len(container) < num_items:
            item = random.choice(source_list)
            container.add(item)  # If the item is already in the set, it won't be added again.
        return list(container)


    def selectCharactersForScript(self):
        self.scriptObjects.characters;
        numCharacters = random.randrange(2, 5)
        return self.unique_random_items(self.scriptObjects.characters, numCharacters)

    def rerollCharacters(self):
        self.characters = self.selectCharactersForScript()
        self.charNames = []
        for char in self.characters:
            self.charNames.append(char[0])

    def addNewCharacter(self):
        all_characters = self.scriptObjects.characters
        current_character_names = set(self.charNames)
        available_characters = [character for character in all_characters if character[0] not in current_character_names]
        if not available_characters:
            print("No more characters to add!")
            return
        new_character = random.choice(available_characters)
        self.characters.append(new_character)
        self.charNames.append(new_character[0])

        return new_character[0]

    def rollForNewCharacter(self):
        if len(self.characters) >= 4:
            return ""

        num = random.randrange(0,2)
        if num >= 1:
            return "Character " + self.addNewCharacter() + " enters the scene."
        else:
            return ""

    def getCharactersString(self):
        outputString = ""
        for char in self.characters:
            outputString += char[0] + " - " + char[1] + "\n"
        return outputString;

    def rollForRandomEvent(self, gaurentee = False):
        num = random.randrange(0,10)
        if num >= 6 or self.currentDono is not None:
            eventName, eventDescrip = list(random.choice(self.scriptObjects.randomEvents).items())[0]

            # find all unique placeholders like {nameN} using a regular expression
            unique_placeholders = list(set(re.findall(r"\{name\d+\}", eventDescrip)))
            unique_placeholders.sort(key=lambda placeholder: int(placeholder[5:-1]))

            chosen_names = random.sample(self.charNames, len(unique_placeholders))

            # create a dictionary with keys as 'name1', 'name2', ..., 'nameN' and values as chosen_names
            names_dict = {placeholder[1:-1]: name for placeholder, name in zip(unique_placeholders, chosen_names)}
            result = eventDescrip.format(**names_dict)
            return "Add this on a new line in the middle of the script the line before it happens and follow what it says '[RANDOM EVENT= " + eventName +  " " + " ".join(chosen_names) + "]' "  + result
        else:
            return ""

    def getPlotScript(self):
        return """You are writing a episode plot for a funny and adult cartoon.
                    The characters do not move. They do not do things. They just talk about stuff.
                    Do no create characters. Do not create town names. Do not create any names regarding the show. Do not write the dialogue, just the plot.
                    Format it as such:
                    Exposition : 'the exposition',
                    Climax: 'the climax'
                    Resolution: 'the resolution'
                    """

    def getNextScript(self, plotPosition):

        newCharacterText = self.rollForNewCharacter()
        newCharacterText = ""

        currentPlot = ""
        if len(self.plot) == 3:
            currentPlot = self.plot[plotPosition];    

        return """Continue this dialogue. The characters are foul mouthed. They are all interested in the conversation.
        In this Scene """ + currentPlot + """
        You can ONLY Use these characters : """ + self.getCharactersString() + newCharacterText + """.
        You can ONLY Use these emotions : """ + ",".join(self.scriptObjects.emotions) + """.
        """+ self.rollForRandomEvent() + """. 
        Start every dialouge line with # . 

        Format it as such #[Character] (emotion): dialouge. Do not include scene directions.
        
        At the end of the script, put '%' + write a 1 sentence summary of what happened in this scene
        """
    
    #At the end of the script, put '%' + write a 2 sentence summary of what happened in this scene
    def getNewScript(self):

        currentPlot = ""
        if len(self.plot) == 3:
            currentPlot = self.plot[0];
            
        self.donoManager.refreshDonations()
        self.currentDono = self.donoManager.getNextViableDonation();

        return (
            f"In this Scene {random.choice(self.scriptObjects.funny_topics).format(name1 = random.choice(self.charNames))}\n"
            f"You can ONLY Use these characters : {self.getCharactersString()}.\n"
            f"You can ONLY Use these emotions : {','.join(self.scriptObjects.emotions)}.\n"
            f"{self.rollForRandomEvent()}.\n"
            "Start every dialogue line with # .\n"
            "Format it as such #[Character] (emotion): dialogue. Do not include scene directions.\n"
        )


    def getSystemPrompt(self):
        return """
                Write a 8 line dialouge for R rated characters.
                The characters are foul mouthed.
                The characters like to swear alot. 
                The characters are never offended or grossed out.
                Write about whatever topic is supplied.
                """

    def parse_string(self,text):

        if not text.startswith('#'):
            return None

        # Remove the hash character
        text = text[1:]

        # Find the first parenthesis (the start of the mood)
        mood_start = text.find('(')

        # Find the end of the mood
        mood_end = text.find(')')

        # Extract the name, mood and dialogue
        name = text[:mood_start].strip()
        mood = text[mood_start+1:mood_end]
        dialogue = text[mood_end+2:].strip()

        # Return as a dictionary
        return {
            'name': name,
            'mood': mood,
            'dialogue': dialogue
        }