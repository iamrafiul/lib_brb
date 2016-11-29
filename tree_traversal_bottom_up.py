
import json
from data import Data
from manipulate_data_new import RuleBase

# Read data from file
with open('temp_data.json') as file_data:
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
                                                    [str(each.antecedent_id) for each in visiting])
        # import pdb; pdb.set_trace()
        # brb_calculation = RuleBase()
        rule_base = RuleBase(visiting, parent)
        rule_base.create_rule_base()
        rule_base.input_transformation()
        rule_base.activation_weight()
        rule_base.belief_update()
        consequence_val = rule_base.aggregate_rule()
        result.insert(count, consequence_val)
        parent.consequence_val = consequence_val

        print "Calculated consequence values for {} are: {}".format(parent.antecedent_id, consequence_val)


        print "\nAll the current nodes have same parent \"{}\" so the tree traversal is done and the ultimate output is: {}".format(parent.antecedent_id, parent.antecedent_id)
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
        rule_base.create_rule_base()
        rule_base.input_transformation()
        rule_base.activation_weight()
        rule_base.belief_update()
        consequence_val = rule_base.aggregate_rule()
        parent.consequence_val = consequence_val
        result.insert(count, consequence_val)

        print "Calculated consequence values for {} are: {}".format(parent.antecedent_id, consequence_val)


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


for each in result:
    print each