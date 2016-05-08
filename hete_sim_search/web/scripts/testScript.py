#!usr/bin/python

import sys
import json


if __name__ == '__main__':

	actor_input = str(sys.argv[0]).split(".")[0]
	top_K = str(sys.argv[2])
	output = []
	output = [[actor_input,top_K]]
	result = json.dumps(output)
	print(result)