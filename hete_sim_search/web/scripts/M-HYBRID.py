from functions import *

if __name__ == '__main__':

	query = str(sys.argv[1])
	top_K = int(sys.argv[2])
	
	

if __name__ == '__main__':

	movie_input = str(sys.argv[1])
	top_K = int(sys.argv[2])

	outputFilename = os.getcwd() + "\..\outputs" +"\\"+ query + "_" + str(sys.argv[0]).split('.')[0] + ".json"

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

	query_xx = "MATCH (m:movie {title:'"+movie_input+"'})-[GENRE]->(g:genre) MATCH (g)<-[GENRE]-(m) \
				RETURN m as movie,count(m.title) as count"
	xx = execute_query(query_xx,graph)
	
	if len(xx) == 0:
		xx_value = 0
		jsonResult = {"data": []}
		print(json.dumps(jsonResult))
		sys.exit()
	else:	
		for result in xx:
			xx_value = int(result.count)
			break

	query_xy = "MATCH (m:movie {title:'"+movie_input+"'})-[g1:GENRE]->(g:genre)<-[g2:GENRE]-(m2:movie) \
				RETURN m2 as movie,count(m2.title) as count"
	xy = execute_query(query_xy,graph)

	hashmap = {}
	for result in xy:
		hashmap.setdefault(result.movie['title'],[]) 
		hashmap[result.movie['title']].append(result.count)

	query_yy = "MATCH (m:movie {title:'"+movie_input+"'})-[g1:GENRE]->(g3:genre)<-[g2:GENRE]-(m2:movie) \
				MATCH (m2)-[g4:GENRE]->(g) \
				MATCH (g)<-[g5:GENRE]-(m2) \
				RETURN m2 as movie,count(m2.title) as count"
	yy = execute_query(query_yy,graph)

	for result in yy:
		key = result.movie['title']
		value = hashmap[key]
		value.append(result.count)
		xy_value = int(value[0])
		yy_value = int(value[1])
		score = (2*xy_value)/float((xx_value+yy_value))
		value.append(score)

	sorted_hashmap = sorted(hashmap.items(), key=lambda e: e[1][2],reverse=True)

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