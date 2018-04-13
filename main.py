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


def analyse(statement, triplestore):
    tokens = nltk.word_tokenize(statement)
    tags = nltk.pos_tag(tokens)
    sub = pred = obj = None
    # Example "my phone is on the table" or "my food is on the fridge" or "the phone is on the table"
    if ('PRP$' == tags[0][1] and 'NN' in tags[1][1] and 'VB' in tags[2][1]
            and tags[3][1] == 'IN' and tags[4][1] == 'DT' and 'NN' in tags[5][1]):
        sub = tags[0][0] + " " + tags[1][0];
        pred = tags[2][0] + " " + tags[3][0];
        obj = tags[4][0] + " " + tags[5][0];
        triplestore.remove_triples(sub, pred, None)
        triplestore.add_triple(sub, pred, obj)
        print("Giving info")

    # Example "My name is Jesus" , sometimes the name as JJ (david) tag, other times as NN (jesus)
    elif tags[0][1] == 'PRP$' and 'NN' in tags[1][1] and 'VB' in tags[2][1] \
            and ('JJ' or 'NN' in tags[3][1]):
        print("Name of user is " + tags[3][0])

    # Example "Where is my phone" / "where is the phone"- must search in triplos for answear
    elif tags[0][1] == 'WRB' and 'VB' in tags[1][1] and 'PRP$' == tags[2][1] and 'NN' in tags[3][1]:
        obj = tags[2][0] + " " + tags[3][0]

        # Search in triples for obj

        res_sub, res_pred, red_obj = triplestore.triples(obj, None, None)[0]
        print("Asking about where " + tags[3][0])
        print('{} {} {}'.format(res_sub, res_pred, red_obj))

    else:
        print("No idea about what was inserted")

    # Do semantic stuff

    # Print values
    #for i in tags:
        #print(i)


def main():
    triplestore = TripleStore()
    while True:
        statement = input("You > ")
        analyse(statement, triplestore)
        if statement == "quit":
            break

        # print ("Bot > " + statement)


if __name__ == "__main__":
    main()
