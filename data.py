class Data(object):

    def __init__(self, antecedent_id, antecedent_name,
                 attribute_weight, ref_val, ref_title,
                 consequent_values, crisp_val, parent,
                 input_val):
        self.name = ""
        self.antecedent_id = antecedent_id
        self.antecedent_name = antecedent_name
        self.attribute_weight = attribute_weight
        self.ref_title = ref_title
        self.ref_val = ref_val
        self.consequent_values = consequent_values
        self.crisp_val = crisp_val
        self.parent = parent
        self.input_val = input_val
