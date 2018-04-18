import nltk
import re
from triplestore import TripleStore
import random

# more tags search here
# PRP personal pronoun I, he, she
# PRP$ possessive pronoun my, his, hers
# JJ adjective 'big'
# JJR adjective, comparative 'bigger'
# JJS adjective, superlative 'biggest'
# NN noun, singular 'desk'
# NNS noun plural 'desks'
# NNP proper noun, singular 'Harrison'
# NNPS proper noun, plural 'Americans'
# IN preposition/subordinating conjunction
# VB verb, base form take
# VBD verb, past tense took
# VBG verb, gerund/present participle taking
# VBN verb, past participle taken
# VBP verb, sing. present, non-3d take
# VBZ verb, 3rd person sing. present takes
# WDT wh-determiner which
# WP wh-pronoun who, what
# WP$ possessive wh-pronoun whose
# WRB wh-abverb where, when

# For statement, my phone is on the table create semantic relations (my,phone), (belongs,me) (is,in) (table)

reflections = {
    "am": "are",
    "was": "were",
    "i": "you",
    "i'd": "you would",
    "i've": "you have",
    "i'll": "you will",
    "my": "your",
    "are": "am",
    "you've": "I have",
    "you'll": "I will",
    "your": "my",
    "yours": "mine",
    "you": "me",
    "me": "you"
}

responses = ["So,", "I see,","I am glad to know that,"];

