import json
from rules import Rules
from data import Data

with open('data.json') as file_data:
    data = json.load(file_data)


class RuleBase(object):

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
                rules = Rules()
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

    def input_transformation(self):
        for each in obj_list:
            print "Before input transformation: {}".format(each.transformed_val)
            user_input = float(each.input_val)

            if user_input > float(each.ref_val[0]):
                user_input = float(each.ref_val[0])
            elif user_input < float(each.ref_val[len(each.ref_val) - 1]):
                user_input = float(each.ref_val[len(each.ref_val) - 1])
            flag = False
            for i in range(len(each.ref_val)):
                if user_input == float(each.ref_val[i]):
                    each.transformed_val[i] = 1
                    flag = True
                    break
            if not flag:
                for j in range(len(each.ref_val) - 1):
                    if (float(each.ref_val[j]) > user_input) and (user_input > float(each.ref_val[j+1])):
                        val_1 = (
                            (float(each.ref_val[j]) - user_input) / (float(each.ref_val[j]) - float(each.ref_val[j+1]))
                        )
                        each.transformed_val[j + 1] = str(val_1)
                        val_2 = 1 - val_1
                        each.transformed_val[j] = str(val_2)
            print "After input transformation: {}".format(each.transformed_val)

obj_list = list()

for each in data:
    obj = Data(**data[each])
    obj.name = str(each)
    obj_list.append(obj)

rule_base = RuleBase(obj_list)
ref_val_list = rule_base.create_rule_base()

rule_base.input_transformation()

for each in ref_val_list:
    print "{} {} {} {} {}".format(each.antecedent_1, each.antecedent_1_ref_title, each.antecedent_2, each.antecedent_2_ref_title, each.consequence_val)
