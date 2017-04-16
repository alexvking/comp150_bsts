# approximate_bst_nlogn.py
# COMP 150
# Created by Cori Jacoby and Alex King
# 4/6/2017

# Implementation of Mehlhorn's O(n logn) approximation algorithm for optimal
# binary search trees

from Queue import Queue
from BSTTree import BSTTree

EPSILON = 0.000000000001

def find_optimal_tree_ordering(beta_list, alpha_list, beta_length):
    """
    Returns optimal insertion order of keys given a list of key probabilities
    (beta_list) and gap probabilities (alpha_list)
    """
    element_list = []

    # holds subdivisions of beta value array
    section_queue = Queue()

    # triple contains beginning and ending indices of array and probability sum
    section_queue.put((0, beta_length - 1, 1))

    # Iteratively find the best root for each subtree
    while not section_queue.empty():

        # find best split
        (left_index, right_index, prob_sum) = section_queue.get()
        # print "popped off:", left_index, right_index, prob_sum

        if (left_index < 0 or 
            right_index >= beta_length or 
            left_index > right_index):
            continue

        if left_index == right_index:
            element_list.append(left_index)
            continue

        left_prob_sum = alpha_list[left_index]
        right_prob_sum = alpha_list[right_index + 1]

        # print "lefthand and righthand sums: ", left_prob_sum, right_prob_sum

        left_last_diff = abs(left_prob_sum - 
                             (prob_sum - left_prob_sum - beta_list[left_index]))
        
        right_last_diff = abs(right_prob_sum -
                              (prob_sum - 
                               right_prob_sum - 
                               beta_list[right_index]))

        for i in xrange(1, (right_index - left_index + 1)):
            # print "inside loop at ", i

            # Move lefthand pointer inwards and calculate new split
            left_prob_sum += beta_list[left_index + i - 1] + alpha_list[left_index + i]

            new_diff = abs(left_prob_sum - 
                           (prob_sum - left_prob_sum - beta_list[left_index + i]))

            # print "lefthand new prob sum", left_prob_sum
            # print "new diff for left is", new_diff

            if new_diff < left_last_diff and abs(new_diff - left_last_diff) > EPSILON:
               left_last_diff = new_diff
            else:
                best_split = left_index + i - 1
                element_list.append(best_split)
                # print "inserted index into element_list:", best_split

                prev_left_prob_sum = left_prob_sum - beta_list[left_index + i - 1] - alpha_list[left_index + i]

                section_queue.put((left_index, best_split - 1, prev_left_prob_sum))
                section_queue.put((best_split + 1, 
                                  right_index, 
                                  (prob_sum - prev_left_prob_sum - beta_list[best_split])))

                break

            # Move righthand pointer inwards and calculate new split
            right_prob_sum += (beta_list[right_index + 1 - i] +
                               alpha_list[right_index + 1 - i])

            new_diff = abs(right_prob_sum -
                           (prob_sum - 
                            right_prob_sum - 
                            beta_list[right_index - i]))

            # print "righthand prob sum", right_prob_sum
            # print "new diff for right is", new_diff

            if new_diff < right_last_diff and abs(new_diff - right_last_diff) > EPSILON:
                right_last_diff = new_diff
            else:
                best_split = right_index - i + 1
                element_list.append(best_split)
                # print "inserted index into element_list:", best_split

                prev_right_prob_sum = right_prob_sum - (beta_list[right_index + 1 - i] - alpha_list[right_index + 1 - i])

                section_queue.put((best_split + 1, right_index, prev_right_prob_sum))
                section_queue.put((left_index, 
                                  best_split - 1, 
                                  (prob_sum - 
                                   prev_right_prob_sum - 
                                   beta_list[best_split])))

                break

    return element_list

def test():
    result = find_optimal_tree_ordering([.3, .1, .3], [.075, .075, .075, .075], 3)
    print "\n1 0 2:", result

    result = find_optimal_tree_ordering([.05, .05, .05], [.45, .1, .1, .2], 3)
    print "\n0 2 1:", result

    result = find_optimal_tree_ordering([.05, .2, .05], [.45, .1, .1, .05], 3)
    print "\n0 1 2:", result

    result = find_optimal_tree_ordering([.05, .05, .1, .15], [.2, .1, .1, .15, .15], 4)
    print "\n2 0 3 1", result
    print "Tests completed without errors"

# test()
