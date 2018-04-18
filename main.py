import nltk
import re
import random
from triplestore import TripleStore
from reflections import reflections
from responses import responses, smart_responses


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


def smart_response(statement):
    for pattern, s_responses in smart_responses:
        match = re.match(pattern.lower(), statement.rstrip(".!").lower())
        if match:
            response = random.choice(s_responses)
            return response.format(*[reflect(g) for g in match.groups()])


def verify_in(x):
    for i in x:
        if 'IN' in i:
            return True
    return False


def reflect(fragment):
    tokens = fragment.lower().split()
    for i, token in enumerate(tokens):
        if token in reflections:
            tokens[i] = reflections[token]
    return ' '.join(tokens)


def analyse(statement, triple_store):
    tokens = nltk.word_tokenize(statement)
    tags = nltk.pos_tag(tokens)

    # Print values
    for i in tags:
        print(i)

    if len(tokens) == 6:
        # Example "my phone is on the table" or "my food is on the fridge" or "the phone is on the table"
        if ('DT' or 'PRP$' in tags[0][1]) and ('NN' in tags[1][1]) and ('VB' in tags[2][1]) \
                and (tags[3][1] == 'IN') and (tags[4][1] == 'DT') and ('NN' in tags[5][1]):
            sub = tags[0][0] + " " + tags[1][0]
            pred = tags[2][0] + " " + tags[3][0]
            obj = tags[4][0] + " " + tags[5][0]
            triple_store.remove_triples(sub, pred, None)
            triple_store.add_triple(sub, pred, obj)
            output = random.choice(responses) + " " + reflect(statement)
            return output
        else:
            return smart_response(statement)
    elif len(tokens) == 4 or len(tokens) == 5:
        # Example "Where is my phone" / "where is the phone"- must search in triplos for answear
        if (tags[0][1] == 'WRB') and ('VB' in tags[1][1]) and ('DT' or 'PRP$' in tags[2][1]) \
                and ('NN' in tags[3][1]):
            obj = tags[2][0] + " " + tags[3][0]
            flag = False
            # Search in triples for obj
            for i in range(0, len(triple_store.triples(obj, None, None))):
                res_sub, res_pred, red_obj = triple_store.triples(obj, None, None)[i]
                if not verify_in(nltk.pos_tag(nltk.word_tokenize(res_pred))):
                    continue
                if tags[1][0] in res_pred:
                    # Check if verb is the same, is != are
                    if not flag:
                        output = '{} {} {}'.format(res_sub, res_pred, red_obj)
                    else:
                        res_pred = nltk.word_tokenize(res_pred)
                        output += ", " + '{} {}'.format(res_pred[1], red_obj)
                    flag = True
            if flag:
                return reflect(output)
            else:
                # Come up with something smart
                output = "I don't know where " + reflect(tags[2][0]) + " " + reflect(tags[3][0]) + " " + tags[1][0]
                return (output)
        # My name is walter white example with last name
        # Example "My name is Jesus" , sometimes the name as JJ (david) tag, other times as NN (jesus)
        elif (tags[0][1] == 'PRP$') and ('NN' in tags[1][1]) and ('VB' in tags[2][1]) \
                and ('JJ' or 'NN' in tags[3][1]):
            # With last name
            if len(tags) == 5:
                sub = tags[0][0] + " " + tags[1][0]
                pred = tags[2][0]
                obj = tags[3][0] + " " + tags[4][0]
                output = random.choice(responses) + " your " + tags[1][0] + " is " + tags[3][0] \
                         + " " + tags[4][0]
            else:
                sub = tags[0][0] + " " + tags[1][0]
                pred = tags[2][0]
                obj = tags[3][0]
                output = random.choice(responses) + " your " + tags[1][0] + " is " + tags[3][0]
            triple_store.remove_triples(sub, pred, None)
            triple_store.add_triple(sub, pred, obj)
            return output
        # Example "What is my name" / any question with what + 3 parcels
        elif (tags[0][1] == 'WP') and ('VB' in tags[1][1]) and (tags[2][1] == 'PRP$') and (
                tags[3][1] in ('NN' or 'JJ')):
            obj = tags[2][0] + " " + tags[3][0]
            flag = False
            # Search in triples for obj
            for i in range(0, len(triple_store.triples(obj, None, None))):
                res_sub, res_pred, red_obj = triple_store.triples(obj, None, None)[i]
                if tags[1][0] in res_pred:
                    # Check if verb is the same, is != are
                    flag = True
                    break
            print("Asking about what " + tags[3][0])
            if flag:
                output = '{} {} {}'.format(res_sub, res_pred, red_obj)
                return reflect(output)
            else:
                # Come up with something smart
                output = "I don't know what " + reflect(tags[2][0]) + " " + reflect(tags[3][0]) + " " + tags[1][0]
                return output
        else:
            return smart_response(statement)
    else:
        return smart_response(statement)


def main():
    triple_store = TripleStore()
    while True:
        statement = input("You > ")
        #statement = statement.lower()
        if statement == "bye":
            print("Bot > bye")
            break
        print("Bot > " + analyse(statement, triple_store))


if __name__ == "__main__":
    main()
