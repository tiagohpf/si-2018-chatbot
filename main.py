import nltk
import re
import random
from reflections import *
from responses import *
from semantic_network import *
from constants import *
from conditions import Condition


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


def another_reflection(fragment):
    tokens = fragment.lower().split()
    for i, token in enumerate(tokens):
        if token in another_reflect:
            tokens[i] = another_reflect[token]
    return ' '.join(tokens)


def possessive_reflection(fragment):
    tokens = fragment.lower().split()
    for i, token in enumerate(tokens):
        if token in possession_reflect:
            tokens[i] = possession_reflect[token]
    return ' '.join(tokens)


def analyse(statement, semantic, condition):
    global red_obj
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
            print('nn_vb_in_dt_nn')
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
        # - What is the color of my boat?
        elif condition.wp_vbz_dt_nn_in_dt_nn():
            print('wp_vbz_dt_nn_in_dt_nn()')
            sub = words[3]
            out=""
            obj = words[5] + ' ' + words[6]
            results = semantic.query_local('user', e2=sub, rel='subtype')
            print(results)
            if len(results) > 0:
                output = ''
                for sentence in results:
                    res_sub = sentence.relation.entity1
                    red_obj = sentence.relation.entity2
                if red_obj == sub:
                    res_results = semantic.query_local('user', e2=obj)
                    for sentences in res_results:
                        sub_results = sentences.relation.entity1
                        pred_results = sentences.relation.name
                        if pred_results in VOWELS:
                            output += "an " + res_sub + " " + words[6]
                        else:
                            output += "a " + res_sub + " " + words[6]
                        out = '{} {} {}'.format(reflect(sub_results), pred_results, output)
                        return out
                output = "I dont know that but i know that " + random_knowledge_about(obj, semantic)
                return output
            else:
                results = semantic.query_local('user', e1=obj)

                output = "I dont know that but i know that "+random_knowledge_about(obj,semantic)
                print(output)
                count = 1
                for sentence in results:
                    sub = sentence.relation.entity1
                    pred = sentence.relation.name
                    obj = sentence.relation.entity2
                    output += reflect(sub + " " + pred + " "+obj)
                    adjectives = semantic.query_local('user', e1=obj, rel='adjective')
                    for adjective in adjectives:
                        if count == 1:
                            if obj[0] in VOWELS:
                                output += " an " + adjective.relation.entity2 + " " + adjective.relation.entity1
                            else:
                                output += " a " + adjective.relation.entity2 + " " + adjective.relation.entity1
                        elif 1 < count < len(adjectives):
                            if obj[0] in VOWELS:
                                output += " and an " + adjective.relation.entity2 + " " + adjective.relation.entity1
                            else:
                                output += " and a " + adjective.relation.entity2 + " " + adjective.relation.entity1
                        elif count == len(adjectives):
                            if obj[0] in VOWELS:
                                output += " and an " + adjective.relation.entity2 + " " + adjective.relation.entity1
                            else:
                                output += " and a " + adjective.relation.entity2 + " " + adjective.relation.entity1
                            break
                        count += 1
                return output
            return smart_response(statement)

        # Examples:
        # - What do you know about John?
        # - What do you know about my phone?
        elif condition.wp_vbp_prp_vb_in():
            print('wp_vbp_prp_vb_in || wp_vbz_rb')
            if len(tokens) == 7:
                sub = words[5] + ' ' + words[6]
            else:
                sub = words[5]
            sub = another_reflection(sub)
            results = semantic.query_local('user', e1=sub) + semantic.query_local('user', e2=sub)
            have_results = semantic.query_local('user', e1='i', rel='have')
            if len(results) > 0:
                output = ""
                count = 1
                for sentence in results:
                    sub = sentence.relation.entity1
                    pred = sentence.relation.name
                    obj = sentence.relation.entity2
                    if pred == 'subtype':
                        if obj[0] in VOWELS:
                            pred = 'is an'
                        else:
                            pred = 'is a'
                        if count == 1:
                            output += sub + " " + pred + " " + obj
                        elif 1 < count < len(results):
                            output += ", " + pred + " " + obj
                        elif count == len(results):
                            output += " and " + pred + " " + obj
                            break
                    elif pred == 'have' or pred == 'adjective' or pred == 'is':
                        if count == 1:
                            output += sub + " is " + obj
                        elif 1 < count < len(results) - len(have_results):
                            if pred != 'have':
                                output += ", " + obj
                        elif count == len(results) - len(have_results):
                            if pred != 'have':
                                output += " and " + obj
                            break
                    count += 1
                return reflect(output)
            return "I don't know anything about " + reflect(sub)
        else:
            return smart_response(statement)

    elif len(tokens) == 4 or len(tokens) == 5:
        # Examples:
        # - Where is my phone?
        # - Where is the phone?
        if condition.wrb_vb_dt_nn():
            print('wrb_vb_dt_nn')
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
                output = "I don't know where " + \
                         reflect(words[2]) + " " + \
                         reflect(words[3]) + " " + words[1]
                random_knowledge = random_knowledge_about(obj, semantic)
                if (random_knowledge != -1):
                    output += " but i know that " + random_knowledge
                return output

        # Examples:
        # - John is my friend
        # - John is a friend
        # - Subtype para alguns casos
        elif condition.nn_vbz_dt_nn(words[1] + " " + words[2]):
            print('nn_vbz_dt_nn')
            sub = words[0]
            pred = words[1]
            obj = words[2] + " " + words[3]
            a = Association(sub, pred, obj)
            da = Declaration("user", a)
            semantic.insert(da)
            output = random.choice(responses) + " " + reflect(statement)
            return output

        # Examples:
        # - My name is John Smith
        # - My name is Zé
        # Sometimes it detects JJ and NN in anothers
        elif condition.prp_nn_vbz_nn():
            print('prp_nn_vbz_nn')
            sub = words[0] + " " + words[1]
            pred = words[2]
            # With last name
            if len(tags) == 5:
                obj = words[3] + " " + words[4]
            else:
                obj = words[3]
            output = random.choice(responses) + " " + reflect(words[0]) + " " + \
                     words[1] + " " + pred + " " + obj
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
            print('dt_nn_vbz_dt_nn() || nn_vbz_dt_nn_subtype ')
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
            print('wp_vbz_prp_nn')
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
            if same_verb:
                output = '{} {} {}'.format(res_sub, res_pred, red_obj)
                return reflect(output)

            else:
                output = "I don't know what " + reflect(words[2]) + " " + \
                         reflect(words[3]) + " " + words[1]
                random_knowledge = random_knowledge_about(obj, semantic)
                if (random_knowledge != -1):
                    output += " but i know that " + random_knowledge
                return output

        # Examples:
        # - Do i have a cat?
        elif condition.vbp_nns_vbp_dt_nn():
            print('vbp_nns_vbp_dt_nn')
            sub = words[1]
            pred = words[2] + " " + words[3]
            obj = words[4]
            another_case = words[3] + " " + words[4]
            last_sentence = False

            results = semantic.query_local('user', e1=sub, e2=possessive_reflection(sub + ' ' + obj))
            if not results:
                results = semantic.query_local('user', e1=sub, e2=another_case)
            for sentence in results:
                res_sub = sentence.relation.entity1
                res_pred = sentence.relation.name
                red_obj = sentence.relation.entity2
                response = "Yes,"
                if red_obj in VOWELS:
                    pred = 'an'
                else:
                    pred = 'a'
                if pred in res_pred or words[2] in res_pred:
                    if not last_sentence:
                        output = '{} {} {} {} {}'.format(response, res_sub, res_pred, pred, obj)
                    else:
                        res_pred = nltk.word_tokenize(res_pred)
                        output += ", " + '{} {} {}'.format(res_pred[1], pred, red_obj)
                    last_sentence = True
            if last_sentence:
                return reflect(output)
            else:
                output = "I don't know if " + \
                         reflect(words[1]) + " " + pred + " " + obj
                random_knowledge = random_knowledge_about(obj, semantic)
                if random_knowledge != -1:
                    output += " but I know that " + random_knowledge
                return output

        # Examples:
        # - I have a red cat
        # - I have a cat
        elif condition.nns_vbp_dt_nn():
            print('nns_vbp_dt_nn')
            sub = words[0]
            pred = words[1]
            if len(tags) == 5:
                adj = words[3]
                obj = words[4]
                reflection = possessive_reflection(str(sub + ' ' + pred).replace(' ', '_')) + ' ' + obj
                if 'have' in pred:
                    assoc = Association(reflection, 'adjective', adj)
                    results = semantic.query_local('user', e1=reflection, rel='adjective') \
                              + semantic.query_local('user', rel='have', e2=reflection)
                    for result in results:
                        sub_res = result.relation.entity1
                        pred_res = result.relation.name
                        obj_res = result.relation.entity2
                        semantic.remove_instances(sub_res, pred_res, obj_res)
                else:
                    assoc = Association((sub + ' ' + pred), 'adjective', adj)
                d = Declaration('user', assoc)
                semantic.insert(d)
                assoc = Association(sub, pred, reflection)
                d = Declaration('user', assoc)
                semantic.insert(d)
                output = random.choice(responses) + " " + reflect(sub) + " " + pred + " " + words[
                    2] + " " + adj + " " + obj
            else:
                obj = words[3]
                reflection = possessive_reflection(str(sub + ' ' + pred).replace(' ', '_')) + ' ' + obj
                assoc = Association(sub, pred, reflection)
                d = Declaration('user', assoc)
                semantic.insert(d)
                output = random.choice(responses) + " " + reflect(sub) + " " + pred + " " + words[2] + " " + obj
            if len(semantic.query_local('user', e1=sub, rel=pred)) > 0:
                semantic.remove_instances(sub, pred, obj)
            if (words[3] == 'green' or words[3] == 'blue' or words[3] == 'red' or words[3] == 'yellow' or words[
                3] == 'orange'):
                subtype = Subtype(words[3], 'color')
                ds = Declaration('user', subtype)
                semantic.insert(ds)
            elif words[3] == 'new' or words[3] == 'old':
                subtype = Subtype(words[3], 'age')
                ds = Declaration('user', subtype)
                semantic.insert(ds)
            return output

        else:
            return smart_response(statement)

    elif len(tokens) == 3:

        # Examples:
        # - Who is John?
        if condition.wp_vbz_rb():
            print('wp_vbz_rb')
            sub = words[2]
            # change from me to I
            sub = another_reflection(sub)
            results = semantic.query_local('user', e1=sub) + semantic.query_local('user', e2=sub)
            if len(results) > 0:
                output = ""
                count = 1
                for sentence in results:
                    sub = sentence.relation.entity1
                    pred = sentence.relation.name
                    obj = sentence.relation.entity2
                    if pred == 'subtype':
                        if obj[0] in VOWELS:
                            pred = 'is an'
                        else:
                            pred = 'is a'
                    if count == 1:
                        output += sub + " " + pred + " " + obj + " "
                    elif 1 < count < len(results):
                        output += "and " + pred + " " + obj
                    elif count == len(results):
                        output += "and " + pred + " " + obj
                        break
                    count += 1
                return reflect(output)
            return "I don't know anything about " + reflect(sub)

        # Examples:
        # - John is Portuguese
        elif condition.nn_vbz_jj():
            print('nn_vbz_jj')
            sub = words[0]
            pred = words[1]
            obj = words[2]
            a = Association(sub, pred, obj)
            da = Declaration("user", a)
            semantic.insert(da)
            output = random.choice(responses) + " " + reflect(statement)
            return output
    else:
        return smart_response(statement)


def random_knowledge_about(entity, semantic):
    results = semantic.query_local('user', e1=entity) + semantic.query_local('user', e2=entity)
    split = entity.split(" ")
    if len(split) > 1:
        results += semantic.query_local('user', e1=split[1]) + semantic.query_local('user', e2=split[1])
    if len(results) > 0:
        rand = random.randint(0, len(results) - 1)
        sub = results[rand].relation.entity1
        pred = results[rand].relation.name
        obj = results[rand].relation.entity2

        output = sub + " " + pred + " " + obj
        return reflect(output)
    else:
        return -1


def main():
    semantic_network = SemanticNetwork()
    condition = Condition()
    while True:
        statement = input("You > ")
        statement = statement.lower().replace('?', '')
        if statement == "bye":
            print("Bot > bye")
            break
        print("Bot > " + analyse(statement, semantic_network, condition))


if __name__ == "__main__":
    main()
