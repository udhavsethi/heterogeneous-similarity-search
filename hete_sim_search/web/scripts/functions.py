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