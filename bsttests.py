# bsttests.py
# COMP 150
# Created by Alex King
# 3/31/2017

# Testing the functionality, correctness, and general runtime of BSTTree

from BSTTree import BSTTree
from random import randint
import time
import sys

def print_value(x):
    sys.stdout.write(str(x) + "\n")

myTree = BSTTree(None)
values = []
for i in range(30):
    random = randint(0, 500)
    values.append(random)
    myTree.insert(random)

print myTree


# Ensure insertion works as expected
for v in values:
    if not myTree.find(v):
        print "Inserted value %d not found in tree!" % v
        exit(1)

myTree.preorder_traversal((lambda x : print_value(x)))
exit(1)

values = []
myTree.inorder_traversal((lambda x : values.append(x)))

# Ensure inorder traversal works as expected
for i in range(1, len(values)):
    if values[i - 1] >= values[i]:
        print "Inorder traversal led to nodes appearing incorrectly ordered!"
        exit(1)

# Works on strings, too! Should work for any other datatype we want as long
# as we overload all comparison functions

myWordTree = BSTTree(None)
myWordTree.insert("aad")
myWordTree.insert("aab")
myWordTree.insert("aaa")
myWordTree.insert("aaaf")

myWordTree.inorder_traversal((lambda x : print_value(x)))

##### Check runtime of large tree #####

def insert_random_values(n, tree):
    values = []
    for i in range(n):
        random = randint(0, 1000000000)
        values.append(random)
        tree.insert(random)
    return values

def read_random_values(tree, values):
    for v in values:
        tree.find(v)

bigTree = BSTTree(None)
start = time.time()
values = insert_random_values(200000, bigTree)
end = time.time()
print "Time to insert:", end-start
start = time.time()
read_random_values(bigTree, values)
end = time.time()
print "Time to read:", end-start