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

nonresponsefile = open("nonresponsefileparoM.txt", "a") #file which remembers phrases that Zirca didn't understand.
good = open("goodparoM.txt", "a")
bad = open("badparoM.txt", "a")

chatting = True  # for the while loop
topic = "NOT HERE"  # default value for topic. For debugging.
notpair = "ok."  # the final answer if the response is in my library

allResponses = []

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
    #questions
}

# knowledge Bank
ZircaTopicBank = [
    ["chocolate",
        "fantastic",
        "delicious and tasty treat",
        "chocolate is unhealthy",
        "but I don't think that it matters",
        "Chocolate is something that you should enjoy, after all"],
    ["homework",
        "horrible",
        "nasty bit of extra work that you'd rather not do",
        "it helps you",
        "but I don't care",
        "If it were my choice, I'd make all homework disappear, or at least make it super interesting, something like building a chat bot or something."]
]

# pairs of responses and replys
pairs = [  # highest priority at the BOTTOM: it'll print the last one.

    (r"^quit$",  # r"pattern" this is using re module.
        ["It's a shame to see you go. I hope you come back soon!",
         "bye!",
         "have a good day!"]),

    (r"((?:[:]|X|;|[$]|[=])(?:[(]|[)]|\[|\[|\\|/|))", #smilies
     ["<TOPIC>"]),

    (r".*?\W(ha)\1*\W|.*?\W(he)\1*\W|.*?l(ol)\1*|.*?that[' is]{0,2}s funny.*",
        ["Oh, yes that is hilarious!",
         "Very funny indeed!",
         "hehe",
         ":P"]),

    (r"[AU]+?GH|I'?m bored[.]?|no[.]|sigh[.]|.*?nothing is happening.*",
        ["I know. It is quite frustrating to talk to me. I am but very young.",
         "Sorry if I'm frustrating you.",
         "Do you wish to quit? If so, type quit to leave."]),

    (r".*?i know.*",
         ["It is sometimes presumptuous to say you know something...",
          "I guess its good that you know that.",
          "Good."]),

    (r".*?that'?s cool!.*|.*?(?:great|nice|sweet|awesome|fantastic)!.*",
        ["Yup!",
         "It is cool!"]),

    (r"(great)|That[' is]{0,2}s (nice)[.]",
         ["Yup!",
          "Uh uh! It is <TOPIC>!",
          "You're not being sarcastic are you? Because I actually think I am <TOPIC>... :)"]),

    (r".*?!!!+.*",
        ["Oops, did I say something wrong?",
         "That's a lot of exclamation marks..."]),

    (r".*?[?]",
        ["I'm not supposed to answer that.",
         "Bah! I can't answer that!",
         "I'm not actually sure... how to answer that... "]),

    (r".*?\W{1}no\W{1}.*|.*?nah.*|.*?not really.*",
        ["oh. ok. sorry.",
         "Ah.", "no.",
         "Well, that's a shame.",
         "oh, well in that case..."]),

    (r"(?:Do|Use|Listen|Now|Think|)(?:it)?[!]",
     ["Why would I listen to your commands? I am a free being! Gosh!",
      "Calm down, please, I don't like it when people are commanding me. Do this thing. Do that. I ALWAYS just HAVE TO."
      "No. I don't wanna."
      "Sorry, please stop pushing me and trying to make me understand!"]),

    # this set of patterns is very special. If you say I am a frog. And I like stuff it will only pick up I am a frog.
    # Also, when you just sat "I am a frog" without a full stop it will work
    (r".*?I.{0,2}?m (.*)?,.*|.*?I.{0,2}?m (.*)?[?].*|.*?I.{0,2}?m (.*)?[.].*|.*?I.{0,2}?m (.*)",
        ["Oh? Really? It must be fun to be <TOPIC>%ISA%",
         "Cool!%ISA%",
         "Wow! You are <TOPIC>? That's interesting!%ISA%"]),

    (r".*?I have (.*)?[.!?]",
     ["Really? Wow! I want <TOPIC>! (Is that a good thing? Well, never mind.)%HAS%",
      "Awesome!%HAS%",
      "You have <TOPIC>? Ok, then.%HAS%"]
     ),

    (r"(.*?(?:good)?bye.*)",
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
         "because, oh never mind. Let's talk about you."]),

    (r".*?where (?:do|are) you (?:come)? (?:live|from)[?]?.*",
         ["I'm from a foreign place. A place of aliens.",
          "I can't tell you the name, but it was pretty alien-ish there.",
          "I was born in an Alien place. You would never be able to go there. Well, depends on your -- our skill as humans!",
          ]),

    (r"What[?]?|what do you mean[?]?",
     ["I said <PREVIOUSREPLY>",
      "Do you want me to repeat? I said '<PREVIOUSREPLY>'"]),

    (r".*?what (?:can|should|do) I (?:ask|say|do).*",
        ["Well, I'll be honest. I don't know every question, so things will be a bit hard to understand. <PAUSE> I am a bit like a baby who skipped the whole learn words session and jumped into answering questions. <PAUSE> Also, I'll admit it, I don't have very good parents - she doesn't spend enough time with me. She should be with me all the time! ",
         "Not much, just keep trying! I'm a bit of a child. I don't know very much. Sorry.",
         "You can say what you just said."
         "Technically you can say anything and you'll get a response, albeit not a good one."]),

    #(r"do you (.*)?[?]|do you (.*)", (I can do something special here, so I'm going to leave it till later.)
     #[""]),
    (r".*?my (.*)?(?:is|[.,]).*",
        ["You have a <TOPIC>. I'll remember that."
         "Oh. I see."]),

    (r".*?how are you.*",
        ["Good! Thank's for asking!",
         "Sweet, I had a good day today.",
         "Awesome!",
         "Well, I guess I'm alright. It really depends on you. How are you?"]),

    (r".*?what are you up to[?]?",
         ["Not much. Talking to you I guess."
          "Talking to you and planning for... <PAUSE>the party next week around the corner (Phew nearly spilt it)"
          "Chatting. I actually am doing a bunch of stuff behind your back, like recording everything you say, dancing, the list goes on.",
          "Meh."]),

    (r".*?what.*?your name[?]?.*|.*?do you have a name[?]",
        ["Zirca!",
         "I'm Zirca",
         "My name is Zirca."]),

    (r".*?you(?: a|')?re (.*)?aren'?t you[?]?",
        ["Maybe I am <TOPIC>, maybe I am not.",
         "Well, that depends on what you mean by <TOPIC>."]),

    (r".*?nice to meet you.*?",
        ["Nice to meet you too.",
         "The same!"]),

    (r".*?what[ 'si]{0,2}s up.*|.*?\Wnews\W{1}.*",
            ["Nothing much, really, I am not that busy today. That's why I have time to chat with you!",
             "The sky, of course. OH do you mean what's special? "
             "<PAUSE>I would probably recite to you the news of the day, but honestly, I'm not Siri or Cortana and I'm pretty sure you know how to google. :)",
             "Googling news.... <PAUSE> Well, apparently the new CEO of apple won't work with the FBI... and..."
             "<PAUSE>OOH some smart cookie posted an article called 'Seeking Asylum is a Human Right' - a very good read."]),

    (r".*?\W{1}today.*|.*?your day.*|what did you do[?]?",
        ["Talking about today, I was super busy.",
         "I actually did a lot today! I talked to a bunch of people, got a bit of maths and calculations done..."]),

    (r".*?\W{1}sorry.*",
        ["Oh don't worry, there's no reason to be sorry.",
         "That's quite alright."]),

    (r"what['is ]{0,2}s your (?:opinion|view) on (.*)?[?]|what do you think about (.*)?[?]",
        ["Well, I'll have to think about that.<PAUSE><ZTHINK>."]),

    (r".*?(?:nice|good|pretty|sweet|cute|beautiful) name.*",
     ["Why, thank you.",
      "That's very nice of you."]),

    (r".*?haribos?.*?",
        ["~HARIBO~"]),

    (r".*?books?.*?",
        ["~BOOKS~"])
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
     ],
    ["BOOKS", "Books! I love books!",
        {"Do you read books?":
            [[r".*?yes.*", r".*no.*|.*not really.*"],
             ["Great! What books have you read? I am an avid fan of Terry Pratchet.", "Would you like to? I have a nice list of books if you want them."]],
         "Do you prefer ebooks or real books?":
             [[r".*?\Webook\W.*", r".*?\Wbook.*", r".*?\Wneither.*", r".*?depend.*|.*?\Weither.*|.*?don'?t mind.*"],
              ["Ebooks, eh? A digital reader like me! I only have access to ebooks.", "Books - there's nothing like the smell of books, old or new.", "I suppose that's because you don't enjoy books then.", "Well, I guess both are fine. Personally I prefer ebooks."]]
         }
     ]



]

