#!usr/bin/python


from py2neo import authenticate,Graph
from py2neo import Node, Relationship
from py2neo.packages.httpstream import http 
# from py2neo import watch
import operator
import sys

def connect_graph():
	# watch('httpstream')
	user_name = 'neo4j'
	password = 'neo4j123'
	
	# port for http: 7474 and for https: 7473
	host_port = '127.0.0.1:7474'
	URI = '127.0.0.1:7474/db/data'
	http.socket_timeout = 9999

	# set up authentication parameters
	authenticate(host_port,user_name,password)

	# connect to authenticated graph database
	graph = Graph("http://"+host_port+"/db/data/")
	cypher = graph.cypher
	
	print 'graph connected'
	return graph

def execute_query(query):
	cypher = graph.cypher
	result = cypher.execute(query)
	return result

if __name__ == '__main__':

	director_input = str(raw_input('Enter the director: '))
	top_K = int(raw_input('Enter k for similarity: '))


	graph = connect_graph()
	query_xx = "MATCH (a:director {name:'"+director_input+"'})-[r1:DIRECTED]->(m:movie) \
				MATCH (m)<-[r2:DIRECTED]-(a1:director) \
				MATCH (a1)-[r3:DIRECTED]->(m2:movie) \
				MATCH (m2)<-[r4:DIRECTED]-(a) \
				RETURN a as director, count(a.name) as count" 
	xx = execute_query(query_xx)
	
	if len(xx) == 0:
		xx_value = 0
	else:	
		for result in xx:
			xx_value = int(result.count)
			break
	print "xx: ",xx_value

	query_xy = "MATCH (a:director {name:'"+director_input+"'})-[r1:DIRECTED]->(m:movie) \
				MATCH (m)<-[r2:DIRECTED]-(a1:director) \
				MATCH (a1)-[r3:DIRECTED]->(m2:movie) \
				MATCH (m2)<-[r4:DIRECTED]-(a2:director) \
				WHERE a2.name <> '"+director_input+"' \
				RETURN a2 as director, count(a2.name) as count"
	xy = execute_query(query_xy)


	hashmap = {}
	for result in xy:
		hashmap.setdefault(result.director['name'],[]) 
		hashmap[result.director['name']].append(result.count)

	query_yy = "MATCH (a:director {name:'"+director_input+"'})-[r1:DIRECTED]->(m:movie) \
				MATCH (m)<-[r2:DIRECTED]-(a1:director) \
				MATCH (a1)-[r3:DIRECTED]->(m2:movie) \
				MATCH (m2)<-[r4:DIRECTED]-(a2:director) \
				WHERE a2.name <> '"+director_input+"' \
				MATCH (a2:director)-[r5:DIRECTED]->(m3:movie) \
				MATCH (m3)<-[r6:DIRECTED]-(a3:director) \
				MATCH (a3)-[r7:DIRECTED]->(m4:movie) \
				MATCH (m4)<-[r8:DIRECTED]-(a2) \
				RETURN a2 as director,count(a2.name) as count"
	yy = execute_query(query_yy)

	for result in yy:
		hashmap[result.director['name']].append(result.count)

	output_file = open("../../sample_outputs/length_5/" +director_input+"_output_DMDMD.txt", "w")

	for key, value in hashmap.iteritems():
		xy_value = int(value[0])
		yy_value = int(value[1])
		score = (2*xy_value)/float((xx_value+yy_value))
		value.append(score)

	sorted_hashmap = sorted(hashmap.items(), key=lambda e: e[1][2], reverse=True)

	for i in range(0,min(len(sorted_hashmap),top_K),1):
		print sorted_hashmap[i][0],sorted_hashmap[i][1][2]

	for i in sorted_hashmap:
		output_file.write(str(i) + '\n')

	output_file.close()