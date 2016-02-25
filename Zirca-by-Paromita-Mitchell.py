# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 15:04:14 2015

@author: perha_2

Zirca

chat should be infinite until they want to leave
be kind and humble in this one, got to be humble with chatbots, else people freak out

Hello! Currently my code is quite basic. I have not built up a large database,
and instead I am concentrating on creating a good base. 
With a good base I can add more to the dictionary later.
"""
import re
import time
import random

nonresponsefile = open("nonresponsefile.txt", "a") #file which remembers phrases that Zirca didn't understand.
good = open("good.txt", "a")
bad = open("bad.txt", "a")

chatting = True  # for the while loop
topic = "NOT HERE"  # default value for topic. For debugging.
notpair = "ok."  # the final answer if the response is in my library


chathistory = ""
# ---------------- DATABASES ----------------------------------------------------------------------------------#

# profile
userProfile = {
    #name
    #age
    #likes
    #dislikes
    #owns
    #is a
    #topics
        #perspective on topic
    #does
    #feels
}

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



    (r".*?[?]",
        [  # "I'm not supposed to answer that.",
         # "Bah! I can't answer that!",
         "I'm not actually sure... how to answer that... "]),

    (r".*?\W{1}no\W{1}.*|.*?nah.*|.*?not really.*",
        ["oh. ok. sorry.",
         "Ah.", "no.",
         "Well, that's a shame.",
         "oh, well in that case..."]),

    # this set of patterns is very special. If you say I am a frog. And I like stuff it will only pick up I am a frog.
    # Also, when you just sat "I am a frog" without a full stop it will work
    (r".*?I.{0,2}?m (.*)?[,]|.*?I.{0,2}?m (.*)?[?]|.*?I.{0,2}?m (.*)?[.]|.*?I.{0,2}?m (.*)",
        ["Oh? Really? It must be fun to be <TOPIC>%ISA%",
         "Cool!%ISA%",
         "Wow! You are <TOPIC>? That's crazy!%ISA%"]),
    (r"(.*?goodbye.*)",
        ["bye! Wait, why are you saying <TOPIC>",
        "Bye? Do you wish to leave? If so, please say <quit>"]),

    (r".*?hello.*|.*?hi$|.*?hi\W{1}.*|.*?yo .*|.*?good morning.*|.*?g'day.*|.*?good afternoon.*",
        ["hello!",
         "hi",
         "Wassup.",
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

    (r".*?what.*?your name[?]?.*|.*?do you have a name[?]",
        ["Zirca!",
         "I'm Zirca",
         "My name is Zirca."]),

    (r"Nice to meet you.*?",
        ["Nice to meet you too.",
         "The same!"]),

    (r".*?\W{1}today.*",
        ["Talking about today, I was super busy.",
         "I actually did a lot today! I talked to a bunch of people, got a bit of maths and calculations done..."]),

    (r".*?\W{1}sorry.*",
        ["Oh don't worry, there's no reason to be sorry.",
         "That's quite alright."]),

    (r"What's your opinion on (.*)?[?]",
        ["Well, I'll have to think about that.<PAUSE><ZTHINK>."]),

    (r".*?haribos?.*?",
        ["~HARIBO~"])
]

# subpairs -> subpair/subtopic -> keyword, initial statement, questionsdict -> question block -> question, response check,
# (cont.)reply
# its really complicated... :'(
subpairs = [
    ["HARIBO", "Oh? You mentioned Haribos!",
        {"They are delicious aren't they?":
            [[r"yes.*", r"no.*"],
            ["Yes! That's fantastic!", "Aw, that's a shame.", "Well, then."]],
        "When did you last eat them?":
            [[r".*?\W{1}year.*?|.*?\W{1}ages.*?|(?m)^(?=.*long)((?!not).)*$", r".*?not long.*|.*?recent.*|.*?day.*|.*?week.*"],
            ["Ah, so quite a while ago, then. That's unfortunate. You should treat yourself!","Not too long ago, then! That's good!", "Ah, hmm."]]
         }
     ]



]

questionlist = ( # NOTE IS A TUPLE!!!!!!!
    ("How are you?",
     (r".*?I.{0,2}?m (.*)?[,]|.*?I.{0,2}?m (.*)?[?]|.*?I.{0,2}?m (.*)?[.]|.*?I.{0,2}?m (.*)", r".*?(fine).*", r".*?(not too \w*)?\W.*", r"^(\w*)?[.,!].*", r"^(very \w*)?\W.*", r"^\w*?$")),

)

# ---------------- FUNCTIONS ----------------------------------------------------------------------------------#


def reply():  # main loop function
    global chathistory
    reply = notpair  # default
    if questionset != ():
        questionreply = checkAnswer()
    for pair in pairs:  # goes through all keys in the pairs dictionary to find one that is preferred
        match = re.match(pair[0], response, re.I)  # re.I removes case sensitivity
        if match != None:
            rawoutput = pair[1][0]
            subblock = re.match(r"~(.*)?~", rawoutput)
            if subblock:
                keyword = subblock.group(1)
                block(keyword)
                return
            else:
                appendUsers = re.match(r".*?%(.*)?%.*", rawoutput)
                if appendUsers:
                    appendProfile(appendUsers.group(1), findgroup(match))
                reply = editoutput(pair[1], match)
    # if questionset != ():
        # print(questionreply)
        # chathistory += str(questionreply) +"\n"
    pause(reply)
    lognonresponses(reply)

def checkAnswer():
    question = questionset[0]  # TIS A TUPLE VALUE so is not linked and that is fine.
    answerchecks = questionset[1]  # "

    answermatch = None

    for answercheck in answerchecks:
        answermatch = re.match(answercheck, response)
        if answermatch:
            answer = findgroup(answermatch)
            break

    global questionlist
    questionlist = list(questionlist)
    questionlist.remove(questionset)
    questionlist = tuple(questionlist)

    if answermatch:
        appendProfile(question, answer)
        return answer
    else:
        return ""

def checkRepeatStatement():



def block(keyword):
    global chathistory

    for subpair in subpairs:
        if subpair[0] == keyword:
            subtopic = subpair
    print(subtopic[1])

    chathistory = chathistory + str(subtopic[1]) + "\n"

    qdict = subtopic[2]
    for question in qdict:
        print(question)
        chathistory = chathistory + str(question) + "\n"
        subresponse = input(userName + ": ")
        chathistory = chathistory + str(userName + ": " + subresponse) + "\n"
        subreply = qdict[question][1][-1]
        for patternnumber in range(len(qdict[question][0])):
            replymatch = re.match(qdict[question][0][patternnumber], subresponse)
            if replymatch:
                subreply = qdict[question][1][patternnumber]
        print(subreply)
        chathistory = chathistory + str(subreply) + "\n"
        if subresponse == "I'm bored.":
            return



def editoutput(output, match):
    # random output
    reply = random.choice(output)

    appendUsers = re.match(r".*?(%.*?%)", reply)
    if appendUsers:
        type = appendUsers.group(1)
        reply = reply.replace(str(type), "")

    if "<TOPIC>" in reply:  # match.group spits out part of pattern that fits the stuff in brackets.
        for n in range(1, 5):
            if match.group(n) != None:
                topic = match.group(n)
        # need to find a better way than this. More fluid. THis is a basic way. A work around.
        reply = reply.replace("<TOPIC>", str(topic))

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
                    zthink = "Oh, I actually do not know much about that topic"
        else:
            zthink = "Oh, I don't think you actually gave me a topic there"
        reply = reply.replace("<ZTHINK>", str(zthink))


    return reply

def findgroup(match):
    groupno = 1
    noError = True
    while noError:
        try:
            value = match.group(groupno)
            if value != None:
                noError = False
            groupno += 1
        except IndexError:
            noError = False
    return value

def appendProfile(key, match):
    userProfile[key] = match

def pause(reply):
    global chathistory

    pausePhrases = re.split(r"<PAUSE>", reply)

    for pausePhrase in pausePhrases:
        #time.sleep(1)
        print(pausePhrase)
        chathistory = chathistory + str(pausePhrase) + "\n"


def lognonresponses(reply):
    if reply == notpair:
        nonresponsefile.write(str(response) + "\n")
    if reply == "I'm not actually sure... how to answer that... ":
        nonresponsefile.write(str(response) + "\n")

def askaquestion():
    # questionlist is a TUPLE MATRIX for immutability
    global questionset
    global chathistory
    try:
        questionset = random.choice(questionlist) # choice is fine with tuples. question set is s separate variable now
        print(questionset[0]) # prints out question
        chathistory += str(questionset[0]) + "\n"
    except IndexError:
        questionset = ()


# ---------------- SOURCE-SOURCE CODE ---------------------------------------------------------------------------------#

chathistory = chathistory + str("What is your name? (please say quit to end chat)") + "\n"
userName = input("?: ")  # initial name
chathistory = chathistory + str("?: "+userName) + "\n"
userProfile["name"] = userName
print("Hi, " + userName)
askaquestion()
chathistory = chathistory + str("Hi, " + userName) + "\n"

# loop for chat
while chatting == True:
    response = input(userName+": ")
    chathistory = chathistory + str(userName+": "+response) + "\n"
    reply()print("What is your name? (please say quit to end chat) (Plz be gentle)")

    askaquestion()

    # ending the chat
    if response == "quit":
        print("WAIT! Please rate this chat! pick a integer between 1(the worst) and 10(the best)!")
        chathistory = chathistory + str("WAIT! Please rate this chat! pick a integer between 1(the worst) and 10(the best)!") + "\n"

        ratingAccepted = False
        while not ratingAccepted:
            try:
                rating = int(input("rating: "))
                chathistory = chathistory + str("rating :"+str(rating)) + "\n"
                ratingAccepted = True
            except ValueError:
                print("Please type in a integer - using your number keys. '10' instead of 'ten'.")
                chathistory = chathistory + str("Please type in a integer - using your number keys. '10' instead of 'ten'.") + "\n"
        print("thank you!")
        chathistory = chathistory + str("thank you!") + "\n\n\n"
        if rating > 5:
            good.write(chathistory)
            good.close()
        else:
            bad.write(chathistory)
            bad.close()
        print(userProfile)
        chatting = False

nonresponsefile.close()


# Issues to deal with:
#  TODO Questions should only be asked once
#  TODO - "but"
#  TODO - more questions, the response no.
#  TODO - much later issue is to fix a theme in what is being said.



# vvvvvvvvvvvvvvvvvvvvvvvvvvvvv me realising what a pain in the butt this is going to be vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

# #library of terms
# closureTerms = []
# greetingTerms = []
# noTerms = []
# yesTerms = []
# historyr=open('history.txt', "r")
# historya=open('history.txt', "a")
#
# #inital information about person
# print("Hiya! Hang on, do I know you? ")
# introduction = input("?:")
# if noTerms in introduction:
#     print("Ah! Then you are new? Fantastic! Well, I guess I better introduce myself then! I'm Zirca and-- well I guess I should let you speak. What's your name?")
#     nameinput = input("?:")
#     if noTerms in nameinput:
#         print("Well, I kind of do need your name, but if you don't want me to know your name that's also fine - you can call yourself anonymous.")
#         print("So I'll ask again - What is your name?")
#         nameinput = input("?:")
#         if nameinput == "anonymous":
#             name = "?"
#         else:
#             name = nameinput
#             historya.write(name)
#             historya.close()
#


