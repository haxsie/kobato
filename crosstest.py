# !/user/bin/env python
# coding: utf - 8

import sys
reload(sys)
sys.setdefaultencoding("utf - 8")
import math

def cross_test(o, a, b, c):
    '''Cross test in 2 way'''
    return cross_test_eval(o, a, b, c) and cross_test_eval(b, c, o, a)

def makeVector(pointFrom, pointTo):
    return (pointTo[0] - pointFrom[0], pointTo[1] - pointFrom[1])

def cross_product_2d(edge1, edge2):
    return edge1[0]*edge2[1] - edge1[1]*edge2[0]
    
def edge_len(edge):
    return math.hypot(edge[0], edge[1])

def cross_test_eval(o, a, b, c):
    '''Cross test for line o to a, and line b to c.'''
    # (Points o, a, b, c are in grid coordinate.)
    # .a  .c
    # .b  .o
    
    if o == b or o == c or a == b or a == c:
        return True
    
    oa = makeVector(o, a)
    #
    ob = makeVector(o, b)
    oc = makeVector(o, c)
    # 
    ab = makeVector(a, b)
    ac = makeVector(a, c)
    #
    cb = makeVector(c, b)
    bc = makeVector(b, c)
    #
    crossProduct1 = cross_product_2d(oa, ob)
    crossProduct2 = cross_product_2d(oa, oc)
    #
    relationOfCP = crossProduct1 * crossProduct2
    if relationOfCP == 0:
        # If in "tri lm-n", edge_len(lm) equals edge_len(nl) + edge_len(nm)
        # mweans points l,m,n are on same single edge.
        # So, here denies following pattern,
        # edge ob = oab, ob = ocb, oc = obc, oc = oac.
        if not(
            # tri ob-a
               edge_len(ob) == edge_len(oa) + edge_len(ab) \
            # tri ob-c
            or edge_len(ob) == edge_len(oc) + edge_len(cb) \
            # tri oc-b
            or edge_len(oc) == edge_len(ob) + edge_len(bc) \
            # tri oc-a
            or edge_len(oc) == edge_len(oa) + edge_len(ac)):
                return True
    elif relationOfCP < 0:
        return True
    else:
        return False