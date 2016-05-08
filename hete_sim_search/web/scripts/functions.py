from py2neo import authenticate,Graph
from py2neo import Node, Relationship
from py2neo.packages.httpstream import http 
import operator, os, sys, json

def connect_graph():
	user_name = 'neo4j'
	password = 'neo4j123'
	
	# port for http: 7474 and for https: 7473
	host_port = '192.168.112.154:7474'
	# host_port = '192.168.136.10:7474'
	http.socket_timeout = 99999
	
	# set up authentication parameters
	authenticate(host_port,user_name,password)

	# connect to authenticated graph database
	graph = Graph("http://"+host_port+"/db/data/")
	return graph

def execute_query(query,graph):
	cypher = graph.cypher
	result = cypher.execute(query)
	return result

def find_topK_results(query, top_K, query_xx, query_xy, query_yy):
	try:
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
		
		#xx
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

		#xy
		xy = execute_query(query_xy,graph)

		hashmap = {}
		for result in xy:
			hashmap.setdefault(result.query_result['name'],[]) 
			hashmap[result.query_result['name']].append(result.count)

		#yy
		yy = execute_query(query_yy,graph)

		for result in yy:
			key = result.query_result['name']
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
	except Exception:
		resultJson = {}
		resultJson["data"] = ["Error"]
		print(json.dumps(resultJson))
		sys.exit()
	