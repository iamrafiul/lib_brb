# @Author: mdrhri-6
# @Date:   2017-01-17T20:51:23+01:00
# @Last modified by:   mdrhri-6
# @Last modified time: 2017-03-23T10:19:17+01:00


import hashlib
import time
import json
from collections import OrderedDict

from flask import Flask, jsonify, request
from manipulate_data_new import RuleBase
from tree_traversal_bottom_up import TreeTraversalBottomUp
from data import Data

app = Flask(__name__)

create_rule_base = list()
input_transformatiom = list()

'''
    Run tree traversal on a JSON file
'''

# def tree_traversal():
#     import json
#
#     from manipulate_data_new import RuleBase
#     from data import Data
#
#     # Read data from file
#     # with open('temp_data.json') as file_data:
#     # with open('2nd_order_tree.json') as file_data:
#     with open('single_tree.json') as file_data:
#         data = json.load(file_data)
#
#     obj_list = list()
#
#     global create_rule_base, input_transformatiom
#
#
#     # Save each node data as an object in a list
#     for each in data:
#         obj = Data(**data[each])
#         obj.name = str(each)
#         obj_list.append(obj)
#
#     # Sort the obj_list based on is_input is true
#     obj_list.sort(key=lambda x: x.is_input == "true", reverse=True)
#     print "Initial nodes: {}".format([str(each.antecedent_id) for each in obj_list])
#
#     visited = list()
#
#     i = 0
#
#     count = 1
#
#     subtree = 1
#
#     result = list()
#
#     rule_list = list()
#
#     # While you have an object in obj_list
#     while len(obj_list):
#         print "\n\nIteration: {}\n".format(count)
#         count += 1
#
#         # Get parent of the current node.
#         parent = None
#         # parent_id =
#         for each in obj_list:
#             if each.name == obj_list[i].parent:
#                 parent = each
#                 break
#
#         visiting = list()
#
#         # Find if there is any other node which has the same parent
#         for j in range(i + 1, len(obj_list)):
#             if obj_list[i].parent == obj_list[j].parent:
#                 visiting.append(obj_list[j])
#         visiting.append(obj_list[i])  # Add the current node in the list
#
#         # Check if all the siblings has is_input true or not.
#         isAllInput = True
#         for each in visiting:
#             if each.is_input != 'true':
#                 isAllInput = False
#         #
#         # import pdb; pdb.set_trace()
#         if len(visiting) == len(obj_list):
#             # Compute the BRB sub-tree for the nodes in visiting.
#             print "Computing value of {} for {}".format(parent.antecedent_id,
#                                                         [str(each.antecedent_id) for each in visiting if
#                                                          each.antecedent_id != parent.antecedent_id])
#             # import pdb; pdb.set_trace()
#             # brb_calculation = RuleBase()
#             rule_base = RuleBase(visiting, parent)
#             row_list = rule_base.create_rule_base()
#
#             return row_list, parent, visiting
#
#             create_rule_base.insert(0, row_list)
#             create_rule_base.insert(1, parent)
#             create_rule_base.insert(2, visiting)
#
#             # return create_rule_base
#             # import pdb; pdb.set_trace()
#             rule_base.input_transformation()
#             rule_base.activation_weight()
#             rule_base.belief_update()
#             consequence_val = rule_base.aggregate_rule()
#             result.insert(count, consequence_val)
#             parent.consequence_val = consequence_val
#
#             crisp_val = 0.0
#             for i in range(len(parent.ref_val)):
#                 crisp_val += float(parent.ref_val[i]) * float(consequence_val[i])
#
#             parent.input_val = str(crisp_val)
#
#             # import pdb; pdb.set_trace()
#
#             print "Calculated consequence values for {} are: {}".format(parent.antecedent_id, consequence_val)
#
#             print "\nAll the current nodes have same parent \"{}\" so the tree traversal is done and the ultimate output is: {}".format(
#                 parent.antecedent_id, parent.antecedent_id)
#
#             # return rule_list
#             break
#
#         print "For {}, parent is: {}".format(str(obj_list[i].antecedent_id), parent.antecedent_id)
#
#         # if not all the siblings has same parent, continue to the next node of obj_list
#         if not isAllInput:
#             i += 1
#             print "Current Nodes: {}".format([str(each.antecedent_id) for each in visiting])
#             print "All the children for parent {} is not calculated yet".format(parent)
#             obj_list.sort(key=lambda x: x.is_input == "true", reverse=True)
#             continue
#         else:
#             # Compute the BRB sub-tree for the nodes in visiting.
#             print "Computing value of {} for {}".format(parent.antecedent_id,
#                                                         [str(each.antecedent_id) for each in visiting])
#             # import pdb; pdb.set_trace()
#             # brb_calculation = RuleBase()
#             rule_base = RuleBase(visiting, parent)
#             rule_base.create_rule_base()
#             rule_base.input_transformation()
#             rule_base.activation_weight()
#             rule_base.belief_update()
#             consequence_val = rule_base.aggregate_rule()
#             parent.consequence_val = consequence_val
#             result.insert(count, consequence_val)
#
#             crisp_val = 0.0
#             for i in range(len(parent.ref_val)):
#                 crisp_val += float(parent.ref_val[i]) * float(consequence_val[i])
#
#             parent.input_val = str(crisp_val)
#
#             # import pdb; pdb.set_trace()
#
#             print "Calculated consequence values for {} are: {}".format(parent.antecedent_id, consequence_val)
#
#             # Remove the visited nodes from obj_list
#             for each in visiting:
#                 visited.append(each)
#             obj_list = [each for each in obj_list if each not in visited]
#
#             # Make the current nodes is_input true
#             current = list()
#             for each in obj_list:
#                 if each == parent:
#                     current = each
#                     each.is_input = 'true'
#                     i = 0
#             print "Remaining nodes for traversal: {}".format([str(each.antecedent_id) for each in obj_list])
#
#             print "\nIn iteration {}, {} is calculated and now it's an input node. We've calculated {} subtrees so far.".format(
#                 count - 1, str(current.antecedent_id), subtree)
#             subtree += 1
#             obj_list.sort(key=lambda x: x.is_input == "true", reverse=True)
#
#     for each in result:
#         print each
#
#     # return rule_list

