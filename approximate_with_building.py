# approximate_with_building.py
# COMP 150
# Created by Cori Jacoby and Alex King
# 4/6/2017

# Implementation of Mehlhorn's O(n logn) approximation algorithm for optimal
# binary search trees

from Queue import Queue
from BSTTree import BSTTree

# EPSILON = 0.000001

def find_optimal_tree_ordering(beta_list, alpha_list, beta_length, key_list, EPSILON):
    """
    Returns nearly optimal binary search tree given key probabilities
    (beta_list) and gap probabilities (alpha_list)
    """
    element_list = []
    root = None

    # holds subdivisions of beta value array
    section_queue = Queue()

    # triple contains beginning and ending indices of array and probability sum
    # in updated version, we also put the parent node
    section_queue.put((0, beta_length - 1, 1, root))

    # Iteratively find the best root for each subtree
    while not section_queue.empty():

        inserted = False
        # find best split
        (left_index, right_index, prob_sum, parent) = section_queue.get()
        # print "probability sum for", left_index, right_index, "is", prob_sum

        if (left_index < 0 or 
            right_index >= beta_length or 
            left_index > right_index):
            continue

        if left_index == right_index:
            # print "base case with", left_index, right_index
            element_list.append(left_index)
            node = BSTTree(key_list[left_index])
            inserted = True

            if parent is None:
                # print "parent is none in base case"
                root = node
            elif left_index < parent.value:
                # print "best split is smaller so assigning left child"
                parent.left = node
            else:
                # print "best split is larger so assigning right child"
                parent.right = node
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

            # print "left last diff is", left_last_diff

            # Move lefthand pointer inwards and calculate new split
            left_prob_sum += beta_list[left_index + i - 1] + alpha_list[left_index + i]

            new_diff = abs(left_prob_sum - 
                           (prob_sum - left_prob_sum - beta_list[left_index + i]))

            # print "lefthand new prob sum", left_prob_sum
            # print "new diff for left is", new_diff
            # print "and left last diff is", left_last_diff

            if (new_diff < left_last_diff) and (abs(new_diff - left_last_diff) > EPSILON):
                # print "abs value is", abs(new_diff - left_last_diff)
                # print "left will keep moving. left last diff was", left_last_diff, "new diff is", new_diff
                # print "new diff of %f is better than old of %f" % (new_diff, left_last_diff)

                left_last_diff = new_diff

            else:
                best_split = left_index + i - 1
                element_list.append(best_split)
                node = BSTTree(key_list[best_split])
                inserted = True
                if parent is None:
                    root = node
                elif key_list[best_split] < parent.value:
                    parent.left = node
                else:
                    parent.right = node


                # print "inserted index into element_list:", best_split

                prev_left_prob_sum = left_prob_sum - beta_list[left_index + i - 1] - alpha_list[left_index + i]

                section_queue.put((left_index, best_split - 1, prev_left_prob_sum, node))
                section_queue.put((best_split + 1, 
                                  right_index, 
                                  (prob_sum - prev_left_prob_sum - beta_list[best_split]), node))

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
                # print "right will keep moving. right last diff was", right_last_diff, "new diff is", new_diff
                right_last_diff = new_diff
            else:
                
                best_split = right_index - i + 1
                element_list.append(best_split)
                node = BSTTree(key_list[best_split])
                inserted = True
                if parent is None:
                    root = node
                elif key_list[best_split] < parent.value:
                    parent.left = node
                else:
                    parent.right = node
                # print "inserted index into element_list:", best_split

                prev_right_prob_sum = right_prob_sum - beta_list[right_index + 1 - i] - alpha_list[right_index + 1 - i]

                section_queue.put((best_split + 1, right_index, prev_right_prob_sum, node))
                section_queue.put((left_index, 
                                  best_split - 1, 
                                  (prob_sum - 
                                   prev_right_prob_sum - 
                                   beta_list[best_split]), node))

                break

        if not inserted:
            print "Something went wrong at", left_index, right_index, prob_sum, parent
            print "betas from left to right:", beta_list[left_index:right_index+1]
            print "alphas from left to right:", alpha_list[left_index:right_index+2]

    print len(element_list)
    return root