smart_responses =[

    [r'I need (.*)',
     ["Why do you need {0}?",
      "Would it really help you to get {0}?",
      "Are you sure you need {0}?"]],

    [r'Why don\'?t you ([^\?]*)\??',
     ["Do you really think I don't {0}?",
      "Perhaps eventually I will {0}.",
      "Do you really want me to {0}?"]],

    [r'Why can\'?t I ([^\?]*)\??',
     ["Do you think you should be able to {0}?",
      "If you could {0}, what would you do?",
      "I don't know -- why can't you {0}?",
      "Have you really tried?"]],

    [r'I can\'?t (.*)',
     ["How do you know you can't {0}?",
      "Perhaps you could {0} if you tried.",
      "What would it take for you to {0}?"]],

    [r'I am (.*)',
     ["Did you come to me because you are {0}?",
      "How long have you been {0}?",
      "How do you feel about being {0}?"]],

    [r'I\'?m (.*)',
     ["How does being {0} make you feel?",
      "Do you enjoy being {0}?",
      "Why do you tell me you're {0}?",
      "Why do you think you're {0}?"]],

    [r'Are you ([^\?]*)\??',
     ["Why does it matter whether I am {0}?",
      "Would you prefer it if I were not {0}?",
      "Perhaps you believe I am {0}.",
      "I may be {0} -- what do you think?"]],

    [r'What (.*)',
     ["Why do you ask?",
      "How would an answer to that help you?",
      "What do you think?"]],

    [r'How (.*)',
     ["How do you suppose?",
      "Perhaps you can answer your own question.",
      "What is it you're really asking?"]],

    [r'Because (.*)',
     ["Is that the real reason?",
      "What other reasons come to mind?",
      "Does that reason apply to anything else?",
      "If {0}, what else must be true?"]],

    [r'(.*) sorry (.*)',
     ["There are many times when no apology is needed.",
      "What feelings do you have when you apologize?"]],

    [r'Hello(.*)',
     ["Hello... I'm glad you could drop by today.",
      "Hi there... how are you today?",
      "Hello, how are you feeling today?"]],

    [r'I think (.*)',
     ["Do you doubt {0}?",
      "Do you really think so?",
      "But you're not sure {0}?"]],

    [r'(.*) friend (.*)',
     ["Tell me more about your friends.",
      "When you think of a friend, what comes to mind?",
      "Why don't you tell me about a childhood friend?"]],

    [r'Yes',
     ["You seem quite sure.",
      "OK, but can you elaborate a bit?"]],

    [r'(.*) computer(.*)',
     ["Are you really talking about me?",
      "Does it seem strange to talk to a computer?",
      "How do computers make you feel?",
      "Do you feel threatened by computers?"]],

    [r'Is it (.*)',
     ["Do you think it is {0}?",
      "Perhaps it's {0} -- what do you think?",
      "If it were {0}, what would you do?",
      "It could well be that {0}."]],

    [r'It is (.*)',
     ["You seem very certain.",
      "If I told you that it probably isn't {0}, what would you feel?"]],

    [r'Can you ([^\?]*)\??',
     ["What makes you think I can't {0}?",
      "If I could {0}, then what?",
      "Why do you ask if I can {0}?"]],

    [r'Can I ([^\?]*)\??',
     ["Perhaps you don't want to {0}.",
      "Do you want to be able to {0}?",
      "If you could {0}, would you?"]],

    [r'You are (.*)',
     ["Why do you think I am {0}?",
      "Does it please you to think that I'm {0}?",
      "Perhaps you would like me to be {0}.",
      "Perhaps you're really talking about yourself?"]],

    [r'You\'?re (.*)',
     ["Why do you say I am {0}?",
      "Why do you think I am {0}?",
      "Are we talking about you, or me?"]],

    [r'I don\'?t (.*)',
     ["Don't you really {0}?",
      "Why don't you {0}?",
      "Do you want to {0}?"]],

    [r'I feel (.*)',
     ["Good, tell me more about these feelings.",
      "Do you often feel {0}?",
      "When do you usually feel {0}?",
      "When you feel {0}, what do you do?"]],

    [r'I have (.*)',
     ["Why do you tell me that you've {0}?",
      "Have you really {0}?",
      "Now that you have {0}, what will you do next?"]],

    [r'I would (.*)',
     ["Could you explain why you would {0}?",
      "Why would you {0}?",
      "Who else knows that you would {0}?"]],

    [r'Is there (.*)',
     ["Do you think there is {0}?",
      "It's likely that there is {0}.",
      "Would you like there to be {0}?"]],

    [r'My (.*)',
     ["I see, your {0}.",
      "Why do you say that your {0}?",
      "When your {0}, how do you feel?"]],

    [r'You (.*)',
     ["We should be discussing you, not me.",
      "Why do you say that about me?",
      "Why do you care whether I {0}?"]],

    [r'Why (.*)',
     ["Why don't you tell me the reason why {0}?",
      "Why do you think {0}?"]],

    [r'I want (.*)',
     ["What would it mean to you if you got {0}?",
      "Why do you want {0}?",
      "What would you do if you got {0}?",
      "If you got {0}, then what would you do?"]],

    [r'(.*) mother(.*)',
     ["Tell me more about your mother.",
      "What was your relationship with your mother like?",
      "How do you feel about your mother?",
      "How does this relate to your feelings today?",
      "Good family relations are important."]],

    [r'(.*) father(.*)',
     ["Tell me more about your father.",
      "How did your father make you feel?",
      "How do you feel about your father?",
      "Does your relationship with your father relate to your feelings today?",
      "Do you have trouble showing affection with your family?"]],

    [r'(.*) child(.*)',
     ["Did you have close friends as a child?",
      "What is your favorite childhood memory?",
      "Do you remember any dreams or nightmares from childhood?",
      "Did the other children sometimes tease you?",
      "How do you think your childhood experiences relate to your feelings today?"]],

    [r'(.*)\?',
     ["Why do you ask that?",
      "Please consider whether you can answer your own question.",
      "Perhaps the answer lies within yourself?",
      "Why don't you tell me?"]],

    [r'quit',
     ["Thank you for talking with me.",
      "Good-bye.",
      "Thank you, that will be $150.  Have a good day!"]],

    [r'(.*)',
     ["Please tell me more.",
      "Let's change focus a bit... Tell me about your family.",
      "Can you elaborate on that?",
      "Why do you say that {0}?",
      "I see.",
      "Very interesting.",
      "{0}.",
      "I see.  And what does that tell you?",
      "How does that make you feel?",
      "How do you feel when you say that?"]]

]

def smart_response (statement):
    for pattern, smart_responsess in smart_responses:
        match = re.match(pattern, statement.rstrip(".!"))
        if match:
            response = random.choice(smart_responsess)
            return response.format(*[reflect(g) for g in match.groups()])

def verifyIN(x):
    for i in x:
        if 'IN' in  i:
            return True
    return False

def reflect(fragment):
    tokens = fragment.lower().split()
    for i, token in enumerate(tokens):
        if token in reflections:
            tokens[i] = reflections[token]
    return ' '.join(tokens)

