import nltk
import re
import random
from reflections import reflections
from responses import responses, smart_responses
from semantic_network import *
from constants import *
from conditions import Condition


# For statement, my phone is on the table create semantic relations (my,phone), (belongs,me) (is,in) (table)


def smart_response(statement):
    for pattern, s_responses in smart_responses:
        match = re.match(pattern.lower(), statement.rstrip(".!").lower())
        if match:
            response = random.choice(s_responses)
            return response.format(*[reflect(g) for g in match.groups()])


def reflect(fragment):
    tokens = fragment.lower().split()
    for i, token in enumerate(tokens):
        if token in reflections:
            tokens[i] = reflections[token]
    return ' '.join(tokens)


def analyse(statement, semantic, condition):
    tokens = nltk.word_tokenize(statement)
    tags = nltk.pos_tag(tokens)

    # Print values
    for sentence in tags:
        print(sentence)

    words = [word for word, statement in tags]
    statements = [statement for word, statement in tags]
    condition.set_statements(statements)

    if len(tokens) == 6 or len(tokens) == 7:
        # Examples:
        # - My phone is on the table
        # - My food is on the fridge
        # - The phone is on the table
        if condition.dt_nn_vb_in_dt_nn():
            print("My phone is on the table")
            sub = words[0] + " " + words[1]
            pred = words[2] + " " + words[3]
            obj = words[4] + " " + words[5]
            a = Association(sub, pred, obj)
            da = Declaration('user', a)
            if len(semantic.query_local('user', sub, pred)) > 0:
                semantic.remove_instances(sub, pred)
            semantic.insert(da)
            output = random.choice(responses) + " " + reflect(statement)
            return output

        # Examples:
        # - What do you know about John?
        # - What do you know about my phone?
        elif condition.wp_vbp_prp_vb_in():
            print("What do you know about John?")
            if len(tokens) == 7:
                sub = words[5] + " " + words[6]
            else:
                sub = words[5]
            results = semantic.query_local('user', e1=sub) + semantic.query_local('user', e2=sub)
            if len(results) > 0:
                output = ""
                count = 1
                for sentence in results:
                    sub = sentence.relation.entity1
                    pred = sentence.relation.name
                    obj = sentence.relation.entity2
                    if count == len(results):
                        output += sub + " " + pred + " " + obj
                        break
                    output += sub + " " + pred + " " + obj + " and "
                    count += 1
                return reflect(output)
            return smart_response(statement)
        else:
            return smart_response(statement)

    elif len(tokens) == 4 or len(tokens) == 5:
        # Examples:
        # - Where is my phone?
        # - Where is the phone?
        if condition.wrb_vb_dt_nn():
            print("Where is my phone?")
            obj = words[2] + " " + words[3]
            last_sentence = False
            results = semantic.query_local('user', obj)
            for sentence in results:
                res_sub = sentence.relation.entity1
                res_pred = sentence.relation.name
                red_obj = sentence.relation.entity2
                if not condition.has_preposition(nltk.pos_tag(nltk.word_tokenize(res_pred))):
                    continue
                if words[1] in res_pred:
                    if not last_sentence:
                        output = '{} {} {}'.format(res_sub, res_pred, red_obj)
                    else:
                        res_pred = nltk.word_tokenize(res_pred)
                        output += ", " + '{} {}'.format(res_pred[1], red_obj)
                    last_sentence = True
            if last_sentence:
                return reflect(output)
            else:
                output = "I don't know where " + reflect(words[2]) + " " + reflect(words[3]) + " " + words[1]
                return output

        # Examples:
        # - John is my friend
        # - John is a friend
        elif condition.nn_vbz_dt_nn(words[1] + " " + words[2]):
            print("John is my friend")
            sub = words[0]
            pred = words[1]
            obj = words[2] + " " + words[3]
            if len(semantic.query_local('user', e1=sub, rel=pred)) > 0:
                semantic.remove_instances(sub=sub, pred=pred)
            a = Association(sub, pred, obj)
            da = Declaration("user", a)
            print(da)
            semantic.insert(da)
            output = random.choice(responses) + " " + reflect(statement)
            return output

        # Examples:
        # - My name is John Smith
        # - My name is Zé
        # Sometimes it detects JJ and NN in anothers
        elif condition.prp_nn_vb_nn():
            print("My name is John Smith")
            sub = words[0] + " " + words[1]
            pred = words[2]
            # With last name
            if len(tags) == 5:
                obj = words[3] + " " + words[4]
            else:
                obj = words[3]
            output = random.choice(responses) + " your " + words[1] + " is " + obj
            if len(semantic.query_local('user', e1=sub, rel=pred)) > 0:
                semantic.remove_instances(sub, pred, obj)
            a = Association(sub, pred, obj)
            dec = Declaration('user', a)
            semantic.insert(dec)
            return output

        # Examples:
        # - I have a cat
        elif condition.nns_vbp_dt_nn():
            print("I have a cat")
            sub = words[0]
            pred = words[1]+ " " + words[2]
            # With last name
            if len(tags) == 5:
                obj = words[3] + " " + words[4]
            else:
                obj = words[3]
            output = random.choice(responses) + " your " + words[1] + " is " + obj
            if len(semantic.query_local('user', e1=sub, rel=pred)) > 0:
                semantic.remove_instances(sub, pred, obj)
            a = Association(sub, pred, obj)
            dec = Declaration('user', a)
            semantic.insert(dec)
            return output

        # Examples:
        # - A cat is an animal
        # - A pussycat is a cat
        elif condition.dt_nn_vbz_dt_nn() or condition.nn_vbz_dt_nn_subtype():
            print("A cat is an animal")
            if condition.dt_nn_vbz_dt_nn():
                sub = words[1]
                pred = words[2] + " " + words[3]
                obj = words[4]
            else:
                sub = words[0]
                pred = words[1] + " " + words[2]
                obj = words[3]
            subtype = Subtype(sub, obj)
            ds = Declaration('user', subtype)
            semantic.insert(ds)
            if len(semantic.query_local('user', e1=obj, rel='subtype')) > 0:
                # Get class in top of hierarchy
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
            return random.choice(responses) + " {} {} {}".format(sub, pred, obj)

        # Examples:
        # - What is my name?
        # Any question with 'What' that has 4 words
        elif condition.wp_vbz_prp_nn():
            print("What is my name?")
            obj = words[2] + " " + words[3]
            same_verb = False
            results = semantic.query_local('user', e1=obj)
            for sentence in results:
                res_sub = sentence.relation.entity1
                res_pred = sentence.relation.name
                red_obj = sentence.relation.entity2
                if words[1] in res_pred:
                    same_verb = True
                    break
            print("Asking about what " + words[3])
            if same_verb:
                output = '{} {} {}'.format(res_sub, res_pred, red_obj)
                return reflect(output)
            else:
                return "I don't know what " + reflect(words[2]) + " " + \
                       reflect(words[3]) + " " + words[1]


        # Examples:
        # - Do i have a cat
        elif condition.vbp_nns_vbp_dt_nn():
            print("Do  i have a cat")
            obj = words[4]
            sub = words[1]
            pred =words[2]+" "+words[3]
            another_case=words[3]+" "+words[4]
            last_sentence = False
            print(sub)
            results = semantic.query_local('user',e1=sub ,e2=obj)
            if (results==[]):
                results = semantic.query_local('user',e1=sub ,e2=another_case)
            print(results)
            for sentence in results:
                res_sub = sentence.relation.entity1
                res_pred = sentence.relation.name
                red_obj = sentence.relation.entity2

                if pred in res_pred or words[2] in res_pred:
                    if not last_sentence:
                        output = '{} {} {}'.format(res_sub, res_pred, red_obj)
                    else:
                        res_pred = nltk.word_tokenize(res_pred)
                        output += ", " + '{} {}'.format(res_pred[1], red_obj)
                    last_sentence = True
            if last_sentence:
                return reflect(output)
            else:
                output = "I don't know if " + reflect(words[1]) + " " +pred + " " + obj
                return output

        else:
            return smart_response(statement)

    elif len(tokens) == 3:

        # Examples:
        # - Who is John?
        if condition.wp_vbz_rb():
            print("Who is John?")
            obj = words[2]
            same_verb = False
            results = semantic.query_local('user', e1=obj)
            for sentence in results:
                res_sub = sentence.relation.entity1
                res_pred = sentence.relation.name
                res_obj = sentence.relation.entity2
                if words[1] in res_pred:
                    if not same_verb:
                        output = '{} {} {}'.format(res_sub, res_pred, res_obj)
                    else:
                        res_pred = nltk.word_tokenize(res_pred)
                        output += ", " + '{} {}'.format(res_pred[1], res_obj)
                    same_verb = True
            if same_verb:
                return reflect(output)
            else:
                output = "I don't know who is " + words[2]
                return output
        else:
            return smart_response(statement)
    else:
        return smart_response(statement)


def main():
    semantic_network = SemanticNetwork()
    condition = Condition()
    while True:
        statement = input("You > ")
        statement = statement.lower()
        if statement == "bye":
            print("Bot > bye")
            break
        print("Bot > " + analyse(statement, semantic_network, condition))


if __name__ == "__main__":
    main()
