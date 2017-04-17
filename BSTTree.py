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

    def find(self, value, depth):
        """
        Returns whether the specified value exists in the tree
        """
        if self.value is None:
            return (False, depth)
        else:
            if value < self.value:
                if self.left is None:
                    return (False, depth)
                else:
                    return self.left.find(value, depth + 1)
            elif value > self.value:
                if self.right is None:
                    return (False, depth)
                else:
                    return self.right.find(value, depth + 1)
            elif value == self.value:
                return (True, depth)

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

    def inorder_traversal_iter(self, func):
        """
        Performs specified function for each node in tree in order
        Iterative algorithm taken from http://www.geeksforgeeks.org/inorder-tree-traversal-without-recursion/
        """
        # Set current to root of binary tree
        current = self 
        s = []
        done = 0
         
        while(not done):
            if current is not None:
                s.append(current)
                current = current.left 
            else:
                if(len(s) >0 ):
                    current = s.pop()
                    func(current.value),
                    current = current.right 
                else:
                    done = 1

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