import nltk

# PRP personal pronoun I, he, she
# PRP$ possessive pronoun my, his, hers
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

def analyse(statement):
    tokens = nltk.word_tokenize(statement)
    sintatic = nltk.pos_tag(tokens)

    #Do semantic stuff
    for i in sintatic:
        print(i)




def main():
    while True:
        statement = input("You > ")
        analyse(statement.lower())
        if statement == "quit":
            break

        #print ("Bot > " + statement)


if __name__ == "__main__":
    main()