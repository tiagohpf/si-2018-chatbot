import nltk
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

responses = ["So,", "I see,"];

smart_responses = ["The sky is infinite.","There are many stars.","Deadpool was a great movie.","Aveiro has nice weather"]

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
        if ('DT' or 'PRP$' in tags[0][1] and 'NN' in tags[1][1] and 'VB' in tags[2][1] and tags[3][1] == 'IN' and tags[4][1] == 'DT' and 'NN' in tags[5][1]):
            sub = tags[0][0] + " " + tags[1][0]
            pred = tags[2][0] + " " + tags[3][0]
            obj = tags[4][0] + " " + tags[5][0]
            triplestore.remove_triples(sub, pred, None)
            triplestore.add_triple(sub, pred, obj)
            output = random.choice(responses) + " " + reflect(statement)
            return output

    elif(len(tokens) == 4):
        # Example "Where is my phone" / "where is the phone"- must search in triplos for answear
        if tags[0][1] == 'WRB' and 'VB' in tags[1][1] and ('DT' or 'PRP$' in tags[2][1]) and 'NN' in tags[3][1]:
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
        elif tags[0][1] == 'PRP$' and 'NN' in tags[1][1] and 'VB' in tags[2][1] and ('JJ' or 'NN' in tags[3][1]):

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

        #Example "What is my name"
        elif tags[0][1] == 'WP' and 'VB' in tags[1][1] and tags[2][1] == 'PRP$' and tags[3][1] == ('NN' or 'JJ'):

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
        output = random.choice(smart_responses)
        return output






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
