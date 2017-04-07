# approximate_bst_nlogn.py
# COMP 150
# Created by Cori Jacoby and Alex King
# 4/6/2017

# Implementation of Mehlhorn's O(n logn) approximation algorithm for optimal
# binary search trees

from Queue import Queue
from BSTTree import BSTTree

# find_optimal_tree_ordering : alpha_list, beta_list, beta_length -> list(num)
# returns BSTTree object based on even weighted subtrees

def find_optimal_tree_ordering(beta_list, alpha_list, beta_length):
    element_list = []

    # holds subdivisions of beta array
    section_queue = Queue()

    # triple contains beginning and ending indices of array and probability sum
    section_queue.put((0, beta_length - 1, 1))

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
            # move left to the right by one, move right to the left by one
            # adjust the probability sums as necessary
            # compare the differences with the most recent ones
            # if a smaller difference, continue
            # if a larger difference, break
                # backtrack to last split and break


            # Move lefthand pointer inwards and calculate new split
            left_prob_sum += beta_list[left_index + i - 1] + alpha_list[left_index + i]

            new_diff = abs(left_prob_sum - 
                           (prob_sum - left_prob_sum - beta_list[left_index + i]))

            # print "lefthand new prob sum", left_prob_sum
            # print "new diff for left is", new_diff

            if new_diff < left_last_diff:
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

            if new_diff < right_last_diff:
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
    # print find_optimal_tree_ordering([.25, .25], [.5], 1)
    # print find_optimal_tree_ordering([.1, .1], [.2, .2, .4], 2)

    result = find_optimal_tree_ordering([.3, .1, .3], [.075, .075, .075, .075], 3)
    print "\n1 0 2:", result

    result = find_optimal_tree_ordering([.05, .05, .05], [.45, .1, .1, .2], 3)
    print "\n0 2 1:", result

    result = find_optimal_tree_ordering([.05, .2, .05], [.45, .1, .1, .05], 3)
    print "\n0 1 2:", result

    result = find_optimal_tree_ordering([.05, .05, .1, .15], [.2, .1, .1, .15, .15], 4)
    print "\n2 0 3 1", result

    # print "1 0 2:", find_optimal_tree_ordering([.3, .1, .3], [.075, .075, .075, .075], 3)
    # print "0 2 1:", find_optimal_tree_ordering([.05, .05, .05], [.45, .1, .1, .2], 3)
    # print "0 1 2:", find_optimal_tree_ordering([.05, .2, .05], [.45, .1, .1, .05], 3)
    print "Tests completed without errors"

test()
