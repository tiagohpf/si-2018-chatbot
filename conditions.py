# DT determinant, My
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


class Condition:
    def __init__(self, statements=[]):
        self.statements = statements

    def set_statements(self, statements):
        self.statements = statements

    def get_statements(self):
        return self.statements

    @staticmethod
    def has_preposition(statements):
        for state in statements:
            if 'IN' in state:
                return True
        return False

    def dt_nn_vb_in_dt_nn(self):
        return (self.statements[0] == 'DT' or self.statements[0] == 'PRP$') \
               and self.statements[1] == 'NN' \
               and (self.statements[2] == 'VB' or self.statements[2] == 'VBZ') \
               and self.statements[3] == 'IN' \
               and self.statements[4] == 'DT' \
               and self.statements[5] == 'NN'

    def wp_vbz_dt_nn_in_dt_nn(self):
        return self.statements[0] == 'WP' \
               and self.statements[1] == 'VBZ' \
               and self.statements[2] == 'DT' \
               and self.statements[3] == 'NN' \
               and self.statements[4] == 'IN' \
               and (self.statements[5] == 'PRP$' or self.statements[5] == 'DT') \
               and self.statements[6] == 'NN'

    def wp_vbp_prp_vb_in(self):
        return self.statements[0] == 'WP' \
               and self.statements[1] == 'VBP' \
               and self.statements[2] == 'PRP' \
               and self.statements[3] == 'VB' \
               and self.statements[4] == 'IN'

    def dt_nn_vbz_dt_nn(self):
        return self.statements[0] == 'DT' \
               and self.statements[1] == 'NN' \
               and self.statements[2] == 'VBZ' \
               and self.statements[3] == 'DT' \
               and self.statements[4] == 'NN'

    def vbp_nns_vbp_dt_nn(self):
        return (self.statements[0] == 'VBP' or self.statements[0] == 'VBZ') \
               and (self.statements[1] == 'NNS' or self.statements[1] == 'NN') \
               and (self.statements[2] == 'VBP' or self.statements[2] == 'VBZ') \
               and self.statements[3] == 'DT' \
               and (self.statements[4] == 'NN' or self.statements[4] == 'JJ')

    def wrb_vb_dt_nn(self):
        return self.statements[0] == 'WRB' \
               and (self.statements[1] == 'VB' or self.statements[1] == 'VBZ') \
               and (self.statements[2] == 'DT' or self.statements[2] == 'PRP$') \
               and self.statements[3] == 'NN'

    def wrb_vb_nn(self):
        return self.statements[0] == 'WRB' \
               and (self.statements[1] == 'VB' or self.statements[1] == 'VBZ') \
               and self.statements[2] == 'NN'

    def nn_vbz_dt_nn(self, sentence):
        return self.statements[0] == 'NN' \
               and self.statements[1] == 'VBZ' \
               and (self.statements[2] == 'DT' or self.statements[2] == 'PRP$') \
               and self.statements[3] == 'NN' \
               and 'is a' not in sentence and 'is an' not in sentence

    def prp_nn_vbz_nn(self):
        return self.statements[0] == 'PRP$' \
               and self.statements[1] == 'NN' \
               and self.statements[2] == 'VBZ' \
               and (self.statements[3] == 'NN' or self.statements[3] == 'JJ')

    def nn_vbz_dt_nn_subtype(self):
        return self.statements[0] == 'NN' \
               and self.statements[1] == 'VBZ' \
               and self.statements[2] == 'DT' \
               and self.statements[3] == 'NN'

    def wp_vbz_prp_nn(self):
        return self.statements[0] == 'WP' \
               and self.statements[1] == 'VBZ' \
               and self.statements[2] == 'PRP$' \
               and (self.statements[3] == 'NN' or self.statements[3] == 'JJ')

    def nns_vbp_dt_nn(self):
        return (self.statements[0] == 'NNS'  or self.statements[0] == 'NN')\
               and self.statements[1] == 'VBP' \
               and self.statements[2] == 'DT' \
               and (self.statements[3] == 'NN' or self.statements[3] == 'JJ')

    def wp_vbz_rb(self):
        return self.statements[0] == 'WP' \
               and self.statements[1] == 'VBZ' \
               and (self.statements[2] == 'RB' or self.statements[2] == 'NN')

    def nn_vbz_jj(self):
        return self.statements[0] == 'NN' \
               and self.statements[1] == 'VBZ' \
               and (self.statements[2] == 'JJ')
