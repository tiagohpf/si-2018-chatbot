import nltk
from triplestore import TripleStore


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
    #for i in tags:
    #    print(i)


    # Example "my phone is on the table" or "my food is on the fridge" or "the phone is on the table"
    if ('PRP$' == tags[0][1] and 'NN' in tags[1][1] and 'VB' in tags[2][1]
            and tags[3][1] == 'IN' and tags[4][1] == 'DT' and 'NN' in tags[5][1]):
        sub = tags[0][0] + " " + tags[1][0]
        pred = tags[2][0] + " " + tags[3][0]
        obj = tags[4][0] + " " + tags[5][0]
        triplestore.remove_triples(sub, pred, None)
        triplestore.add_triple(sub, pred, obj)
        output = "I will remember that"
        return output

    # Example "Where is my phone" / "where is the phone"- must search in triplos for answear
    elif tags[0][1] == 'WRB' and 'VB' in tags[1][1] and 'PRP$' == tags[2][1] and 'NN' in tags[3][1]:
        obj = tags[2][0] + " " + tags[3][0]
        flag = False

        # Search in triples for obj
        for i in range(0, len(triplestore.triples(obj, None, None))):
            res_sub, res_pred, red_obj = triplestore.triples(obj, None, None)[i]
            if (tags[1][0] in res_pred):
                # Check if verb is the same, is != are

                flag = True
                break
        print("Asking about " + tags[3][0])

        if (flag == True):
            output = '{} {} {}'.format(res_sub, res_pred, red_obj)
            return reflect(output)
        else:
            # Come up with something smart
            output = "Maybe you inserted a bad verb tense, I don't remember seeing anything like that ..."
            return (output)



    #My name is walter white example with last name
    # Example "My name is Jesus" , sometimes the name as JJ (david) tag, other times as NN (jesus)
    elif tags[0][1] == 'PRP$' and 'NN' in tags[1][1] and 'VB' in tags[2][1] and ('JJ' or 'NN' in tags[3][1]):

        #With last name
        if(len(tags) == 5):
            sub = tags[0][0] + " " + tags[1][0]
            pred = tags[2][0]
            obj = tags[3][0] + " "+ tags[4][0]
            output = "So, your name is " + tags[3][0] +" " + tags[4][0]+ " ,very interesting!"

        else:
            sub = tags[0][0] + " " + tags[1][0]
            pred = tags[2][0]
            obj = tags[3][0]
            output = "So, your name is " + tags[3][0] + " ,very interesting!"

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
            output = "Maybe you inserted a bad verb tense, I don't remember seeing anything like that ..."
            return (output)

    else:
        output = "Either I don't have info on that, or I don't understand the sentence given"
        return output






def main():
    triplestore = TripleStore()
    while True:
        statement = input("You > ")
        if statement == "quit":
            break

        print ("Bot > " + analyse(statement, triplestore))


if __name__ == "__main__":
    main()
