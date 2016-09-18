class Rules(object):
    def __init__(self):
        self.rule_weight = 1
        self.antecedent_1 = ""
        self.antecedent_1_ref_title = ""
        self.antecedent_2 = ""
        self.antecedent_2_ref_title = ""
        self.parent = ""
        self.consequence_val = list()
        self.matching_degree = None
        self.activation_weight = None

