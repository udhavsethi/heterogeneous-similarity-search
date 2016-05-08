#!usr/bin/python

from py2neo import authenticate,Graph
from py2neo import Node, Relationship
from py2neo.packages.httpstream import http 
# from py2neo import watch
import operator
import os
import sys
import json
# import re

def connect_graph():
	# watch('httpstream')
	user_name = 'neo4j'
	password = 'neo4j123'
	# print('function entered')
	
	# port for http: 7474 and for https: 7473
	host_port = '192.168.112.154:7474'
	# host_port = '192.168.136.10:7474'
	# URI = '192.168.136.10:7474/db/data'
	http.socket_timeout = 99999
	
	# set up authentication parameters
	authenticate(host_port,user_name,password)

	# connect to authenticated graph database
	graph = Graph("http://"+host_port+"/db/data/")
	# print('graph connected')
	return graph

def execute_query(query):
	cypher = graph.cypher
	result = cypher.execute(query)
	return result

if __name__ == '__main__':

	actor_input = str(sys.argv[1])
	top_K = int(sys.argv[2])

	outputFilename = os.getcwd() + "\..\outputs" +"\\"+ actor_input + "_" + str(sys.argv[0]).split('.')[0] + ".json"

	if os.path.isfile(outputFilename):
		# f = open(outputFilename,'r')
		# resultList = []
		# for line in f:
		# 	resultList.append(line)
		# 	if len(resultList) >= top_K:
		# 		break
		# print(resultList)
		
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
	xx = execute_query(query_xx)
	
	if len(xx) == 0:
		xx_value = 0
	else:	
		for result in xx:
			xx_value = int(result.count)
			break

	#xy
	query_xy = "MATCH (a:actor {name:'"+str(actor_input)+"'})-[r1:ACTED_IN]->(m1:movie)<-[r2:ACTED_IN]-(b:actor) \
	RETURN b as actor,count(b.name) as count"
	xy = execute_query(query_xy)

	hashmap = {}
	for result in xy:
		hashmap.setdefault(result.actor['name'],[]) 
		hashmap[result.actor['name']].append(result.count)

	#yy
	query_yy = "MATCH (a:actor {name:'"+str(actor_input)+"'})-[r1:ACTED_IN]->(m1:movie)<-[r2:ACTED_IN]-(b:actor) \
	MATCH (b)-[r3:ACTED_IN]->(m) \
	MATCH (m)<-[r4:ACTED_IN]-(b) \
	RETURN b as actor,count(b.name) as count"
	yy = execute_query(query_yy)

	for result in yy:
		key = result.actor['name']
		value = hashmap[key]
		value.append(result.count)
		xy_value = int(value[0])
		yy_value = int(value[1])
		score = (2*xy_value)/float((xx_value+yy_value))
		value.append(score)

	sorted_hashmap = sorted(hashmap.items(), key=lambda e: e[1][2], reverse=True)

	output_file = open(outputFilename, "w+")
	output = []

	for i in range(0,min(100,len(sorted_hashmap)),1):
		outputLine = {"name": sorted_hashmap[i][0], "score": sorted_hashmap[i][1][2] }
		output.append(outputLine)
	
	outJsonObj = {}
	outJsonObj["data"] = output
	output_file.write(outJsonObj)

	# print "hello"
	outJsonObj = {}
	outJsonObj["data"] = output[0:top_K]
	print(json.dumps(outJsonObj))


	# for i in sorted_hashmap:
	# 	output_file.write(str(i) + '\n')

	output_file.close()