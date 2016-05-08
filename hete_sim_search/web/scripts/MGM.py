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
	host_port = 'localhost:7474'
	URI = 'localhost:7474/db/data'
	http.socket_timeout = 9999

	# set up authentication parameters
	authenticate(host_port,user_name,password)

	# connect to authenticated graph database
	graph = Graph("http://"+host_port+"/db/data/")
	print 'graph connected'
	return graph

def execute_query(query):
	cypher = graph.cypher
	result = cypher.execute(query)
	return result

if __name__ == '__main__':

	movie_input = str(raw_input('Enter the movie: '))
	top_K = int(raw_input('Enter k for similarity: '))


	graph = connect_graph()
	query_xx = "MATCH (m:movie {title:'"+movie_input+"'})-[GENRE]->(g:genre) MATCH (g)<-[GENRE]-(m) RETURN m as movie,count(m.title) as count"
	xx = execute_query(query_xx)
	
	if len(xx) == 0:
		xx_value = 0
	else:	
		for result in xx:
			xx_value = int(result.count)
			break
	print "xx: ",xx_value

	query_xy = "MATCH (m:movie {title:'"+movie_input+"'})-[g1:GENRE]->(g:genre)<-[g2:GENRE]-(m2:movie) RETURN m2 as movie,count(m2.title) as count"
	xy = execute_query(query_xy)


hashmap = {}
for result in xy:
	hashmap.setdefault(result.movie['title'],[]) 
	hashmap[result.movie['title']].append(result.count)

	query_yy = "MATCH (m:movie {title:'"+movie_input+"'})-[g1:GENRE]->(g3:genre)<-[g2:GENRE]-(m2:movie) MATCH (m2)-[g4:GENRE]->(g) MATCH (g)<-[g5:GENRE]-(m2) RETURN m2 as movie,count(m2.title) as count"
	yy = execute_query(query_yy)

	for result in yy:
		hashmap[result.movie['title']].append(result.count)

	output_file = open("../../sample_outputs/length_3/" +movie_input+"_output_MGM.txt", "w")

	for key, value in hashmap.iteritems():
		xy_value = int(value[0])
		yy_value = int(value[1])
		score = (2*xy_value)/float((xx_value+yy_value))
		value.append(score)

	sorted_hashmap = sorted(hashmap.items(), key=lambda e: e[1][2],reverse=True)

	for i in range(0,top_K):
		print sorted_hashmap[i][0],sorted_hashmap[i][1][2]

	for i in sorted_hashmap:
		output_file.write(str(i) + '\n')

	output_file.close()