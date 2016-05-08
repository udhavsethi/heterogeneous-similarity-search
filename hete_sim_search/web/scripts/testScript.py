# import sys

# print ("test worked " + str(sys.argv[0]) +" "+ str(sys.argv[1]))

#!usr/bin/python

import sys
import json


if __name__ == '__main__':

	# actor_input = str(raw_input('Enter the actor: '))
	# top_K = int(raw_input('Enter k for similarity: '))

	# if len(sys.argv) < 3:
	# 	sys.exit("Usage: python file_name.py actor k_value")

	actor_input = str(sys.argv[0]).split(".")[0]
	top_K = str(sys.argv[2])
	output = []
	output = [[actor_input,top_K]]
	result = json.dumps(output)
	print(result)


	# for i in sorted_hashmap:
		# output_file.write(str(i) + '\n')

	# output_file.close()