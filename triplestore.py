class TripleStore:
    def __init__(self):
        self.spo = []

    def add_triple(self, sub, pred, obj):
        if (sub or pred or obj) and ((sub, pred, obj) not in self.spo):
            self.spo.append((sub, pred, obj))

    def remove_triples(self, sub, pred, obj):
        for del_sub, del_pred, del_obj in self.triples(sub, pred, obj):
            self.spo.remove(tuple([del_sub, del_pred, del_obj]))

    def triples(self, sub, pred, obj):
        triples_list = []
        if sub is not None:
            if pred is not None:
                if obj is not None:
                    # (sub, pred, obj)
                    for triple in self.spo:
                        if triple == (sub, pred, obj):
                            triples_list.append(triple);
                else:
                    # (sub, pred, None)
                    for triple in self.spo:
                        if triple[0] == sub and triple[1] == pred:
                            triples_list.append(triple);
            else:
                if obj is not None:
                    # (sub, None, obj)
                    for triple in self.spo:
                        if triple[0] == sub and triple[2] == obj:
                            triples_list.append(triple);
                else:
                    # (sub, None, None)
                    for triple in self.spo:
                        if triple[0] == sub:
                            triples_list.append(triple);
        else:
            if pred is not None:
                if obj is not None:
                    # (None, pred, obj)
                    for triple in self.spo:
                        if triple[1] == pred and triple[2] == obj:
                            triples_list.append(triple);
                else:
                    # (None, pred, None)
                    for triple in self.spo:
                        if triple[1] == pred:
                            triples_list.append(triple);
            else:
                # (None, None, obj)
                if obj is not None:
                    for triple in self.spo:
                        if triple[2] == obj:
                            triples_list.append(triple);
                else:
                    # (None, None, None)
                    for triple in self.spo:
                        triples_list.append(triple)
        return triples_list

    def query(self, clauses):
        bindings = None
        for clause in clauses:
            bpos = {}
            qc = []
            for pos, x in enumerate(clause):
                if x.startswith('?'):
                    qc.append(None)
                    bpos[x[
                         1:]] = pos
                else:
                    qc.append(x)
            rows = list(self.triples(qc[0], qc[1], qc[2]))
            if bindings == None:
                bindings = []
                for row in rows:
                    binding = {}
                    for var, pos in bpos.items():
                        binding[var] = row[pos]
                    bindings.append(binding)
            else:
                newb = []
                for binding in bindings:
                    for row in rows:
                        validmatch = True
                        tempbinding = binding.copy()
                        for var, pos in bpos.items():
                            if var in tempbinding:
                                if tempbinding[var] != row[pos]:
                                    validmatch = False
                            else:
                                tempbinding[var] = row[
                                    pos]
                        if validmatch:
                            newb.append(tempbinding)
                bindings = newb
        return bindings

    def print_all_triples(self):
        t = self.triples(None, None, None)
        self.print_triples(t)

    @staticmethod
    def print_triples(lst):
        if not lst:
            print(lst)
        for triple in lst:
            print('({}, {}, {})'.format(triple[0], triple[1], triple[2]))
