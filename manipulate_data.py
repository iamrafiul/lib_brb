import json

with open('data.json') as file_data:
    data = json.load(file_data)


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


class RuleBase(object):

    class Rule(object):
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

    def __init__(self, object_list):
        self.obj_list = object_list
        self.con_ref_values = list()
        self.intermediate_ref_val = 0

    def create_rule_base(self):
        cons_ref_val_1 = 0
        cons_ref_val_2 = 0
        cons_ref_val_3 = 0
        for each in obj_list:
            if each.name != 'x8':
                cons_ref_val_1 += float(
                    float(each.attribute_weight) * float(each.ref_val[0])
                )
                cons_ref_val_3 += float(
                    float(each.attribute_weight) * float(each.ref_val[2])
                )
        cons_ref_val_2 += (cons_ref_val_1 + cons_ref_val_3) / 2

        self.con_ref_values.append(cons_ref_val_1)
        self.con_ref_values.append(cons_ref_val_2)
        self.con_ref_values.append(cons_ref_val_3)

        a = 0
        count = 0

        rule_row_list = list()

        for i in range(len(obj_list[2].ref_val)):
            for j in range(len(obj_list[1].ref_val)):
                rules = self.Rule()
                rules.antecedent_1 = obj_list[2].antecedent_id
                rules.antecedent_2 = obj_list[1].antecedent_id
                rules.parent = obj_list[2].parent

                self.intermediate_ref_val = a + float(
                        (float(obj_list[2].attribute_weight) * float(obj_list[2].ref_val[i])) +
                        (float(obj_list[1].attribute_weight) * float(obj_list[1].ref_val[j]))
                )
                is_continue = False
                for q in range(len(self.con_ref_values)):
                    if self.intermediate_ref_val == self.con_ref_values[q]:
                        rules.antecedent_1_ref_title = obj_list[2].ref_title[i]
                        rules.antecedent_2_ref_title = obj_list[1].ref_title[j]
                        rules.consequence_val.append({obj_list[2].ref_title[q]: 1.0})
                        rule_row_list.append(rules)

                        count += 1
                        is_continue = True

                if is_continue:
                    continue
                else:
                    for m in range(0, len(self.con_ref_values)-1):
                        if (self.con_ref_values[m] > self.intermediate_ref_val) and \
                                (self.intermediate_ref_val > self.con_ref_values[m+1]):
                            val_1 = float(
                                (self.con_ref_values[m] - self.intermediate_ref_val) /
                                (self.con_ref_values[m] - self.con_ref_values[m+1])
                            )
                            val_2 = float(1 - val_1)

                            rules.antecedent_1_ref_title = obj_list[2].ref_title[i]
                            rules.antecedent_2_ref_title = obj_list[1].ref_title[j]
                            rules.consequence_val.append({obj_list[2].ref_title[m+1]: val_1})
                            rules.consequence_val.append({obj_list[2].ref_title[m]: val_2})

                            count += 1
                rule_row_list.append(rules)
        return rule_row_list

obj_list = list()

for each in data:
    obj = Data(**data[each])
    obj.name = str(each)
    obj_list.append(obj)

rule_base = RuleBase(obj_list)
ref_val_list = rule_base.create_rule_base()

for each in ref_val_list:
    print "{} {} {} {} {}".format(each.antecedent_1, each.antecedent_1_ref_title, each.antecedent_2, each.antecedent_2_ref_title, each.consequence_val)
