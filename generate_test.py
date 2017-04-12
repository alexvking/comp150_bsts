#file to generate different types of test data

import random

#generate test file and prob values given number of values and range
def generate_test(element_range, num_checks):
	test_list = []

	for x in range(num_checks):
		test_list.append(random.randint(0, element_range))

	probs = [float(0)] * (element_range + 1)

	print test_list

	for x in test_list:
		probs[x] += 1 / float(num_checks)

	print probs

	alphas = []
	betas = []
	i = 0

	while i < (len(probs) - 1):
		print "inserting at", i
		alphas.append(probs[i])
		i += 1
		print "inserting at", i
		betas.append(probs[i])
		i += 1

	print "inserting at", i
	alphas.append(probs[i])

	assert(i == (len(probs) - 1))

	return (test_list, betas, alphas)

#generate a list of a given number of searches given alpha and beta values
def generate_search(alphas, betas, num_search):
	test_list = []
	insert_num = 0

	for i in range(len(betas)):
		for e in range(int(alphas[i] * num_search)):
			test_list.append(insert_num)
		insert_num += 1

		for e in range(int(betas[i] * num_search)):
			test_list.append(insert_num)
		insert_num += 1

	for e in range(int(alphas[len(betas)] * num_search)):
		test_list.append(insert_num)

	#could shuffle so it looks random
	return(test_list)

#generate a search list with fuzz given alphas and betas
def generate_fuzz_search(alphas, betas, num):
	test_list = []

	all_probs = [0] * (len(alphas) + len(betas))

	for i in range(len(alphas)):
		all_probs[i * 2] = alphas[i]

	for i in range(len(betas)):
		all_probs[i * 2 + 1] = betas[i]

	sum_probs = [0] * len(all_probs)
	for i in range(len(all_probs)):
		sum_probs[i] = sum_probs[i-1] + all_probs[i]

	print sum_probs

	for i in range(num):
		indicator = random.random()
		for j in range(len(sum_probs)):
			if indicator < sum_probs[j]:
				print "value:", i, "=", indicator, "so inserting", j
				test_list.append(j)
				break

	return (test_list)

def test():
	#print generate_search([.25, .25], [.5], 20)
	#print generate_test(6, 12)
	print generate_fuzz_search([.2, .3], [.5], 12)

test()


