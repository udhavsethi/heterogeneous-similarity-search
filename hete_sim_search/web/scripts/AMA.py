from functions import *

if __name__ == '__main__':

	actor_input = str(sys.argv[1])
	top_K = int(sys.argv[2])
	
	#xx
	query_xx = "MATCH (a:actor {name:'"+str(actor_input)+"'})-[ACTED_IN]->(m) \
				MATCH (m)<-[r:ACTED_IN]-(a) \
				RETURN a as actor,count(a.name) as count"
	
	#xy
	query_xy = "MATCH (a:actor {name:'"+str(actor_input)+"'})-[r1:ACTED_IN]->(m1:movie)<-[r2:ACTED_IN]-(b:actor) \
				RETURN b as actor,count(b.name) as count"
	
	#yy
	query_yy = "MATCH (a:actor {name:'"+str(actor_input)+"'})-[r1:ACTED_IN]->(m1:movie)<-[r2:ACTED_IN]-(b:actor) \
				MATCH (b)-[r3:ACTED_IN]->(m) \
				MATCH (m)<-[r4:ACTED_IN]-(b) \
				RETURN b as actor,count(b.name) as count"
	
	find_topK_results(actor_input, top_K, query_xx, query_xy, query_yy)