a = [[1, 2, 3],[1, 2],[1, 2, 3],[1, 2, 3],[1, 2, 3]]

# r = [[]]
# for each in a:
#     r = [i + [y] for y in each for i in r]
#     for each in r:
#         if len(each) == len(a):
#             print each
#             import pdb; pdb.set_trace()
#             each.sort()
#         print each
#     print len(r)


# def product(a, repeat=1):
#     count = 0
#     # product('ABCD', 'xy') --> Ax Ay Bx By Cx Cy Dx Dy
#     # product(range(2), repeat=3) --> 000 001 010 011 100 101 110 111
#     pools = [tuple(pool) for pool in a] * repeat
#     result = [[]]
#     for pool in pools:
#         result = [x+[y] for x in result for y in pool]
#     for prod in result:
#         if len(prod) == len(a):
#         # import pdb; pdb.set_trace()
#             print prod
#         count+=1
#     print count
# product(a, 1)

for each in range(4):
    for i in range(3):
        print each, i

