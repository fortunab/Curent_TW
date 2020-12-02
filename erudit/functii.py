from erudit import chatterREF

def nume(text):
    discutie = 'Nice to meet you, ' + text + '. I will present you my skills. What do you want to talk about?'
    return discutie

def convorbireIT(userText):
    if userText.lower() == "yes":
        raspuns = "So, let's begin! Please type a word, syntagm or sentence, but in english. For terminate this discussion, type exit"
    elif userText.lower() == "no":
        raspuns = "I understand, I'll wait! Type YES when you are ready. In contrast, the conversation will be over."
    else:
        raspuns = "Sorry, but I don't understand! Please type YES or NO. " \
                  "I will wait for your response, but I expect you to accept. In contrast, discussion will be over."
    return raspuns

def convorbireREF(userText):
    if userText.lower() == "yes":
        raspuns = "Let's start then. Please introduce a word which you consider is necessary for XAI. I'll try to find the sentence and its associated reference. For exit, type Q"
    elif userText.lower() == "no":
        raspuns = "I understand, I'll wait! Type YES when you are ready. In contrast, the conversation will be over."
    else:
        raspuns = "Sorry, but I don't understand! Please type YES or NO. " \
                  "I will wait for your response, but I expect you to accept. In contrast, discussion will be over."
    return raspuns

def referinte(userText):
    return chatterREF.response(userText)
