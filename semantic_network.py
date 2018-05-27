# -*- coding: utf-8 -*-
from collections import Counter


# Classe Relation, com as seguintes classes derivadas:
#     - Association - uma associacao generica entre duas entidades
#     - Subtype     - uma relacao de subtipo entre dois tipos
#     - Member      - uma relacao de pertenca de uma instancia a um tipo
#

class Relation:
    def __init__(self, e1, rel, e2):
        self.entity1 = e1
        #       self.relation = rel  # obsoleto
        self.name = rel
        self.entity2 = e2

    def __str__(self):
        return self.name + "(" + str(self.entity1) + "," + \
               str(self.entity2) + ")"

    def __repr__(self):
        return str(self)


# Subclasse Association
class Association(Relation):
    def __init__(self, e1, assoc, e2):
        Relation.__init__(self, e1, assoc, e2)


# Exemplo:
#   a = Association('socrates','professor','filosofia')

# Subclasse Subtype
class Subtype(Relation):
    def __init__(self, sub, super):
        Relation.__init__(self, sub, "subtype", super)


# Exemplo:
#   s = Subtype('homem','mamifero')

# Subclasse Member
class Member(Relation):
    def __init__(self, obj, type):
        Relation.__init__(self, obj, "member", type)


# 16. a) criar duas classes derivadas de Relations: AssocOne (aceita um único valor) e AssocNum(aceita valores numéricos)
class AssocOne(Relation):
    def __init__(self, e1, assoc, e2):
        Relation.__init__(self, e1, assoc, e2)


class AssocNum(Relation):
    def __init__(self, e1, assoc, e2):
        Relation.__init__(self, e1, assoc, e2)


# Exemplo:
#   m = Member('socrates','homem')

# classe Declaration
# -- associa um utilizador a uma relacao por si inserida
#    na rede semantica
#
class Declaration:
    def __init__(self, user, rel):
        self.user = user
        self.relation = rel

    def __str__(self):
        return "decl(" + str(self.user) + "," + str(self.relation) + ")"

    def __repr__(self):
        return str(self)


# Exemplos:
#   da = Declaration('descartes',a)
#   ds = Declaration('darwin',s)
#   dm = Declaration('descartes',m)

