from functions import *

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

	hashmap_MGM = {}
	for result in xy:
		hashmap_MGM.setdefault(result.movie['title'],[]) 
		hashmap_MGM[result.movie['title']].append(result.count)

	query_yy = "MATCH (m:movie {title:'"+movie_input+"'})-[g1:GENRE]->(g3:genre)<-[g2:GENRE]-(m2:movie) \
				MATCH (m2)-[g4:GENRE]->(g) \
				MATCH (g)<-[g5:GENRE]-(m2) \
				RETURN m2 as movie,count(m2.title) as count"
	yy = execute_query(query_yy,graph)

	for result in yy:
		key = result.movie['title']
		value = hashmap_MGM[key]
		value.append(result.count)
		xy_value = int(value[0])
		yy_value = int(value[1])
		score = (2*xy_value)/float((xx_value+yy_value))
		value.append(score)

	'''
	MAM
	'''
	query_xx = "MATCH (m:movie {title:'"+movie_input+"'})<-[ACTED_IN]-(a:actor) MATCH (a)-[ACTED_IN]->(m) \
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

	query_xy = "MATCH (m:movie {title:'"+movie_input+"'})<-[a1:ACTED_IN]-(a:actor)-[a2:ACTED_IN]->(m2:movie) \
				RETURN m2 as movie,count(m2.title) as count"
	xy = execute_query(query_xy,graph)

	hashmap_MAM = {}
	for result in xy:
		hashmap_MAM.setdefault(result.movie['title'],[]) 
		hashmap_MAM[result.movie['title']].append(result.count)

	query_yy = "MATCH (m:movie {title:'"+movie_input+"'})<-[a1:ACTED_IN]-(a:actor)-[a2:ACTED_IN]->(m2:movie) \
				MATCH (m2)<-[a4:ACTED_IN]->(a) \
				MATCH (a)<-[a5:ACTED_IN]-(m2) \
				RETURN m2 as movie,count(m2.title) as count"
	yy = execute_query(query_yy,graph)

	for result in yy:
		key = result.movie['title']
		value = hashmap_MAM[key]
		value.append(result.count)
		xy_value = int(value[0])
		yy_value = int(value[1])
		score = (2*xy_value)/float((xx_value+yy_value))
		value.append(score)

	'''
	MAxM
	'''
	query_xx = "MATCH (m:movie {title:'"+movie_input+"'})<-[ACTED_IN]-(a:actresses) MATCH (a)-[ACTED_IN]->(m) \
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

	query_xy = "MATCH (m:movie {title:'"+movie_input+"'})<-[a1:ACTED_IN]-(a:actresses)-[a2:ACTED_IN]->(m2:movie) \
				RETURN m2 as movie,count(m2.title) as count"
	xy = execute_query(query_xy,graph)

	hashmap_MAxM = {}
	for result in xy:
		hashmap_MAxM.setdefault(result.movie['title'],[]) 
		hashmap_MAxM[result.movie['title']].append(result.count)

	query_yy = "MATCH (m:movie {title:'"+movie_input+"'})<-[a1:ACTED_IN]-(a:actresses)-[a2:ACTED_IN]->(m2:movie) \
				MATCH (m2)<-[a4:ACTED_IN]->(a) \
				MATCH (a)<-[a5:ACTED_IN]-(m2) \
				RETURN m2 as movie,count(m2.title) as count"
	yy = execute_query(query_yy,graph)

	for result in yy:
		key = result.movie['title']
		value = hashmap_MAxM[key]
		value.append(result.count)
		xy_value = int(value[0])
		yy_value = int(value[1])
		score = (2*xy_value)/float((xx_value+yy_value))
		value.append(score)

	'''
	MDM
	'''

	query_xx = "MATCH (m:movie {title:'"+movie_input+"'})<-[DIRECTED]-(a:director) MATCH (a)-[DIRECTED]->(m) \
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

	query_xy = "MATCH (m:movie {title:'"+movie_input+"'})<-[a1:DIRECTED]-(a:director)-[a2:DIRECTED]->(m2:movie) \
				RETURN m2 as movie,count(m2.title) as count"
	xy = execute_query(query_xy,graph)

	hashmap_MDM = {}
	for result in xy:
		hashmap_MDM.setdefault(result.movie['title'],[]) 
		hashmap_MDM[result.movie['title']].append(result.count)

	query_yy = "MATCH (m:movie {title:'"+movie_input+"'})<-[a1:DIRECTED]-(a:director)-[a2:DIRECTED]->(m2:movie) \
				MATCH (m2)<-[a4:ACTED_IN]->(a) \
				MATCH (a)<-[a5:ACTED_IN]-(m2) \
				RETURN m2 as movie,count(m2.title) as count"
	yy = execute_query(query_yy,graph)

	for result in yy:
		key = result.movie['title']
		value = hashmap_MDM[key]
		value.append(result.count)
		xy_value = int(value[0])
		yy_value = int(value[1])
		score = (2*xy_value)/float((xx_value+yy_value))
		value.append(score)

	final_hashmap = {}
	for key in hashmap_MGM:
		value = hashmap_MGM[key]
		score_MGM = float(value[2])
		score_MAM = score_MAxM = score_MDM = 0.0
		if key in hashmap_MAM:
			score_MAM = float(hashmap_MAM[key][2])
		if key in hashmap_MAxM:
			score_MAxM = float(hashmap_MAxM[key][2])
		if key in hashmap_MDM:
			score_MDM = float(hashmap_MDM[key][2])

		final_score = 0.75*score_MGM + 0.25*(score_MAM+score_MAxM+score_MDM)
		final_hashmap[key] = final_score

	sorted_list = sorted(final_hashmap.values(), reverse=True)

	output = []
	for i in range(0,min(100,len(sorted_list)),1):
		outputLine = {"name": sorted_list[i][0], "score": sorted_list[i][1]}
		output.append(outputLine)
	
	outJsonObj = {}
	outJsonObj["data"] = output

	output_file = open(outputFilename, "w+")
	output_file.write(json.dumps(outJsonObj))

	outJsonObj = {}
	outJsonObj["data"] = output[0:top_K]
	print(json.dumps(outJsonObj))

	output_file.close()