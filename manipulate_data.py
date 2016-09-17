import json

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


class User(object):
    def __init__(self, antecedent_id, ref_val):
        self.antecedent_id = antecedent_id
        self.ref_val = ref_val

# j = json.loads(json_data)

print "JSON data type: {}".format(type(data))

# for key in data:
#     for val in data[key]:
#         print data[key][val]

for each in data:
    u = User(**data[each])
    print u.ref_val
