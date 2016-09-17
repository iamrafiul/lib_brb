import json
# import ripdb

# json_data = json.dumps({
#     "x7": {
#         "antecedent_id": "12345",
#         "ref_val": [
#             "800",
#             "1234"
#         ]
#     },
#     "x8": {
#         "antecedent_id": "34567",
#         "ref_val":  [
#             "1000",
#             "4567"
#         ]
#     }
# })


with open('data.json') as file_data:
    # import pdb; pdb.set_trace()
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

    def __init__(self, obj_list):
        self.obj_list = obj_list
        self.con_ref_values = list()
        # self.values = [[None for _ in range(3)] for _ in range(3)]
        self.intermediate_ref_val = 0

    def create_rule_base(self):
        cons_ref_val_1 = 0
        cons_ref_val_2 = 0
        cons_ref_val_3 = 0
        for each in obj_list:
            # import pdb; pdb.set_trace()
            if each.name != 'x8':
                cons_ref_val_1 += float(float(each.attribute_weight) * float(each.ref_val[0]))
                cons_ref_val_3 += float(float(each.attribute_weight) * float(each.ref_val[2]))

        cons_ref_val_2 += (cons_ref_val_1 + cons_ref_val_3) / 2

        self.con_ref_values.append(cons_ref_val_3)
        self.con_ref_values.append(cons_ref_val_2)
        self.con_ref_values.append(cons_ref_val_1)

        values = [[0.00 for _ in range(3)] for _ in range(9)]

        for each in values:
            print each

        a = 0

        count = 0

        for i in range(len(obj_list[2].ref_val)):
            for j in range(len(obj_list[1].ref_val)):
                self.intermediate_ref_val = a + float(
                        (float(obj_list[2].attribute_weight) * float(obj_list[2].ref_val[i])) +
                        (float(obj_list[1].attribute_weight) * float(obj_list[1].ref_val[j]))
                )
                is_continue = False
                for q in range(len(self.con_ref_values)):
                    if self.intermediate_ref_val == self.con_ref_values[q]:
                        # print "values before inserting 1.00: {}".format(values[i])
                        values[count][q] = 1.0
                        count += 1
                        print count
                        # print "Calculated values before continue: {}".format(values[i])
                        is_continue = True
                if is_continue:
                    continue

                for m in range(0, len(self.con_ref_values)-2):
                    if (self.con_ref_values[m] > self.intermediate_ref_val) and (self.intermediate_ref_val > self.con_ref_values[m+1]):
                        print "intermediate_ref_val: {}".format(self.intermediate_ref_val)

                        val_1 = float((self.con_ref_values[m] - self.intermediate_ref_val) / (self.con_ref_values[m] - self.con_ref_values[m+1]))
                        values[count][m+1] = val_1
                        val_2 = float(1 - values[i+j][m+1])
                        values[count][m] = val_2
                        # count += 1
                        # print count
                print "Calculated values: {}".format(values[count])
            count += 1
            print count

        return values




# j = json.loads(json_data)

print "JSON data type: {}".format(type(data))

# for key in data:
#     for val in data[key]:
#         print data[key][val]

obj_list = list()

for each in data:
    obj = Data(**data[each])
    obj.name = str(each)
    obj_list.append(obj)
    # print u.ref_val


# import pdb
#
# pdb.set_trace()


rule_base = RuleBase(obj_list)
ref_val_list = rule_base.create_rule_base()

print "\n\n\n\n\n"
for each in ref_val_list:
    print each

