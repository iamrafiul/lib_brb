
import json
import math
from rules import Rules
from data import Data

with open('data.json') as file_data:
    data = json.load(file_data)


class RuleBase(object):

    def __init__(self, object_list):
        self.obj_list = object_list
        self.con_ref_values = list()
        self.intermediate_ref_val = 0
        self.rule_row_list = list()

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
                        self.rule_row_list.append(rules)

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
                self.rule_row_list.append(rules)
        return self.rule_row_list

    def input_transformation(self):
        for each in obj_list:
            if each.name != 'x8':
                # print "Before input transformation: {}".format(each.transformed_val)
                try:
                    user_input = float(each.input_val)
                except:
                    user_input = 0

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
                # print "After input transformation: {}".format(each.transformed_val)

    def activation_weight(self):
        matching_degree = list()
        for i in range(len(obj_list[2].ref_val)):
            for j in range(len(obj_list[1].ref_val)):
                degree = float(
                    pow(float(obj_list[2].transformed_val[i]), float(obj_list[2].attribute_weight)) *
                    pow(float(obj_list[1].transformed_val[j]), float(obj_list[1].attribute_weight))
                )
                matching_degree.append(degree)

        sum = 0.0
        for k in range(len(self.rule_row_list)):
            current_rule = self.rule_row_list[k]
            current_rule.matching_degree = matching_degree[k]
            sum += float(current_rule.rule_weight) * float(current_rule.matching_degree)

        for p in range(len(self.rule_row_list)):
            current_rule = self.rule_row_list[p]
            activation_weight = float(
                (float(current_rule.rule_weight) * float(current_rule.matching_degree)) /
                sum
            )
            current_rule.activation_weight = activation_weight

    def belief_update(self):
        tao = [0 for _ in range(3)]

        for i in range(len(obj_list)):
            if obj_list[i].name != 'x8':
                try:
                    input_val = float(obj_list[i].input_val)
                except:
                    input_val = 0
                if input_val != 0:
                    tao[i] = 1
        total = 0

        for j in range(len(obj_list)):
            if obj_list[j].name != 'x8':
                summation = sum([float(each) for each in obj_list[j].transformed_val])
                total += summation

        update_value = total / 2

        for each in self.rule_row_list:
            new_val_list = []
            for row in each.consequence_val:
                # import pdb; pdb.set_trace()
                for key, val in row.iteritems():
                    print "Before: {} {}".format(key, val)
                    new_val = float(val) * update_value
                    new_val_list.append({str(key): new_val})
                    print "After: {} {}".format(key, new_val)
            each.consequence_val = new_val_list

obj_list = list()

for each in data:
    obj = Data(**data[each])
    obj.name = str(each)
    obj_list.append(obj)

rule_base = RuleBase(obj_list)
ref_val_list = rule_base.create_rule_base()

rule_base.input_transformation()
rule_base.activation_weight()
rule_base.belief_update()

# for each in ref_val_list:
#     print "{} {} {} {} {}".format(each.antecedent_1, each.antecedent_1_ref_title, each.antecedent_2, each.antecedent_2_ref_title, each.consequence_val)

for each in rule_base.rule_row_list:
    print each.__dict__