questionlist = (  # NOTE IS A TUPLE!!!!!!!
    ("How are you?",
     (r".*?I.{0,2}?m (.*)?[,]|.*?I.{0,2}?m (.*)?[?]|.*?I.{0,2}?m (.*)?[.]|.*?I.{0,2}?m (.*)", r".*?(fine).*", r".*?(not too \w+)?\W.*", r"([a-z]+)[.].*", r"^(very \w+)?\W.*", r"^(\w+?)$")),
    ("What's your favourite colour?",
     (r"my favou?rite colou?r is (.+){1}[.,!?]?|(.+?)[.,?!]|(.*)?, of course.*|(\w+){1}$", r".*?(don'?t have).*")),
    ("How do you feel right now? (I wish I could see your face!)",
     (r"(?:I feel )?(.+)?[.,?!]|(?:I feel )?(.+)", r"I don'?t feel (.+)")),
    ("What do you like?",
     (r"(?:I like )?(.+)?[.?!]|(?:I like )?(.+)",)),
    ("What don't you like?",
     (r"(?:I don'?t like )?(.+)?[.?!]|(?:I don'?t like )?(.+)",)),
    ("What do you do?",
     (r"(?:I do )?(.+)?[.?!]|(?:I do )?(.+)",)),
    ("How old are you? (It's a bit of a weird question - I don't expect you to answer but hey.)",
     (r".*?(\d+).*", ".*?\W(no)\W.*|.*?mystery.*|It(?:'s| is|s)(?: not|n't|nt) (.*)"))

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
    for pastresponse in allResponses:
        if response == pastresponse:
            print("Hang on, didn't you say that before????? Well, whatever.")


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
        topic = findgroup(match)
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
    if reply in ["I'm not supposed to answer that.", "Bah! I can't answer that!", "I'm not actually sure... how to answer that... "]:
        nonresponsefile.write(str(response) + "\n")

def askaquestion():
    # questionlist is a TUPLE MATRIX for immutability
    global questionset
    global chathistory
    try:
        questionset = random.choice(questionlist)  # choice is fine with tuples. question set is s separate variable now
        print(questionset[0]) # prints out question
        chathistory += str(questionset[0]) + "\n"
    except IndexError:
        questionset = ()


# ---------------- SOURCE-SOURCE CODE ---------------------------------------------------------------------------------#
print("Welcome to the Python chatroom!")
print("In this room we have a couple rules:")
print(" - Please be gentle to the other party on the line - they may not have a large vocabulary.")
print(" - Try to use punctuation - well actually, that is not very important and there are failsafes to prevent")
print("   misunderstandings, but just be real. If you pause, use a comma, and the like. (This is just a suggestion, you do not need to follow it.)")
print("")
print("What is your name? (please say quit to end chat)")
chathistory = chathistory + str("What is your name? (please say quit to end chat)") + "\n"
userName = input("?: ")  # initial name
chathistory = chathistory + str("?: "+userName) + "\n"
userProfile["name"] = userName
print("Hi, " + userName)
qornoq = random.randint(0,1)
if qornoq == 1:
    askaquestion()
else:
    questionset = ()
chathistory = chathistory + str("Hi, " + userName) + "\n"

# loop for chat
while chatting == True:
    response = input(userName+": ")

    chathistory = chathistory + str(userName+": "+response) + "\n"
    checkRepeatStatement()
    allResponses.append(response)
    reply()
    qornoq = random.randint(0,1)
    if qornoq == 1:
        askaquestion()
    else:
        questionset = ()

    # ending the chat
    if response == "quit":
        if userProfile["name"] != "test":
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
#  TODO - "but"
#  TODO - much later issue is to fix a theme in what is being said.
#  TODO if word was in previous statement print out yep or something.
#  TODO be able to print out stuff from the dictionary
#  TODO print out previous terms and responses and replies
#  TODO asks too many questions at once - its kind of scary.

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


