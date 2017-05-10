# COMP 150 Project

Cori Jacoby, Alex King

This repository holds all code from our project focused on optimal binary search trees.

Files:

* `BSTTree.py`: basic binary search tree implementation used by below algorithms
* `optimal_bst_knuth.py`: implementation of Knuth's O(n^2) dynamic programming algorithm for optimal binary search trees
* `optimal_bst_knuth_n3.py`: un-optimized version of above that runs in O(n^3) time
* `approximate_bst_mehlhorn.py`: implementation of Mehlhorn's O(n*log(n)) approximation algorithm
* `highest_prob_root.py`: implementation of Knuth's poor "Rule 1" approximation algorithm (Also O(n*log(n)))
* `AVLTree.py`: AVL tree implementation
* `generate_test.py`: helper functions related to generating test searches upon probability distributions
* `benchmarks.py`: benchmarking program to compare runtimes and expected depths of different trees
* `bsttests.py`: basic functional tests for binary search tree implementation
* `final_report.pdf`: A thorough report and analysis of all results