def create_hash():
    hash = hashlib.sha1()
    hash.update(str(time.time()))
    return hash.hexdigest()

rule_base = ""

@app.route('/')
def home():
    return jsonify('Welcome')

@app.route('/api/v1/initiate_brb/', methods=['GET', 'POST'])
def initiate_brb():
    response_dict = dict()

    if request.method == 'GET':
        response_dict['response'] = 200
        response_dict['access_key'] = ''
        response_dict['message'] = 'No data found. Please send a POST request with JSON data.'
        return jsonify(response_dict)

    if request.method == 'POST':
        data = request.get_json()
        print data

        access_key = create_hash()
        file_name = '' + str(access_key) + '.json'

        write_file = open(file_name, 'w')
        json.dump(data, write_file)
        write_file.close()
        # import pdb; pdb.set_trace()
        global rule_base

        try:
            with open(file_name) as file_data:
                data = json.load(file_data, object_pairs_hook=OrderedDict)

            obj_list = list()
            parent = ""

            for each in data:
                obj = Data(**data[each])
                obj.name = str(each)
                # if obj.parent != 'x8':
                #     parent = obj
                # else:
                obj_list.append(obj)


            tree_traversal = TreeTraversalBottomUp()
            # import pdb; pdb.set_trace()
            # consequence_val, crisp_val = tree_traversal.traverse_tree(obj_list)
            initial_rule_base, transformed_input, activation_weight, belief_update, consequence_val, crisp_val = tree_traversal.traverse_tree(obj_list)


            # import pdb; pdb.set_trace()
            result_dict  = dict()
            result_dict["initial_rule_base"] = initial_rule_base
            result_dict["transformed_input"] = transformed_input
            result_dict["activation_weight"] = activation_weight
            result_dict["belief_update"] = belief_update
            result_dict["consequence_val"] = consequence_val
            result_dict["crisp_val"] = crisp_val

            # import pdb; pdb.set_trace()

            with open('result/' + file_name, 'w') as fp:
                json.dump(result_dict, fp)

            fp.close()

            # rule_base = RuleBase(obj_list, parent)
            response_dict['response'] = 200
            response_dict['access_key'] = access_key
            response_dict['message'] = 'Initiated BRB algorithm'
            return jsonify(response_dict)

        except:
            response_dict['response'] = 400
            response_dict['access_key'] = ''
            response_dict['message'] = 'Error initiating BRB algorithm'
            return jsonify(response_dict)

@app.route('/api/v1/<access_key>/get_initial_rule_base/')
def get_initial_rule_base(access_key=None):
    if access_key is not None:
        file_path = 'result/' + access_key + '.json'
        with open(file_path) as data_file:
            data = json.load(data_file)
        data_file.close()
        return jsonify(data['initial_rule_base'])
    else:
        return jsonify({'message': 'This is not a valid URL, no access key found.', 'response': '400'})


@app.route('/api/v1/<access_key>/get_transformed_input/')
def get_transformed_input(access_key=None):
    if access_key is not None:
        file_path = 'result/' + access_key + '.json'
        with open(file_path) as data_file:
            data = json.load(data_file)
        data_file.close()
        return jsonify(data['transformed_input'])
    else:
        return jsonify({'message': 'This is not a valid URL, no access key found.', 'response': '400'})

@app.route('/api/v1/<access_key>/get_modified_rule_base/')
def get_modified_rule_base(access_key=None):
    if access_key is not None:
        file_path = 'result/' + access_key + '.json'
        with open(file_path) as data_file:
            data = json.load(data_file)
        data_file.close()
        return jsonify(data['activation_weight'])
    else:
        return jsonify({'message': 'This is not a valid URL, no access key found.', 'response': '400'})


@app.route('/api/v1/<access_key>/get_belief_update/')
def get_belief_update(access_key=None):
    if access_key is not None:
        file_path = 'result/' + access_key + '.json'
        with open(file_path) as data_file:
            data = json.load(data_file)
        data_file.close()
        return jsonify(data['belief_update'])
    else:
        return jsonify({'message': 'This is not a valid URL, no access key found.', 'response': '400'})


@app.route('/api/v1/<access_key>/get_aggregated_rule/')
def get_aggregated_rule(access_key=None):
    if access_key is not None:
        file_path = 'result/' + access_key + '.json'
        with open(file_path) as data_file:
            data = json.load(data_file)
        data_file.close()
        return jsonify(data['consequence_val'], data['crisp_val'])
    else:
        return jsonify({'message': 'This is not a valid URL, no access key found.', 'response': '400'})



if __name__ == '__main__':
    app.run(debug=True)
