#!usr/bin/python

from functions import *

if __name__ == '__main__':

	actor_input = str(sys.argv[1])
	top_K = int(sys.argv[2])

	# print(actor_input, top_K)
	# sys.exit()

	outputFilename = os.getcwd() + "\..\outputs" +"\\"+ actor_input + "_" + str(sys.argv[0]).split('.')[0] + ".json"

	if os.path.isfile(outputFilename) and os.stat(outputFilename).st_size > 0:
		with open(outputFilename, encoding='utf-8') as f:
			data = json.load(f)

		resultList = data["data"]
		resultList = resultList[0:min(len(resultList),top_K)]
		resultJson = {}
		resultJson["data"] = resultList
		print(json.dumps(resultJson))
		sys.exit()

	graph = connect_graph()
	
	#xx
	query_xx = "MATCH (a:actor {name:'"+str(actor_input)+"'})-[ACTED_IN]->(m) \
	MATCH (m)<-[r:ACTED_IN]-(a) \
	RETURN a as actor,count(a.name) as count"
	xx = execute_query(query_xx,graph)
	
	if len(xx) == 0:
		xx_value = 0
	else:	
		for result in xx:
			xx_value = int(result.count)
			break

	#xy
	query_xy = "MATCH (a:actor {name:'"+str(actor_input)+"'})-[r1:ACTED_IN]->(m1:movie)<-[r2:ACTED_IN]-(b:actor) \
	RETURN b as actor,count(b.name) as count"
	xy = execute_query(query_xy,graph)

	hashmap = {}
	for result in xy:
		hashmap.setdefault(result.actor['name'],[]) 
		hashmap[result.actor['name']].append(result.count)

	#yy
	query_yy = "MATCH (a:actor {name:'"+str(actor_input)+"'})-[r1:ACTED_IN]->(m1:movie)<-[r2:ACTED_IN]-(b:actor) \
	MATCH (b)-[r3:ACTED_IN]->(m) \
	MATCH (m)<-[r4:ACTED_IN]-(b) \
	RETURN b as actor,count(b.name) as count"
	yy = execute_query(query_yy,graph)

	for result in yy:
		key = result.actor['name']
		value = hashmap[key]
		value.append(result.count)
		xy_value = int(value[0])
		yy_value = int(value[1])
		score = (2*xy_value)/float((xx_value+yy_value))
		value.append(score)

	sorted_hashmap = sorted(hashmap.items(), key=lambda e: e[1][2], reverse=True)

	output = []
	for i in range(0,min(100,len(sorted_hashmap)),1):
		outputLine = {"name": sorted_hashmap[i][0], "score": sorted_hashmap[i][1][2] }
		output.append(outputLine)
	
	outJsonObj = {}
	outJsonObj["data"] = output

	output_file = open(outputFilename, "w+")
	output_file.write(json.dumps(outJsonObj))

	outJsonObj = {}
	outJsonObj["data"] = output[0:top_K]
	print(json.dumps(outJsonObj))

	output_file.close()