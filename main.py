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


def get_verb_dt(next_letter):
    if next_letter in VOWELS:
        return 'is an'
    return 'is a'


def analyse(statement, semantic, condition):
    global red_obj
    tokens = nltk.word_tokenize(statement)
    tags = nltk.pos_tag(tokens)

    # Print values
    # for sentence in tags:
    # print(sentence)

    words = [word for word, statement in tags]
    statements = [statement for word, statement in tags]
    condition.set_statements(statements)

    if len(tokens) == 6 or len(tokens) == 7:
        # Examples:
        # - My phone is on the table
        # - My food is on the fridge
        # - The phone is on the table
        if condition.dt_nn_vb_in_dt_nn():
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
        # - What is the age of my cat?
        # Ask only about the age or the color
        elif condition.wp_vbz_dt_nn_in_dt_nn():
            sub = words[3]
            if sub != 'age' and sub != 'color':
                return "Sorry, I don't know " + reflect(statement)
            obj = words[5] + ' ' + words[6]
            # Search for "have(I, my cat)" to assure that I have a cat
            pred_have = semantic.query_local('user', e2=obj, rel='have')
            if len(pred_have) > 0:
                # Search for "adjective(my cat, age)"
                pred_adjs = semantic.query_local('user', e1=obj, rel='adjective')[0]
                # Search for "member(red, color)"
                content = semantic.query_local('user', e1=pred_adjs.relation.entity2, e2=sub, rel='member')
                if len(content) > 0:
                    return 'The ' + sub + ' of ' + reflect(obj) + ' is ' + content[0].relation.entity1
                else:
                    return "I don't know the " + sub + ' of ' + reflect(obj)
            else:
                output = "You don't have "
                if words[6][0] in VOWELS:
                    output += 'an '
                else:
                    output += 'a '
                output += words[6]
                return output
            return smart_response(statement)
        else:
            return smart_response(statement)

    elif len(tokens) == 4 or len(tokens) == 5:
        # Examples:
        # - Where is my phone?
        # - Where is the phone?
        if condition.wrb_vb_dt_nn():
            obj = words[2] + ' ' + words[3]
            places = semantic.get_places_of_obj(obj)[1:]
            if len(places) > 0:
                output = reflect(obj) + ' '
                for place in places:
                    output += place + ', '
                return output[:-2]
            else:
                output = "I don't know where " + \
                         reflect(words[2]) + " " + \
                         reflect(words[3]) + " " + words[1]
                random_knowledge = random_knowledge_about(obj, semantic)
                if random_knowledge != -1:
                    output += " but I know that " + random_knowledge
                return output

        # Examples:
        # - John is my friend
        # - John is the father
        elif condition.nn_vbz_dt_nn(words[1] + ' ' + words[2]):
            sub = words[0]
            pred = words[1]
            obj = words[2] + ' ' + words[3]
            assoc = Association(sub, pred, obj)
            dec = Declaration('user', assoc)
            pred_have = semantic.query_local(user='user', e1=sub, rel=pred)
            if len(pred_have) == 0:
                semantic.insert_instance(dec)
            else:
                substituted = False
                for declaration in pred_have:
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
            sub = words[0] + " " + words[1]
            pred = words[2]
            # With last name
            if len(tags) == 5:
                obj = words[3] + " " + words[4]
            else:
                obj = words[3]
            output = random.choice(responses) + " " + reflect(words[0]) + " " + \
                     words[1] + " " + pred + " " + obj
            pred_have = semantic.query_local('user', e1=sub, rel=pred)
            remove_queries(pred_have, semantic)
            assoc = Association(sub, pred, obj)
            dec = Declaration('user', assoc)
            semantic.insert_instance(dec)
            return output

        # Examples:
        # - A cat is an animal
        # - Pussycat is a cat
        elif condition.dt_nn_vbz_dt_nn() or condition.nn_vbz_dt_nn_subtype():
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
                sentence = get_verb_dt(root[0])
                assoc = Association(sub, sentence, root)
                dec = Declaration('user', assoc)
                semantic.insert_instance(dec)
                return 'So, {} {} {}'.format(sub, sentence, root)
            return random.choice(responses) + " {} {} {}".format(sub, pred, obj)

        # Examples:
        # - What is my name?
        # - What is her age?
        # Any question with 'What' that has 4 words
        elif condition.wp_vbz_prp_nn():
            pred = words[1]
            obj = words[2] + ' ' + words[3]
            declaration = semantic.query_local('user', e1=obj, rel=pred)
            if len(declaration) > 0:
                res_sub = declaration[0].relation.entity1
                res_pred = declaration[0].relation.name
                res_obj = declaration[0].relation.entity2
                output = '{} {} {}'.format(res_sub, res_pred, res_obj)
                return reflect(output)
            else:
                output = "I don't know what " + reflect(words[2]) + " " + \
                         reflect(words[3]) + " " + words[1]
                random_knowledge = random_knowledge_about(obj, semantic)
                if random_knowledge != -1:
                    output += " but i know that " + random_knowledge
                return output

        # Examples:
        # - Do I have a cat?
        elif condition.vbp_nns_vbp_dt_nn():
            sub = words[1]
            pred = words[2] + " " + words[3]
            obj = words[4]
            another_case = words[3] + " " + words[4]
            last_sentence = False

            pred_have = semantic.query_local(
                'user', e1=sub, e2=possessive_reflection(sub + ' ' + obj))
            if not pred_have:
                pred_have = semantic.query_local('user', e1=sub, e2=another_case)
            for sentence in pred_have:
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
                pred_have = semantic.query_local('user', e1=my_obj, rel='adjective') \
                            + semantic.query_local('user', e1=sub, e2=my_obj) \
                            + semantic.query_local('user', rel='member', e2='color') \
                            + semantic.query_local('user', rel='member', e2='age')
                remove_queries(pred_have, semantic)
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
            else:
                obj = words[3]
                if 'have' in pred:
                    # Transform to "have(I, my cat)"
                    my_obj = possessive_reflection(str(sub + ' ' + pred).replace(' ', '_')) + ' ' + obj
                else:
                    # Transform to "need(I, cat)"
                    my_obj = obj
                # Remove relations with same subject and object
                pred_have = semantic.query_local('user', e1=sub, e2=my_obj)
                remove_queries(pred_have, semantic)
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
            sub = words[2]
            sub = another_reflection(sub)
            pred_have = semantic.query_local('user', e1=sub) + semantic.query_local('user', e2=sub)
            if len(pred_have) > 0:
                output = ''
                count = 1
                for sentence in pred_have:
                    sub_res = sentence.relation.entity1
                    pred_res = sentence.relation.name
                    obj_res = sentence.relation.entity2
                    if pred_res == 'subtype' or pred_res == 'member':
                        pred_res = get_verb_dt(obj_res[0])
                    if count == 1:
                        output += sub_res + ' ' + pred_res + ' ' + obj_res
                    elif 1 < count < len(pred_have):
                        output += ', ' + pred_res + ' ' + obj_res
                    elif count == len(pred_have):
                        output += ' and ' + pred_res + ' ' + obj_res
                    count += 1
                return reflect(output)
            return "I don't know anything about " + reflect(sub)

        # Examples:
        # - John is english
        # - John is nice
        elif condition.nn_vbz_jj():
            sub = words[0]
            pred = words[1]
            obj = words[2]
            query = semantic.query_local('user', e1=sub, rel=pred, e2=obj)
            if len(query) == 0:
                assoc = Association(sub, pred, obj)
                dec = Declaration("user", assoc)
                semantic.insert_instance(dec)
            output = random.choice(responses) + " " + reflect(statement)
            return output
    else:
        return smart_response(statement)
    return smart_response(statement)


