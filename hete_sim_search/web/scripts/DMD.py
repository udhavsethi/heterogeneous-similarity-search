from functions import *

if __name__ == '__main__':

	query = str(sys.argv[1])
	top_K = int(sys.argv[2])
	
	#xx
	query_xx = "MATCH (a:director {name:'"+query+"'})-[DIRECTED]->(m) \
				MATCH (m)<-[r:DIRECTED]-(a) \
				RETURN a as query_result,count(a.name) as count"
	
	#xy
	query_xy = "MATCH (a:director {name:'"+query+"'})-[r1:DIRECTED]->(m1:movie)<-[r2:DIRECTED]-(b:director) \
				RETURN b as query_result,count(b.name) as count"
	
	
	#yy
	query_yy = "MATCH (a:director {name:'"+query+"'})-[r1:DIRECTED]->(m1:movie)<-[r2:DIRECTED]-(b:director) \
				MATCH (b)-[r3:DIRECTED]->(m) \
				MATCH (m)<-[r4:DIRECTED]-(b) \
				RETURN b as query_result,count(b.name) as count"
	
	
	find_topK_results(query, top_K, query_xx, query_xy, query_yy)
