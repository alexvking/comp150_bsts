# BSTTree.py
# COMP 150
# Created by Alex King
# 3/31/2017

# Basic binary search tree implementation to be used by optimal construction
# algorithms

class BSTTree:
    def __init__(self, value):
        """
        Creates a new tree node with the specified value. 

        INVARIANT: If value = None, then the tree will behave as an empty Node
        (this allows `insert` and other functions to be member functions of 
        the class)
        """
        self.value = value
        self.left = None
        self.right = None

    def insert(self, value):
        """
        Inserts specified value into tree
        """
        if self.value is None:
            self.value = value
        else:
            if value < self.value:
                # Recursion on child isn't possible unless it's initialized
                if self.left is None:
                    self.left = BSTTree(value)
                else:
                    self.left.insert(value)
            elif value > self.value:
                if self.right is None:
                    self.right = BSTTree(value)
                else:
                    self.right.insert(value)
            elif value == self.value:
                return

    def find(self, value):
        """
        Returns whether the specified value exists in the tree
        """
        if self.value is None:
            return False
        else:
            if value < self.value:
                if self.left is None:
                    return False
                else:
                    return self.left.find(value)
            elif value > self.value:
                if self.right is None:
                    return False
                else:
                    return self.right.find(value)
            elif value == self.value:
                return True

    def inorder_traversal(self, func):
        """
        Performs specified function for each node in tree in order
        """
        if self.value is None:
            return
        if self.left:
            self.left.inorder_traversal(func)
        func(self.value)
        if self.right:
            self.right.inorder_traversal(func)

    def preorder_traversal(self, func):
        """
        Performs specified function for each node in tree in pre order
        """
        if self.value is None:
            return
        func(self.value)
        if self.left:
            self.left.preorder_traversal(func)
        if self.right:
            self.right.preorder_traversal(func)

    def __str__(self, depth=0):
        """
        Prints binary search tree structure in rotated fashion
        Algorithm taken from http://krenzel.org/articles/printing-trees
        """
        ret = ""

        if self.right != None:
            ret += self.right.__str__(depth + 1)

        ret += "\n" + ("    "*depth) + str(self.value)

        if self.left != None:
            ret += self.left.__str__(depth + 1)

        return ret