
import json
from data import Data

# with open('test_tree_traversal.json') as file_data:
with open('temp_data.json') as file_data:
    data = json.load(file_data)

obj_list = list()

for each in data:
    obj = Data(**data[each])
    obj.name = str(each)
    obj_list.append(obj)

obj_list.sort(key=lambda x: x.is_input == "true", reverse=True)
print "Initial nodes: {}".format([str(each.antecedent_id) for each in obj_list])



visited = list()

i = 0

count = 1

subtree = 1

while(len(obj_list) > 0):
    print "\n\nIteration: {}\n".format(count)
    count += 1

    parent = obj_list[i].parent
    visiting = list()
    for j in range(i + 1, len(obj_list)):
        if obj_list[i].parent == obj_list[j].parent:
            visiting.append(obj_list[j])
    visiting.append(obj_list[i])

    if len(visiting) == len(obj_list):
        print "\nAll the current nodes have same parent \"{}\" so the tree traversal is done and the ultimate output is: {}".format(parent, parent)
        break

    print "For {}, parent is: {}".format(str(obj_list[i].antecedent_id), parent)

    isAllInput = True
    for each in visiting:
        if each.is_input != 'true':
            isAllInput = False

    if not isAllInput:
        i += 1
        print "Current Nodes: {}".format([str(each.antecedent_id) for each in visiting])
        print "All the children for parent {} is not calculated yet".format(parent)
        obj_list.sort(key=lambda x: x.is_input == "true", reverse=True)
        continue
    else:
        print "{} children found for parent {}. They are: {}".format(len(visiting), parent, [str(each.antecedent_id) for each in visiting])

        for each in visiting:
            visited.append(each)
        obj_list = [each for each in obj_list if each not in visited]

        current = list()
        for each in obj_list:
            if each.antecedent_id == parent:
                current = each
                each.is_input = 'true'
                i = 0
        print "Remaining nodes for traversal: {}".format([str(each.antecedent_id) for each in obj_list])

        print "\nIn iteration {}, {} is calculated and now it's an input node. We've calculated {} subtrees so far.".format(count-1, str(current.antecedent_id), subtree)
        subtree += 1
        obj_list.sort(key=lambda x: x.is_input == "true", reverse=True)

