# Relation between two entities
# (e1, rel, e2)
class Relation:
    def __init__(self, e1, rel, e2):
        self.entity1 = e1
        self.name = rel
        self.entity2 = e2

    def __str__(self):
        return self.name + "(" + str(self.entity1) + "," + str(self.entity2) + ")"

    def __repr__(self):
        return str(self)


class Association(Relation):
    def __init__(self, e1, assoc, e2):
        Relation.__init__(self, e1, assoc, e2)


class Subtype(Relation):
    def __init__(self, sub, super):
        Relation.__init__(self, sub, "subtype", super)


class Member(Relation):
    def __init__(self, obj, type):
        Relation.__init__(self, obj, "member", type)


class Declaration:
    def __init__(self, user, rel):
        self.user = user
        self.relation = rel

    def __str__(self):
        return "decl(" + str(self.user) + "," + str(self.relation) + ")"

    def __repr__(self):
        return str(self)

# Set of triples manage in a list
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
             if (user is None or d.user == user)
             and (e1 is None or d.relation.entity1 == e1)
             and (rel is None or d.relation.name == rel)
             and (e2 is None or d.relation.entity2 == e2)]
        return self.query_result

    def show_query_result(self):
        for d in self.query_result:
            print(str(d))

    def remove_instances(self, entity1, rel, obj=None):
        queries = self.query_local('user', entity1, rel, obj)
        for query in queries:
            self.declarations.remove(query)

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

    # Convert lists to set of characters
    def my_list2string(lst):
        if lst is []:
            return "[]"
        s = "[ " + str(lst[0])
        for i in range(1, len(lst)):
            s += ", " + str(lst[i])
        return s + " ]"