def random_knowledge_about(entity, semantic):
    results = semantic.query_local('user', e1=entity) + semantic.query_local('user', e2=entity)
    split = entity.split(' ')
    if len(split) > 1:
        results += semantic.query_local('user', e1=split[1]) + semantic.query_local('user', e2=split[1])
    if len(results) > 0:
        rand = random.randint(0, len(results) - 1)
        sub = results[rand].relation.entity1
        pred = results[rand].relation.name
        obj = results[rand].relation.entity2
        if pred == 'subtype' or pred == 'member':
            pred = get_verb_dt(obj[0])
        output = sub + " " + pred + " " + obj
        predecessors = semantic.path_to_root(obj)
        count = 0
        for predecessor in predecessors:
            count += 1
            if count == len(predecessors):
                output += ' and '
            else:
                output += ', '
            output += get_verb_dt(predecessor[0]) + ' ' + predecessor
        return reflect(output)
    else:
        return -1


def main():
    semantic_network = SemanticNetwork()
    condition = Condition()
    file = open('conversation.txt', 'w')
    welcome = "Bot > Hello, welcome to our chat!"
    print(welcome)
    file.write(welcome + "\n\n")
    while True:
        statement = input("You > ")
        file.write("You > " + statement + "\n\n")
        statement = statement.lower().replace('?', '').replace('.', '').strip()
        if statement == "bye":
            bye = "Bot > Bye Bye! ;)"
            print(bye)
            file.write(bye + "\n")
            break
        response = "Bot > " + analyse(statement, semantic_network, condition)
        print(response)
        file.write(response + "\n\n")
    file.close()


if __name__ == "__main__":
    main()