def analyse(statement, triplestore):
    tokens = nltk.word_tokenize(statement)
    tags = nltk.pos_tag(tokens)

    output = ""
    sub = pred = obj = None


    #Print values
    for i in tags:
        print(i)

    if(len(tokens) == 6):
        # Example "my phone is on the table" or "my food is on the fridge" or "the phone is on the table"
        if ('DT' or 'PRP$' in tags[0][1]) and ('NN' in tags[1][1]) and ('VB' in tags[2][1]) and (tags[3][1] == 'IN') and (tags[4][1] == 'DT') and ('NN' in tags[5][1]):
            sub = tags[0][0] + " " + tags[1][0]
            pred = tags[2][0] + " " + tags[3][0]
            obj = tags[4][0] + " " + tags[5][0]
            triplestore.remove_triples(sub, pred, None)
            triplestore.add_triple(sub, pred, obj)
            output = random.choice(responses) + " " + reflect(statement)
            return output
        else:
            return smart_response(statement)


    elif(len(tokens) == 4):
        # Example "Where is my phone" / "where is the phone"- must search in triplos for answear
        if (tags[0][1] == 'WRB') and ('VB' in tags[1][1]) and ('DT' or 'PRP$' in tags[2][1]) and ('NN' in tags[3][1]):
            obj = tags[2][0] + " " + tags[3][0]
            flag = False

            # Search in triples for obj
            for i in range(0, len(triplestore.triples(obj, None, None))):
                res_sub, res_pred, red_obj = triplestore.triples(obj, None, None)[i]

                if verifyIN(nltk.pos_tag(nltk.word_tokenize(res_pred))) == False:
                    continue

                if (tags[1][0] in res_pred):

                    # Check if verb is the same, is != are
                    if(flag == False):
                        output = '{} {} {}'.format(res_sub, res_pred, red_obj)
                    else:
                        res_pred = nltk.word_tokenize(res_pred)
                        output+= ", " + '{} {}'.format(res_pred[1], red_obj)

                    flag = True


            if (flag == True):
                return reflect(output)
            else:
                # Come up with something smart
                output = "I don't know where " +reflect(tags[2][0]) + " " + reflect(tags[3][0]) + " " + tags[1][0]
                return (output)



        #My name is walter white example with last name
        # Example "My name is Jesus" , sometimes the name as JJ (david) tag, other times as NN (jesus)
        elif (tags[0][1] == 'PRP$') and ('NN' in tags[1][1]) and ('VB' in tags[2][1]) and ('JJ' or 'NN' in tags[3][1]):

            #With last name
            if(len(tags) == 5):
                sub = tags[0][0] + " " + tags[1][0]
                pred = tags[2][0]
                obj = tags[3][0] + " "+ tags[4][0]
                output = random.choice(responses)+" your " + tags[1][0]+ " is " + tags[3][0] +" " + tags[4][0]+ " ,very interesting!"

            else:
                sub = tags[0][0] + " " + tags[1][0]
                pred = tags[2][0]
                obj = tags[3][0]
                output = random.choice(responses) + " your "+ tags[1][0]+ " is " + tags[3][0] + " ,very interesting!"

            triplestore.remove_triples(sub, pred, None)
            triplestore.add_triple(sub, pred, obj)
            return output

        #Example "What is my name" / any question with what + 3 parcels
        elif (tags[0][1] == 'WP') and ('VB' in tags[1][1]) and (tags[2][1] == 'PRP$') and (tags[3][1] in ('NN' or 'JJ')):

            obj = tags[2][0] + " "+tags[3][0]

            flag = False

            # Search in triples for obj
            for i in range(0, len(triplestore.triples(obj, None, None))):
                res_sub, res_pred, red_obj = triplestore.triples(obj, None, None)[i]
                if (tags[1][0] in res_pred):
                    # Check if verb is the same, is != are

                    flag = True
                    break
            print("Asking about what " + tags[3][0])

            if (flag == True):
                output = '{} {} {}'.format(res_sub, res_pred, red_obj)
                return reflect(output)
            else:
                # Come up with something smart
                output = "I don't know what " + reflect(tags[2][0]) + " " + reflect(tags[3][0]) + " " + tags[1][0]
                return (output)
        else:
            return smart_response(statement)
    else:
        return smart_response(statement)






def main():
    triplestore = TripleStore()
    while True:
        statement = input("You > ")
        if statement == "bye":
            print("Bot > bye")
            break

        print ("Bot > " + analyse(statement, triplestore))


if __name__ == "__main__":
    main()
