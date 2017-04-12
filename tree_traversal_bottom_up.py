# @Author: mdrhri-6
# @Date:   2016-12-22T03:30:09+01:00
# @Last modified by:   mdrhri-6
# @Last modified time: 2017-02-13T15:08:06+01:00



import json

from manipulate_data_new import RuleBase
from data import Data

# Read data from file
with open('temp_data.json') as file_data:
# with open('2nd_order_tree.json') as file_data:
#with open('api/single_tree.json') as file_data:
# with open('sunonda_tree.json') as file_data:
# with open('agriculture_tree.json') as file_data:
    data = json.load(file_data)

obj_list = list()

# Save each node data as an object in a list
for each in data:
    obj = Data(**data[each])
    obj.name = str(each)
    obj_list.append(obj)

# Sort the obj_list based on is_input is true
obj_list.sort(key=lambda x: x.is_input == "true", reverse=True)
print "Initial nodes: {}".format([str(each.antecedent_id) for each in obj_list])

visited = list()

i = 0

count = 1

subtree = 1

result = list()

# While you have an object in obj_list
while len(obj_list):
    print "\n\nIteration: {}\n".format(count)
    count += 1

    # Get parent of the current node.
    parent = None
    # parent_id =
    for each in obj_list:
        if each.name == obj_list[i].parent:
            parent = each
            break

    visiting = list()

    # Find if there is any other node which has the same parent
    for j in range(i + 1, len(obj_list)):
        if obj_list[i].parent == obj_list[j].parent:
            visiting.append(obj_list[j])
    visiting.append(obj_list[i]) # Add the current node in the list

    # Check if all the siblings has is_input true or not.
    isAllInput = True
    for each in visiting:
        if each.is_input != 'true':
            isAllInput = False

    if len(visiting) == len(obj_list):
        # Compute the BRB sub-tree for the nodes in visiting.
        print "Computing value of {} for {}".format(parent.antecedent_id,
                                                    [str(each.antecedent_id) for each in visiting if each.antecedent_id != parent.antecedent_id])
        # import pdb; pdb.set_trace()
        # brb_calculation = RuleBase()
        rule_base = RuleBase(visiting, parent)
        row_list = rule_base.create_rule_base()
        rule_base.input_transformation()
        rule_base.activation_weight()
        rule_base.belief_update()
        consequence_val = rule_base.aggregate_rule()
        result.insert(count, consequence_val)
        parent.consequence_val = consequence_val

        crisp_val = 0.0
        for i in range(len(parent.ref_val)):
            crisp_val += float(parent.ref_val[i]) * float(consequence_val[i])

        parent.input_val = str(crisp_val)

        # import pdb; pdb.set_trace()

        print "Rule Row List: {}".format([each.__dict__ for each in row_list])


        print "\nAll the current nodes have same parent \"{}\" so the tree traversal is done and the ultimate output is: {}".format(parent.antecedent_id, parent.antecedent_id)

        print "Calculated consequence values for {} are: {}".format(parent.antecedent_id, consequence_val)

        print "Crisp Value: {}".format(str(crisp_val))

        break

    print "For {}, parent is: {}".format(str(obj_list[i].antecedent_id), parent.antecedent_id)

    # if not all the siblings has same parent, continue to the next node of obj_list
    if not isAllInput:
        i += 1
        print "Current Nodes: {}".format([str(each.antecedent_id) for each in visiting])
        print "All the children for parent {} is not calculated yet".format(parent)
        obj_list.sort(key=lambda x: x.is_input == "true", reverse=True)
        continue
    else:
        # Compute the BRB sub-tree for the nodes in visiting.
        print "Computing value of {} for {}".format(parent.antecedent_id, [str(each.antecedent_id) for each in visiting])
        # import pdb; pdb.set_trace()
        # brb_calculation = RuleBase()
        rule_base = RuleBase(visiting, parent)
        row_list_1 = rule_base.create_rule_base()
        rule_base.input_transformation()
        rule_base.activation_weight()
        rule_base.belief_update()
        consequence_val = rule_base.aggregate_rule()
        parent.consequence_val = consequence_val
        result.insert(count, consequence_val)

        crisp_val = 0.0
        for i in range(len(parent.ref_val)):
            crisp_val += float(parent.ref_val[i]) * float(consequence_val[i])

        parent.input_val = str(crisp_val)

        # import pdb; pdb.set_trace()

        print "Calculated consequence values for {} are: {}".format(parent.antecedent_id, consequence_val)

        print "Rule Row List: {}".format([each.__dict__ for each in row_list_1])


        # Remove the visited nodes from obj_list
        for each in visiting:
            visited.append(each)
        obj_list = [each for each in obj_list if each not in visited]

        # Make the current nodes is_input true
        current = list()
        for each in obj_list:
            if each == parent:
                current = each
                each.is_input = 'true'
                i = 0
        print "Remaining nodes for traversal: {}".format([str(each.antecedent_id) for each in obj_list])

        print "\nIn iteration {}, {} is calculated and now it's an input node. We've calculated {} subtrees so far.".format(count-1, str(current.antecedent_id), subtree)
        subtree += 1
        obj_list.sort(key=lambda x: x.is_input == "true", reverse=True)


# for each in result:
#     print each
