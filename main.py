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


def remove_queries(queries, semantic):
    for declaration in queries:
        sub_to_remove = declaration.relation.entity1
        pred_to_remove = declaration.relation.name
        obj_to_remove = declaration.relation.entity2
        semantic.remove_instances(sub_to_remove, pred_to_remove, obj_to_remove)


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
            assoc = Association(sub, pred, obj)
            dec = Declaration('user', assoc)
            if len(semantic.query_local('user', sub, pred)) > 0:
                semantic.remove_instances(sub, pred)
            semantic.insert_instance(dec)
            return random.choice(responses) + ' ' + reflect(statement)

        # Examples:
        # - What is the color of my boat?
        elif condition.wp_vbz_dt_nn_in_dt_nn():
            print('wp_vbz_dt_nn_in_dt_nn()')
            sub = words[3]
            out = ""
            obj = words[5] + ' ' + words[6]
            queries = semantic.query_local('user', e2=sub, rel='subtype')
            print(queries)
            if len(queries) > 0:
                output = ''
                for sentence in queries:
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
                            output += "assoc " + res_sub + " " + words[6]
                        out = '{} {} {}'.format(
                            reflect(sub_results), pred_results, output)
                        return out
                output = "I dont know that but i know that " + \
                         random_knowledge_about(obj, semantic)
                return output
            else:
                queries = semantic.query_local('user', e1=obj)

                output = "I dont know that but i know that " + \
                         random_knowledge_about(obj, semantic)
                print(output)
                count = 1
                for sentence in queries:
                    sub = sentence.relation.entity1
                    pred = sentence.relation.name
                    obj = sentence.relation.entity2
                    output += reflect(sub + " " + pred + " " + obj)
                    adjectives = semantic.query_local(
                        'user', e1=obj, rel='adjective')
                    for adjective in adjectives:
                        if count == 1:
                            if obj[0] in VOWELS:
                                output += " an " + adjective.relation.entity2 + " " + adjective.relation.entity1
                            else:
                                output += " assoc " + adjective.relation.entity2 + " " + adjective.relation.entity1
                        elif 1 < count < len(adjectives):
                            if obj[0] in VOWELS:
                                output += " and an " + adjective.relation.entity2 + \
                                          " " + adjective.relation.entity1
                            else:
                                output += " and assoc " + adjective.relation.entity2 + " " + adjective.relation.entity1
                        elif count == len(adjectives):
                            if obj[0] in VOWELS:
                                output += " and an " + adjective.relation.entity2 + \
                                          " " + adjective.relation.entity1
                            else:
                                output += " and assoc " + adjective.relation.entity2 + " " + adjective.relation.entity1
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
            queries = semantic.query_local(
                'user', e1=sub) + semantic.query_local('user', e2=sub)
            have_results = semantic.query_local('user', e1='i', rel='have')
            if len(queries) > 0:
                output = ""
                count = 1
                for sentence in queries:
                    sub = sentence.relation.entity1
                    pred = sentence.relation.name
                    obj = sentence.relation.entity2
                    if pred == 'subtype':
                        if obj[0] in VOWELS:
                            pred = 'is an'
                        else:
                            pred = 'is assoc'
                        if count == 1:
                            output += sub + " " + pred + " " + obj
                        elif 1 < count < len(queries):
                            output += ", " + pred + " " + obj
                        elif count == len(queries):
                            output += " and " + pred + " " + obj
                            break
                    elif pred == 'have' or pred == 'adjective' or pred == 'is':
                        if count == 1:
                            output += sub + " is " + obj
                        elif 1 < count < len(queries) - len(have_results):
                            if pred != 'have':
                                output += ", " + obj
                        elif count == len(queries) - len(have_results):
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
            queries = semantic.query_local('user', obj)
            for sentence in queries:
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
                if random_knowledge != -1:
                    output += " but i know that " + random_knowledge
                return output

        # Examples:
        # - John is my friend
        # - John is the father
        elif condition.nn_vbz_dt_nn(words[1] + ' ' + words[2]):
            print('nn_vbz_dt_nn')
            sub = words[0]
            pred = words[1]
            obj = words[2] + ' ' + words[3]
            assoc = Association(sub, pred, obj)
            dec = Declaration('user', assoc)
            queries = semantic.query_local(user='user', e1=sub, rel=pred)
            if len(queries) == 0:
                semantic.insert_instance(dec)
            else:
                substituted = False
                for declaration in queries:
                    if words[3] in declaration.relation.entity2:
                        sub_to_remove = declaration.relation.entity1
                        pred_to_remove = declaration.relation.name
                        obj_to_remove = declaration.relation.entity2
                        semantic.remove_instances(sub_to_remove, pred_to_remove, obj_to_remove)
                        semantic.insert_instance(dec)
                        substituted = True
                if not substituted:
                    semantic.insert_instance(dec)
            return random.choice(responses) + ' ' + reflect(statement)

        # Examples:
        # - My name is John
        # - My name is John Smith
        # Sometimes it detects JJ and NN in another situations
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
                semantic.remove_instances(sub, pred)
            assoc = Association(sub, pred, obj)
            dec = Declaration('user', assoc)
            semantic.insert_instance(dec)
            return output

        # Examples:
        # - A cat is an animal
        # - Pussycat is a cat
        elif condition.dt_nn_vbz_dt_nn() or condition.nn_vbz_dt_nn_subtype():
            print('dt_nn_vbz_dt_nn || nn_vbz_dt_nn_subtype ')
            if condition.dt_nn_vbz_dt_nn():
                sub = words[1]
                pred = words[2] + " " + words[3]
                obj = words[4]
            else:
                sub = words[0]
                pred = words[1] + " " + words[2]
                obj = words[3]
            subtype = Subtype(sub, obj)
            dec = Declaration('user', subtype)
            semantic.insert_instance(dec)
            if len(semantic.query_local('user', e1=obj, rel='subtype')) > 0:
                # Get class in top of hierarchy
                root = semantic.path_to_root(sub)[-1]
                if root[0] in VOWELS:
                    sentence = 'is an'
                else:
                    sentence = 'is a'
                assoc = Association(sub, sentence, root)
                dec = Declaration('user', assoc)
                semantic.insert_instance(dec)
                return 'So, {} {} {}'.format(sub, sentence, root)
            return random.choice(responses) + " {} {} {}".format(sub, pred, obj)

        # Examples:
        # - What is my name?
        # Any question with 'What' that has 4 words
        elif condition.wp_vbz_prp_nn():
            print('wp_vbz_prp_nn')
            obj = words[2] + " " + words[3]
            same_verb = False
            queries = semantic.query_local('user', e1=obj)
            for sentence in queries:
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
        # - Do I have assoc cat?
        elif condition.vbp_nns_vbp_dt_nn():
            print('vbp_nns_vbp_dt_nn')
            sub = words[1]
            pred = words[2] + " " + words[3]
            obj = words[4]
            another_case = words[3] + " " + words[4]
            last_sentence = False

            queries = semantic.query_local(
                'user', e1=sub, e2=possessive_reflection(sub + ' ' + obj))
            if not queries:
                queries = semantic.query_local('user', e1=sub, e2=another_case)
            for sentence in queries:
                res_sub = sentence.relation.entity1
                res_pred = sentence.relation.name
                red_obj = sentence.relation.entity2
                response = "Yes,"
                if red_obj in VOWELS:
                    pred = 'an'
                else:
                    pred = 'assoc'
                if pred in res_pred or words[2] in res_pred:
                    if not last_sentence:
                        output = '{} {} {} {} {}'.format(
                            response, res_sub, res_pred, pred, obj)
                    else:
                        res_pred = nltk.word_tokenize(res_pred)
                        output += ", " + \
                                  '{} {} {}'.format(res_pred[1], pred, red_obj)
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
        # - I need a red cat
        # - I need a cat
        elif condition.nns_vbp_dt_nn():
            print('nns_vbp_dt_nn')
            sub = words[0]
            pred = words[1]
            if len(tags) == 5:
                adj = words[3]
                obj = words[4]
                if 'have' in pred:
                    # Transform to: "have(I, my cat)" and "adjective(my cat, red)"
                    my_obj = possessive_reflection(str(sub + ' ' + pred).replace(' ', '_')) + ' ' + obj
                else:
                    # Transform to: "need(I, cat)" and "adjective(cat, red)"
                    my_obj = obj
                # Search and remove "adjective(my cat, red)", "have(I, my cat)" and "subtype(red, color)"
                # when changes color
                queries = semantic.query_local('user', e1=my_obj, rel='adjective') \
                          + semantic.query_local('user', e1=sub, e2=my_obj) \
                          + semantic.query_local('user', rel='member', e2='color') \
                          + semantic.query_local('user', rel='member', e2='age')
                remove_queries(queries, semantic)
                # Insert "adjective(my cat, red)" or "adjective(cat, red)"
                assoc = Association(my_obj, 'adjective', adj)
                dec = Declaration('user', assoc)
                semantic.insert_instance(dec)
                # Insert "have(I, my cat)" or "need(I, cat)"
                assoc = Association(sub, pred, my_obj)
                dec = Declaration('user', assoc)
                semantic.insert_instance(dec)
                # Insert "member(red, color)" or "member(old, age)"
                if adj in COLORS:
                    member = Member(adj, 'color')
                    dec = Declaration('user', member)
                    semantic.insert_instance(dec)
                elif adj in AGE:
                    member = Member(adj, 'age')
                    dec = Declaration('user', member)
                    semantic.insert_instance(dec)
                output = random.choice(responses) + " " + reflect(sub) + " " + pred + " " \
                         + words[2] + " " + adj + " " + obj
                print(semantic.declarations)
            else:
                obj = words[3]
                if 'have' in pred:
                    # Transform to "have(I, my cat)"
                    my_obj = possessive_reflection(str(sub + ' ' + pred).replace(' ', '_')) + ' ' + obj
                else:
                    # Transform to "need(I, cat)"
                    my_obj = obj
                # Remove relations with same subject and object
                queries = semantic.query_local('user', e1=sub, e2=my_obj)
                remove_queries(queries, semantic)
                assoc = Association(sub, pred, my_obj)
                dec = Declaration('user', assoc)
                semantic.insert_instance(dec)
                output = random.choice(responses) + ' ' + reflect(sub) + ' ' + pred + ' ' + words[2] + ' ' + obj
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
            queries = semantic.query_local(
                'user', e1=sub) + semantic.query_local('user', e2=sub)
            if len(queries) > 0:
                output = ""
                count = 1
                for sentence in queries:
                    sub = sentence.relation.entity1
                    pred = sentence.relation.name
                    obj = sentence.relation.entity2
                    if pred == 'subtype':
                        if obj[0] in VOWELS:
                            pred = 'is an'
                        else:
                            pred = 'is assoc'
                    if count == 1:
                        output += sub + " " + pred + " " + obj + " "
                    elif 1 < count < len(queries):
                        output += "and " + pred + " " + obj
                    elif count == len(queries):
                        output += "and " + pred + " " + obj
                        break
                    count += 1
                return reflect(output)
            return "I don't know anything about " + reflect(sub)

        # Examples:
        # - John is english
        # - John is nice
        elif condition.nn_vbz_jj():
            print('nn_vbz_jj')
            sub = words[0]
            pred = words[1]
            obj = words[2]
            assoc = Association(sub, pred, obj)
            dec = Declaration("user", assoc)
            semantic.insert_instance(dec)
            output = random.choice(responses) + " " + reflect(statement)
            return output
    else:
        return smart_response(statement)
    # Precisa de estar aqui para frases não suportadas, i am nice por exemplo
    return smart_response(statement)


def random_knowledge_about(entity, semantic):
    results = semantic.query_local(
        'user', e1=entity) + semantic.query_local('user', e2=entity)
    split = entity.split(" ")
    if len(split) > 1:
        results += semantic.query_local(
            'user', e1=split[1]) + semantic.query_local('user', e2=split[1])
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
