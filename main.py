import nltk
import re
import random
from reflections import reflections
from responses import responses, smart_responses
from semantic_network import *
from constants import *


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


def analyse(statement, semantic):
    tokens = nltk.word_tokenize(statement)
    tags = nltk.pos_tag(tokens)

    # Print values
    for i in tags:
        print(i)

    if len(tokens) == 6 or len(tokens) == 7:
        # Example "my phone is on the table" or "my food is on the fridge" or "the phone is on the table"
        if ('DT' or 'PRP$' in tags[0][1]) and ('NN' in tags[1][1]) and ('VB' in tags[2][1]) \
                and (tags[3][1] == 'IN') and (tags[4][1] == 'DT') and ('NN' in tags[5][1]):
            s = tags[0][0] + " " + tags[1][0]
            pred = tags[2][0] + " " + tags[3][0]
            obj = tags[4][0] + " " + tags[5][0]
            a = Association(s, pred, obj)
            da = Declaration('user', a)
            if len(semantic.query_local('user', s, pred, obj)) > 0:
                semantic.remove_instances(s, pred, obj)
            semantic.insert(da)
            output = random.choice(responses) + " " + reflect(statement)
            return output

        # What do you know about ... ?
        elif('WP' in tags[0][1] and 'VBP' in tags[1][1] and 'PRP' in tags[2][1] and 'VB' in tags[3][1] and 'IN' in tags[4][1]):
            # entity = my phone
            if(len(tokens) == 7):
                entity = str(tokens[5] + ' ' + tokens[6])
            #entity = jhon
            else:
                entity = str(tokens[5])
            print(entity)

            if (int(len(semantic.query_local('user', entity))) > 0 or int(len(semantic.query_local('user', e2=entity))) > 0):
                listofknowledge = semantic.query_local(
                    'user', entity) + semantic.query_local('user', e2=entity)
                print(len(listofknowledge))
                output = ""
                count = 1
                for i in listofknowledge:
                    res_sub = i.relation.entity1
                    res_pred = i.relation.name
                    red_obj = i.relation.entity2
                    if(count == len(listofknowledge)):
                        output += str(res_sub) + " " + \
                            str(res_pred) + " " + str(red_obj)
                        break
                    output += str(res_sub) + " " + str(res_pred) + \
                        " " + str(red_obj) + " and "
                    count += 1
                return reflect(output)
            return smart_response(statement)
        else:
            return smart_response(statement)

    elif len(tokens) == 4 or len(tokens) == 5:
        # Example "Where is my phone" / "where is the phone"- must search in triplos for answear
        if (tags[0][1] == 'WRB') and ('VB' in tags[1][1]) and ('DT' or 'PRP$' in tags[2][1]) \
                and ('NN' in tags[3][1]):
            obj = tags[2][0] + " " + tags[3][0]
            flag = False
            # Search in triples for obj
            for i in range(0, len(semantic.query_local("user", obj))):
                res_sub = semantic.query_local("user", obj)[i].relation.entity1
                res_pred = semantic.query_local("user", obj)[i].relation.name
                red_obj = semantic.query_local("user", obj)[i].relation.entity2
                # res_sub, res_pred, red_obj = triple_store.triples(obj, None, None)[i]
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
                output = "I don't know where " + \
                    reflect(tags[2][0]) + " " + \
                    reflect(tags[3][0]) + " " + tags[1][0]
                return output

        # Example "Tiago is my friend" / "Tiago is a friend"- must search in triplos for answear
        elif(tags[0][1] == 'NN') and ('VBZ' in tags[1][1]) and ('DT' or 'PRP$' in tags[2][1]) \
                and ('NN' in tags[3][1]):
            s = tags[0][0]
            pred = tags[1][0]
            obj = tags[2][0] + " " + tags[3][0]
            a = Association(s, pred, obj)
            da = Declaration("user", a)
            if (len(semantic.query_local('user', None, pred, obj)) > 0 and (obj == 'my mom'or obj == 'my mother' or obj == 'my father' or obj == 'my dad' or obj == "my girlfriend")):
                semantic.remove_instances(None, pred, obj)
            semantic.insert(da)
            output = random.choice(responses) + " " + reflect(statement)
            return output

        # who is my friend?"
        elif(tags[0][1] == 'WP') and ('VBZ' in tags[1][1]) and ('RB'or 'PRP$' in tags[2][1])\
                and ('NN' in tags[3][1]):
            #obj = "Tiago"
            obj = tags[2][0] + " " + tags[3][0]
            print("entrouuuuuuuuuuuuuuuuuuuuuuu")
            print(semantic.query_local('user', None, None, obj))
            flag = False
            # Search in triples for obj
            for i in range(0, len(semantic.query_local('user', None, None, obj))):
                print(tags[1][0] + "!!!!!!!!!!!!!!!")
                res_sub = semantic.query_local('user', None, None, obj)[
                    i].relation.entity1
                res_pred = semantic.query_local('user', None, None, obj)[
                    i].relation.name
                res_obj = semantic.query_local('user', None, None, obj)[
                    i].relation.entity2
                # res_sub, res_pred, red_obj = triple_store.triples(obj, None, None)[i]
                print(res_sub + " " + res_pred + " " + res_obj)
                if tags[1][0] in res_pred:
                        # Check if verb is the same, is != are
                    if not flag:
                        output = '{} {} {}'.format(
                            res_sub, res_pred, res_obj) + " "
                    else:

                        output += "and" + " " + \
                            '{} {} {}'.format(res_sub, res_pred, res_obj)
                    flag = True
            if flag:
                return reflect(output)
            else:
                # Come up with something smart
                output = "I don't know who is " + reflect(obj)
                return output

        # My name is walter white example with last name
        # Example "My name is Jesus" , sometimes the name as JJ (david) tag, other times as NN (jesus)
        elif (tags[0][1] == 'PRP$') and ('NN' in tags[1][1]) and ('VB' in tags[2][1]) \
                and ('JJ' or 'NN' in tags[3][1]):
            # With last name
            if len(tags) == 5:
                s = tags[0][0] + " " + tags[1][0]
                pred = tags[2][0]
                obj = tags[3][0] + " " + tags[4][0]
                output = random.choice(responses) + " your " + tags[1][0] + " is " + tags[3][0] \
                    + " " + tags[4][0]
            else:
                s = tags[0][0] + " " + tags[1][0]
                pred = tags[2][0]
                obj = tags[3][0]
                output = random.choice(
                    responses) + " your " + tags[1][0] + " is " + tags[3][0]
            if len(semantic.query_local('user', s, pred)) > 0:
                semantic.remove_instances(s, pred, obj)
            a = Association(s, pred, obj)
            dec = Declaration('user', a)
            semantic.insert(dec)
            return output

        # Example "A cat is an animal" or "A pussy is a cat"
        elif tags[0][1] == 'DT' and 'NN' in tags[1][1] and 'VB' in tags[2][1] \
                and 'DT' in tags[3][1] and 'NN' in tags[4][1]:
            sub = tags[1][0]
            pred = tags[2][0] + " " + tags[3][0]
            obj = tags[4][0]
            s = Subtype(sub, obj)
            ds = Declaration('user', s)
            semantic.insert(ds)
            if len(semantic.query_local('user', e1=obj, rel='subtype')) > 0:
                root = semantic.path_to_root(sub)[-1]
                if root[0] in VOWELS:
                    a = Association(sub, 'is an', root)
                    da = Declaration('user', a)
                    semantic.insert(da)
                    return "So, {} is an {}".format(sub, root)
                else:
                    a = Association(sub, 'is a', root)
                    da = Declaration('user', a)
                    semantic.insert(da)
                    return "So, {} is a {}".format(sub, root)
            return "So, {} {} {}".format(sub, pred, obj)

        # Example "Cat is an animal" or "Pussy is a cat"
        elif 'NN' in tags[0][1] and 'VB' in tags[1][1] and 'DT' in tags[2][1] and 'NN' in tags[3][1]:
            sub = tags[0][0]
            pred = tags[1][0] + " " + tags[2][0]
            obj = tags[3][0]
            s = Subtype(sub, obj)
            ds = Declaration('user', s)
            semantic.insert(ds)
            if len(semantic.query_local('user', e1=obj, rel='subtype')) > 0:
                root = semantic.path_to_root(sub)[-1]
                if root[0] in VOWELS:
                    a = Association(sub, 'is an', root)
                    da = Declaration('user', a)
                    semantic.insert(da)
                    return "So, {} is an {}".format(sub, root)
                else:
                    a = Association(sub, 'is a', root)
                    da = Declaration('user', a)
                    semantic.insert(da)
                    return "So, {} is a {}".format(sub, root)
            return "So, {} {} {}".format(sub, pred, obj)

        # Example "What is my name" / any question with what + 3 parcels
        elif (tags[0][1] == 'WP') and ('VB' in tags[1][1]) and (tags[2][1] == 'PRP$') and (
                tags[3][1] in ('NN' or 'JJ')):
            obj = tags[2][0] + " " + tags[3][0]
            flag = False
            # Search in triples for obj
            for i in range(0, len(semantic.query_local("user", obj))):
                res_sub = semantic.query_local("user", obj)[i].relation.entity1
                res_pred = semantic.query_local("user", obj)[i].relation.name
                red_obj = semantic.query_local("user", obj)[i].relation.entity2
                # res_sub, res_pred, red_obj = triple_store.triples(obj, None, None)[i]
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
                output = "I don't know what " + \
                    reflect(tags[2][0]) + " " + \
                    reflect(tags[3][0]) + " " + tags[1][0]
                return output
        elif (tags[0][1] == 'WP') and ('VB' in tags[1][1]) and (tags[2][1] == 'PRP$') and (
                tags[3][1] in ('NN' or 'JJ')):
            pass
        else:
            return smart_response(statement)

    elif len(tokens) == 3:
        # who is Tiago?"
        if(tags[0][1] == 'WP') and ('VBZ' in tags[1][1]) and ('RB'or 'NN' in tags[2][1]):
                #obj = "Tiago"
            obj = tags[2][0]
            print(obj)
            print(semantic.query_local('user', obj))
            flag = False
            # Search in triples for obj
            for i in range(0, len(semantic.query_local("user", obj))):
                print(tags[1][0] + "!!!!!!!!!!!!!!!")

                res_sub = semantic.query_local("user", obj)[i].relation.entity1
                res_pred = semantic.query_local("user", obj)[i].relation.name
                res_obj = semantic.query_local("user", obj)[i].relation.entity2
                # res_sub, res_pred, red_obj = triple_store.triples(obj, None, None)[i]
                if tags[1][0] in res_pred:
                    # Check if verb is the same, is != are
                    if not flag:
                        output = '{} {} {}'.format(res_sub, res_pred, res_obj)
                    else:
                        res_pred = nltk.word_tokenize(res_pred)
                        output += ", " + '{} {}'.format(res_pred[1], res_obj)
                    print(res_sub + " " + res_pred + " " + res_obj)
                    flag = True
            if flag:
                return reflect(output)
            else:
                # Come up with something smart
                output = "I don't know who is " + tags[2][0]
                return output
        else:
            return smart_response(statement)
    else:
        return smart_response(statement)


def main():
    semantic = SemanticNetwork()
    while True:
        statement = input("You > ")
        statement = statement.lower()
        if statement == "bye":
            print("Bot > bye")
            break
        print("Bot > " + analyse(statement, semantic))


if __name__ == "__main__":
    main()
