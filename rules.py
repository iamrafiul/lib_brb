class Rules(object):
    def __init__(self):
        self.rule_weight = 1
        # self.antecedent_ref_val = []
        # self.antecedent_ref_title = []
        # self.antecedent_2 = ""
        # self.antecedent_2_ref_title = ""
        self.parent = ""
        self.combinations = []
        self.consequence_val = []
        self.matching_degree = None
        self.activation_weight = None

    # def sum_of_activation_weight(self):
    #     return sum(self.rule_weight * self.matching_degree)

