import nltk

#more tags search here
# PRP personal pronoun I, he, she
# PRP$ possessive pronoun my, his, hers
#JJ adjective 'big'
#JJR adjective, comparative 'bigger'
#JJS adjective, superlative 'biggest'
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

    #Example "my phone is on the table"
    if (sintatic[0][1] == 'PRP$' and 'NN' in sintatic[1][1] and 'VB' in sintatic[2][1] and sintatic[3][1] == 'IN' and 'NN' in sintatic[4][1] ):
        print(statement)
        print("Without DT")


        return

    #Example "my food is in the fridge"
    elif(sintatic[0][1] == 'PRP$' and 'NN' in sintatic[1][1] and 'VB' in sintatic[2][1] and sintatic[3][1] == 'IN' and sintatic[4][1] == 'DT' and 'NN' in sintatic[5][1]):
        print(statement)
        print("With DT")

        return
    #Example "My name is Jesus" , sometimes the name as JJ (david) tag, other times as NN (jesus)
    elif (sintatic[0][1] == 'PRP$' and 'NN' in sintatic[1][1] and 'VB' in sintatic[2][1] and ('JJ' or 'NN' in sintatic[3][1])):
        print(statement)
        print("Name of interactor is " + sintatic[3][0])

        return

    #Example "Where is my phone" - must search in triplos for answear
    elif(sintatic[0][1] == 'WRB' and 'VB' in sintatic[1][1] and sintatic[2][1] == 'PRP$' and 'NN' in sintatic[3][1]):
        print(statement)
        print("Asking about whereabout of " + sintatic[3][0])

        return

    else:
        print("No ideia about what was inserted")




    #Do semantic stuff


    #Print values
    for i in sintatic:
        print(i)




def main():
    while True:
        statement = input("You > ")
        analyse(statement)
        if statement == "quit":
            break

        #print ("Bot > " + statement)


if __name__ == "__main__":
    main()