# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 15:04:14 2015

@author: perha_2

Zirca

chat should be infinite until they want to leave
be kind and humble in this one, got to be humble with chatbots, else people freak out
should know more about one topic than others - colours and light

Hello! Currently my code is quite basic. I have not built up a large database,
and instead I am concentrating on creating a good base. 
With a good base I can add more to the dictionary later.
Memory will be easy to implement later.


"""
import re
import time
import random


chatting = True  # for the while loop
topic = "NOT HERE"  # default value for topic. For debugging.
notpair = "ok."  # the final answer if the response is in my library
name = input("?: ")  # initial name

# ---------------- DATABASES ----------------------------------------------------------------------------------#

# knowledge Bank
ZircaTopicBank = [
    ["chocolate",
        "fantastic",
        "delicious and tasty treat",
        "chocolate is unhealthy",
        "but I don't think that it matters",
        "Chocolate is something that you should enjoy, after all"]
]

# pairs of responses and replys
pairs = [  # highest priority at the BOTTOM: it'll print the last one.

    (r"quit",  # r"pattern" this is using re module.
        ["It's a shame to see you go. I hope you come back soon!",
         "bye!", "have a good day!"]),

    (r"(.*?goodbye.*)",
        ["bye! Wait, why are you saying <TOPIC>",
         "Bye? Do you wish to leave? If so, please say <quit>"]),

    (r".*?[?]",
        ["I'm not supposed to answer that.",
         "Bah! I can't answer that!",
         "I'm not actually sure... how to answer that... "]),

    (r".*?no.*|.*?nah.*|.*?not really.*",
        ["oh. ok. sorry.",
         "Ah.", "no.",
         "Well, that's a shame.",
         "oh, well in that case..."]),

    # this set of patterns is very special. If you say I am a frog. And I like stuff it will only pick up I am a frog.
    # Also, when you just sat "I am a frog" without a full stop it will work
    (r".*?I.{0,2}?m (.*)?[,]|.*?I.{0,2}?m (.*)?[?]|.*?I.{0,2}?m (.*)?[.]|.*?I.{0,2}?m (.*)",
        ["Oh? Really? It must be fun to be <TOPIC>",
         "Cool!",
         "Wow! You are <TOPIC>? That's crazy!"]),


    (r".*?hello.*|.*?hi$|.*?hi\W{1}.*|.*?yo .*|.*?good morning.*|.*?g'day.*|.*?good afternoon.*",
        ["hello!",
         "hi",
         "Wassup?",
         "Hello my deary! >_<",
         "Yo!"]),

    (r".*?why.*",
        ["Why? Ooh, that's a hard one to answer... ",
         "because, oh nevermind. Let's talk about you."]),

    (r".*?how are you.*",
        ["Good! Thank's for asking!",
         "Sweet, I had a good day today.",
         "Awesome!",
         "Well, I guess I'm alright. It really depends on you. How are you?"]),

    (r".*?what.*?your name[?]|.*?do you have a name[?]",
        ["Zirca!",
         "I'm Zirca",
         "My name is Zirca."]),

    (r"Nice to meet you.*?",
        ["Nice to meet you too.",
         "The same!"]),

    (r".*?\W?today.*",
        ["Talking about today, I was super busy.",
         "I actually did a lot today! I talked to a bunch of people, got a bit of maths and calculations done..."]),

    (r".*?\W?sorry.*",
        ["Oh don't worry, there's no reason to be sorry.", "That's quite alright."]),

    (r"What's your opinion on (.*)?[?]",
        ["Well, I'll have to think about that.<PAUSE><ZTHINK>."])
]

# ---------------- FUNCTIONS ----------------------------------------------------------------------------------#

def editOutput(response, output, match):

    #random output
    reply = random.choice(output)

    if "<TOPIC>" in reply:  # match.group spits out part of pattern that fits the stuff in brackets.
        for n in range(1, 5):
            if match.group(n) != None:
                topic = match.group(n)
        # need to find a better way than this. More fluid. THis is a basic way. A work around.
        reply = reply.replace("<TOPIC>", str(topic))

    #if "[PAUSE]" in reply:
        # somehow split the string at that point and print the two halves of the string separately.

    if "<ZTHINK>" in reply:
        if match.group(1) != None:
            ztopic = match.group(1)
            for knownTopic in ZircaTopicBank:
                if ztopic.lower() == knownTopic[0]:
                    posNeg = knownTopic[1]
                    description = knownTopic[2]
                    otherViews = knownTopic[3]
                    agreeDisagree = knownTopic[4]
                    conclusion = knownTopic[5]
                    zthink = "I believe that " + ztopic + " is a " + posNeg + " thing. It really is a " + description + ". I know that other people say that " + otherViews + ", " + agreeDisagree + ". " + conclusion
                else:
                    zthink = "Oh, I actually do not know much about that topic."
        else:
            zthink = "Oh, I don't think you actually gave me a topic there."
        reply = reply.replace("<ZTHINK>", str(zthink))


    return reply

def reply(response):  # main loop function
    reply = notpair  # default
    for pair in pairs:  # goes through all keys in the pairs dictionary to find one that is preferred
        match = re.match(pair[0], response, re.I)  # re.I removes case sensitivity
        if match != None:
            print(pair)
            reply = editOutput(response, pair[1], match)
    pause(reply)

def pause(reply):
    pausePhrases = re.split(r"<PAUSE>", reply)

    for pausePhrase in pausePhrases:
        print(pausePhrase)
        time.sleep(1)


# ---------------- SOURCE-SOURCE CODE ---------------------------------------------------------------------------------#

print("What is your name? (please say quit to end chat)")
print("Hi,", name)
# loop for chat
while chatting == True:
    response = input(name+": ")
    time.sleep(1)
    # more natural to have wait time. Seems more human.
    reply(response)

    # ending the chat
    if response == "quit":
        chatting = False
    








"""
Issues to deal with:

 - Questions need an input
 - "but"
 - more questions, the response no.
 - much later issue is to fix a theme in what is being said.
"""


"""
#library of terms
closureTerms = []
greetingTerms = []
noTerms = []
yesTerms = []
historyr=open('history.txt', "r")
historya=open('history.txt', "a")

#inital information about person
print("Hiya! Hang on, do I know you? ")
introduction = input("?:")
if noTerms in introduction:
    print("Ah! Then you are new? Fantastic! Well, I guess I better introduce myself then! I'm Zirca and-- well I guess I should let you speak. What's your name?")
    nameinput = input("?:")
    if noTerms in nameinput:
        print("Well, I kind of do need your name, but if you don't want me to know your name that's also fine - you can call yourself anonymous.")
        print("So I'll ask again - What is your name?")
        nameinput = input("?:")
        if nameinput == "anonymous":
            name = "?"
        else:
            name = nameinput
            historya.write(name)
            historya.close()
    
    
"""

