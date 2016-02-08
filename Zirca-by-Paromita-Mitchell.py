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

chatting = True #for the while loop

print("What is your name? (please say quit to end chat")
name = input("?: ") #inital name
print("Hi,", name)
topic = "NOT HERE" # default value for topic. For debugging.

pairs={
r"hello": "hello!", #r"pattern" this is using re module.
r"(.*?goodbye.*)":"bye! Wait, why are you saying TOPIC",
r"no": "oh. ok. sorry.",
r".*?I am (.*)?[,]|.*?I am (.*)?[?]|.*?I am (.*)?[.]|.*?I am (.*)": "Oh? Really? It must be fun to be TOPIC",
# this set of patterns is very special. If you say I am a frog. And I like stuff it will only pick up I am a frog. 
#Also, when you just sat "I am a frog" without a full stop it will work
r".*?\?":"I'm not supposed to answer that.",
r"quit":"It's a shame to see you go. I hope you come back soon!",
r".*?why.*": "because, oh nevermind. Let's talk about you."
}#problem with priorities or statements.

notpair = "ok." #the final answer if the response is in my library

def replyold(response): #main loop function
    reply = notpair #default
    for key in pairs: #goes through all keys in the pairs dictionary to find one that is preferred
        match = re.match(key,response,re.I) #re.I removes case sensitivity
        if match != None:
            if "TOPIC" in pairs[key]:#match.group spits out part of pattern that fits the stuff in brackets.
                for n in range(1,5):
                    if match.group(n)!=None:
                        topic = match.group(n)
                # need to find a better way than this. More fluid. THis is a basic way. A work around.
                reply = pairs[key].replace("TOPIC", str(topic))
            else:
                reply = pairs[key]
    
    print(reply)

def reply(response): #main loop function
    reply = notpair #default
    for key in pairs: #goes through all keys in the pairs dictionary to find one that is preferred
        match = re.match(key,response,re.I) #re.I removes case sensitivity
        if match != None:
            if "TOPIC" in pairs[key]:#match.group spits out part of pattern that fits the stuff in brackets.
                for n in range(1,5):
                    if match.group(n)!=None:
                        topic = match.group(n)
                # need to find a better way than this. More fluid. THis is a basic way. A work around.
                reply = pairs[key].replace("TOPIC", str(topic))
            else:
                reply = pairs[key]

    print(reply)

#loop for chat
while chatting == True:
    response = input(name+": ")
    time.sleep(1) #more natural to have wait time. Seems more human.
    reply(response)
    #no i need another method. I'll do it like mitsuku for now to keep it simple.
    #ending the chat
    if response == "quit":
        chatting = False
    

'''
Issues to deal with:

 - if two keywords in a line, it picks the last one.
 - Questions need an input
 -find all might be a better alternative
 - "but"
 - more questions, the response no.
 - much later issue is to fix a theme in what is being said.
 -triggers only one key word. Need to fix that. Need some kind of priority.
'''







'''
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
    
    
'''

