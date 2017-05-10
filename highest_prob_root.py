# highest_prob_root.py
# COMP 150
# Created by Alex King
# 4/26/2017

# Implementation of Knuth's "Rule 1" heuristic that does not lead to
# approximately optimal BSTs: always pick the highest probability key as the
# root

from Queue import Queue
from BSTTree import BSTTree

def find_optimal_tree_ordering(beta_list, alpha_list, beta_length, key_list):
    """
    Returns binary search tree ordered according to Rule 1 
    with given key probabilities
    (beta_list) and gap probabilities (alpha_list)
    """
    root = None

    # holds subdivisions of beta value array
    section_queue = Queue()

    section_queue.put((0, beta_length - 1, root))

    # Iteratively find the best root for each subtree
    while not section_queue.empty():
        (left_index, right_index, parent) = section_queue.get()

        if (left_index < 0 or 
            right_index >= beta_length or 
            left_index > right_index):
            continue

        if left_index == right_index:
            node = BSTTree(key_list[left_index])
            if parent is None:
                root = node
            elif left_index < parent.value:

                parent.left = node
            else:
                parent.right = node
            continue

        max_prob = 0
        best_splits = [left_index]
        for i in range(left_index, right_index + 1):
            if beta_list[i] > max_prob:
                max_prob = beta_list[i]
                best_splits = [i]
            if beta_list[i] == max_prob:
                best_splits.append(i)

        best_split = best_splits[len(best_splits)/2]

        node = BSTTree(key_list[best_split])
        if parent is None:
            root = node
        elif key_list[best_split] < parent.value:
            parent.left = node
        else:
            parent.right = node

        section_queue.put((left_index, best_split - 1, node))
        section_queue.put((best_split + 1, right_index, node))

    return root