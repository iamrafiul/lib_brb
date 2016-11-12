
import json
import math
from rules import Rules
from data import Data

with open('single_tree.json') as file_data:
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
                print "Value before input transformation: {}".format(each.transformed_val)
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
                print "Value after input transformation: {}".format(each.transformed_val)

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

        for each in ref_val_list:
            print "{} {} {} {} {} {} {}".format(each.antecedent_1, each.antecedent_1_ref_title, each.antecedent_2,
                                             each.antecedent_2_ref_title, each.rule_weight, each.consequence_val, each.activation_weight)

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
                    # print "Before: {} {}".format(key, val)
                    new_val = float(val) * update_value
                    new_val_list.append({str(key): new_val})
                    # print "After: {} {}".format(key, new_val)
            each.consequence_val = new_val_list

        for each in self.rule_row_list:
            print "{} {} {} {} {} {} {}".format(each.antecedent_1, each.antecedent_1_ref_title, each.antecedent_2,
                                             each.antecedent_2_ref_title, each.rule_weight, each.consequence_val, each.activation_weight)

    def aggregate_rule(self):

        # Create 2D array for consequent values from rule base
        consequent_array = [[0 for _ in range(3)] for _ in range(9)]
        for i in range(len(self.rule_row_list)):
            row = self.rule_row_list[i]
            for j in range(len(row.consequence_val)):
                values = row.consequence_val[j]
                # import pdb; pdb.set_trace()
                if values.has_key('High'):
                    consequent_array[i][0] = float(values['High'])
                if values.has_key('Medium'):
                    consequent_array[i][1] = float(values['Medium'])
                if values.has_key('Low'):
                    consequent_array[i][2] = float(values['Low'])

        # Calculate mn from the consequent array and save in a 2D array(named mn here)
        mn = [[0 for _ in range(9)] for _ in range(3)]

        for i in range(len(self.rule_row_list)):
            for each in self.rule_row_list[i].consequence_val:
                # import pdb;
                # pdb.set_trace()
                for key, val in each.iteritems():
                    if key == 'High':
                        mn[0][i] = float(
                            float(self.rule_row_list[i].activation_weight) *
                            float(val)
                        )
                    elif key == 'Medium':
                        mn[1][i] = float(
                            float(self.rule_row_list[i].activation_weight) *
                            float(val)
                        )
                    elif key == 'Low':
                        mn[2][i] = float(
                            float(self.rule_row_list[i].activation_weight) *
                            float(val)
                        )

        # Calculate md from the consequent array and save in a 1Ds array(named md here)
        md = [0 for _ in range(len(self.rule_row_list))]

        for j in range(len(consequent_array)):
            total = 0
            for k in range(len(consequent_array[j])):
                total += consequent_array[j][k]

            md[j] = 1 - (float(self.rule_row_list[j].activation_weight) * total)

        # Calculate d in a 1D array in several steps

        # Step 1: calculate total rowsum
        rowsum = [1 for _ in range(3)]

        for x in range(len(rowsum)):
            for y in range(len(self.rule_row_list)):
                rowsum[x] *= (mn[x][y] + md[y])

        total_rowsum = sum(rowsum)

        # Step 2: Calculate mh and save in a 1D array
        mh = 1

        for i in range(len(md)):
          mh *= md[i]

        # Step 3: Calculate kn, kn1, m(1D array), mhn and aggregated_consequence_val
        kn = total_rowsum - (2 * mh)
        kn1 = 1 / kn

        m = [0 for _ in range(3)]

        for j in range(3):
            m[j] = kn1 * (rowsum[j] - mh)

        mhn = kn1 * mh

        aggregated_consequence_val = [0 for k in range(3)]
        for k in range(len(rowsum)):
            aggregated_consequence_val[k] = m[k] / (1 - mhn)

        print aggregated_consequence_val


obj_list = list()

for each in data:
    obj = Data(**data[each])
    obj.name = str(each)
    obj_list.append(obj)

print "Initial Data:"
print "Antecedent ID    Name     Attribute Weight    Reference Titles    Reference Values"
for row in obj_list:
    print "{}   {}  {}  {}  {}".format(row.antecedent_id, row.antecedent_name, row.attribute_weight, row.ref_val, row.ref_title)

rule_base = RuleBase(obj_list)
ref_val_list = rule_base.create_rule_base()

print "\n\n"
print "Rule Base: "
for each in ref_val_list:
    print "{} {} {} {} {} {}".format(each.antecedent_1, each.antecedent_1_ref_title, each.antecedent_2, each.antecedent_2_ref_title, each.rule_weight, each.consequence_val)

print "\n\n"
print "Input Transformation: "

rule_base.input_transformation()

print "\n\n"
print "Rule base with activation weight"

rule_base.activation_weight()

print "\n\n"
print "Belief Update"
rule_base.belief_update()

print "\n\n"
print "Aggregated rule for X8:"
rule_base.aggregate_rule()