# classe SemanticNetwork
# -- composta por um conjunto de declaracoes
#    armazenado na forma de uma lista
#
class SemanticNetwork:
    def __init__(self, ldecl=[]):
        self.declarations = ldecl

    def __str__(self):
        return self.my_list2string(self.declarations)

    def insert(self, decl):
        self.declarations.append(decl)

    def query_local(self, user=None, e1=None, rel=None, e2=None):
        self.query_result = \
            [d for d in self.declarations
             if (user == None or d.user == user)
             and (e1 == None or d.relation.entity1 == e1)
             and (rel == None or d.relation.name == rel)
             and (e2 == None or d.relation.entity2 == e2)]
        return self.query_result

    def show_query_result(self):
        for d in self.query_result:
            print(str(d))

    def remove_instances(self, entity1, rel, obj):
        queries = self.query_local('user', entity1, rel, obj)
        for query in queries:
            self.declarations.remove(query)

    # 1. verificar se entity1 é predecessor de e2
    def predecessor(self, pred, suc):
        declarations = self.query_local(e1=suc, rel='subtype') + \
                       self.query_local(e1=suc, rel='member')
        if declarations == []:
            return False
        for query in declarations:
            if query.relation.entity2 == pred:
                return True
            else:
                return self.predecessor(pred, query.relation.entity2)

    def path_to_root(self, entity):
        direct_relations = [d for d in self.declarations if d.relation.entity1 == entity]
        if direct_relations is []:
            return []
        inheritances = [d for d in direct_relations
                        if isinstance(d.relation, Subtype) or isinstance(d.relation, Member)]
        parents = [d.relation.entity2 for d in inheritances]
        for d in inheritances:
            parents += self.path_to_root(d.relation.entity2)
        return parents

    # 2. caminho de uma entidade até ao seu predecessor
    def predecessor_path(self, pred, suc):
        declarations = self.query_local(e1=suc, rel='subtype') + \
                       self.query_local(e1=suc, rel='member')
        if declarations == []:
            return None
        for query in declarations:
            if query.relation.entity2 == pred:
                return [suc, pred]
            else:
                return [suc] + self.predecessor_path(pred, query.relation.entity2)

    # 3. associações existentes
    def associations(self):
        return list(set([d.relation.name for d in self.declarations if isinstance(d.relation, Association)]))

    # 4. instâncias de objetos
    def instances(self):
        return list(set([d.relation.entity1 for d in self.declarations if isinstance(d.relation, Member)]))

    # 5. interlocutores
    def interlocutores(self):
        return list(set([d.user for d in self.declarations]))

    # 6. tipos existentes da rede
    def types(self):
        return list(set([d.relation.entity1 for d in self.declarations if isinstance(d.relation, Subtype)] +
                        [d.relation.entity2 for d in self.declarations if isinstance(d.relation, Subtype)]))

    # 7. associações de uma entidade
    def entityAssociations(self, entity):
        return list(set([d.relation.name for d in self.declarations if d.relation.entity1 == entity and
                         isinstance(d.relation, Association)]))

    # 8. relações declaradas pelo interlocutor
    def userDeclarations(self, user):
        return list(set([d.relation.name for d in self.declarations if d.user == user]))

    # 9. número de associações utilizadas nas relações declaradas por um interlocutor
    def numAssociations(self, user):
        return len(set([d.relation.name for d in self.declarations
                        if isinstance(d.relation, Association) and d.user == user]))

    # 10. lista de tuplos (associação, interlocutor) de uma entidade
    def entityAssociations(self, entity):
        return [(d.relation.name, d.user) for d in self.declarations
                if isinstance(d.relation, Association) and d.relation.entity1 == entity]

    # 11 a). associações locais ou herdades por uma entidade
    def query(self, entity, rel=None):
        direct_dec = [d for d in self.declarations if d.relation.entity1 == entity]
        if direct_dec == []:
            return []
        relations = [d for d in direct_dec
                     if isinstance(d.relation, Association)
                     and (d.relation.name == rel or rel is None)]
        parents = [d.relation.entity2 for d in direct_dec
                   if isinstance(d.relation, Member) or isinstance(d.relation, Subtype)]
        for d in parents:
            relations += self.query(d, rel)
        return relations

    # 11 b). declarações locais ou associações herdadas por uma entidade
    def query2(self, entity, rel=None):
        direct_dec = [d for d in self.declarations
                      if d.relation.entity1 == entity]
        if direct_dec == []:
            return []
        relations = [d for d in direct_dec if rel is None or d.relation.name == rel] + \
                    [d for d in direct_dec if isinstance(d.relation, Subtype) or isinstance(d.relation, Member)]
        parents = [d.relation.entity2 for d in direct_dec
                   if isinstance(d.relation, Member) or isinstance(d.relation, Subtype)]
        for d in parents:
            relations += self.query2(d, rel)
        return relations

    # 12. query() com cancelamento de herança
    def query_cancel(self, entity, rel, assoc=[]):
        declarations = [d for d in self.declarations if d.relation.entity1 == entity]
        if declarations == []:
            return []
        relations = [d for d in declarations
                     if d.relation.name == rel
                     and isinstance(d.relation, Association)
                     and d.relation.name not in assoc]
        assoc += [d.relation.name for d in relations]
        parents = [d.relation.entity2 for d in declarations
                   if (isinstance(d.relation, Subtype) or isinstance(d.relation, Member))]
        for d in parents:
            relations += self.query_cancel(d, rel, assoc)
        return relations

    # 13. valor da associação A na entidade E
    def query_assoc_value(self, entity, association):
        declarations = [d for d in self.declarations if d.relation.entity1 == entity]
        if declarations == []:
            return None
        values = [d.relation.entity2 for d in declarations if d.relation.name == association]
        if len(values) == 1:
            return values[0]
        parents_values = [d.relation.entity2 for d in self.query(entity, association)
                          if d.relation.entity1 is not entity]
        cLocal = Counter(values)
        if parents_values == []:
            return max([v for v in cLocal if cLocal[v] == max(cLocal.values())])
        cParents = Counter(parents_values)
        cValues = cLocal + cParents
        maxim = value = None
        for v in cValues:
            l = (cLocal[v] / len(list(cLocal.elements()))) * 100
            h = (cParents[v] / len(list(cParents.elements()))) * 100
            f = (l + h) / 2
            if maxim is None or f > maxim:
                maxim = f
                value = v
        return value

    # 14. associações das entidades descendentes de um tipo
    def query_down(self, parent, assoc):
        declarations = [d for d in self.declarations if d.relation.entity1 == parent or d.relation.entity2 == parent]
        if declarations == []:
            return []
        relations = [d for d in declarations if d.relation.name == assoc and isinstance(d.relation, Association)]
        childs = [d.relation.entity1 for d in declarations
                  if (isinstance(d.relation, Subtype) or isinstance(d.relation, Member))
                  and d.relation.entity2 == parent]
        for d in childs:
            relations += self.query_down(d, assoc)
        return relations

    # 15. dado um tipo e uma associação, devolver valor mais frequente nas entidades descendentes
    def query_induce(self, entity, association):
        values = [d.relation.entity2 for d in self.query_down(entity, association)]
        counter = Counter(values)
        if len(counter) == 0:
            return None
        maxim = v = None
        for i in values:
            if maxim is None or counter[i] > maxim:
                maxim = counter[i]
                v = i
        return v

    # 16 b). consultas de valores em diferentes tipos de associações locais
    def query_local_assoc(self, entity, association):
        values = [d.relation.entity2 for d in self.declarations
                  if d.relation.entity1 == entity and d.relation.name == association]
        if values == []:
            return None
        counter = Counter(values)
        if association in [d.relation.name for d in self.declarations if isinstance(d.relation, Association)]:
            lst = []
            sum_freq = 0
            while sum_freq < 0.75:
                maxim = value = None
                for v in counter:
                    res = round(counter[v] / len(list(counter.elements())), 2)
                    if (maxim is None or res > maxim) and (v, res) not in lst:
                        maxim = res
                        value = v
                lst.append((value, maxim))
                sum_freq += maxim
            return lst
        elif association in [d.relation.name for d in self.declarations if isinstance(d.relation, AssocOne)]:
            maxim = value_frequent = None
            for v in counter:
                res = counter[v] / len(list(counter.elements()))
                if maxim is None or res > maxim:
                    maxim = res
                    value_frequent = v
            return value_frequent, round(maxim, 2)
        elif association in [d.relation.name for d in self.declarations if isinstance(d.relation, AssocNum)]:
            return round(sum(values) / len(values), 1)

    # Funcao auxiliar para converter para cadeias de caracteres
    # listas cujos elementos sejam convertiveis para
    # cadeias de caracteres
    def my_list2string(list):
        if list == []:
            return "[]"
        s = "[ " + str(list[0])
        for i in range(1, len(list)):
            s += ", " + str(list[i])
        return s + " ]"
