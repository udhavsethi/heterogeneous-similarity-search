from functions import *

if __name__ == '__main__':

	query = str(sys.argv[1])
	top_K = int(sys.argv[2])
	
	#xx
	query_xx = "MATCH (a:director {name:'"+query+"'})-[r1:DIRECTED]->(m:movie) \
				MATCH (m)-[r2:GENRE]->(a1:genre) \
				MATCH (a1)<-[r3:GENRE]-(m2:movie) \
				MATCH (m2)<-[r4:DIRECTED]-(a) \
				RETURN a as query_result, count(a.name) as count" 
	#xy
	query_xy = "MATCH (a:director {name:'"+query+"'})-[r1:DIRECTED]->(m:movie) \
				MATCH (m)-[r2:GENRE]->(a1:genre) \
				MATCH (a1)<-[r3:GENRE]-(m2:movie) \
				MATCH (m2)<-[r4:DIRECTED]-(a2:director) \
				WHERE a2.name <> '"+query+"' \
				RETURN a2 as query_result, count(a2.name) as count"
	
	#yy
	query_yy = "MATCH (a:director {name:'"+query+"'})-[r1:DIRECTED]->(m:movie) \
				MATCH (m)-[r2:GENRE]->(a1:genre) \
				MATCH (a1)<-[r3:GENRE]-(m2:movie) \
				MATCH (m2)<-[r4:DIRECTED]-(a2:director) \
				WHERE a2.name <> '"+query+"' \
				MATCH (a2:director)-[r5:DIRECTED]->(m3:movie) \
				MATCH (m3)-[r6:GENRE]->(a3:genre) \
				MATCH (a3)<-[r7:GENRE]-(m4:movie) \
				MATCH (m4)<-[r8:DIRECTED]-(a2) \
				RETURN a2 as query_result,count(a2.name) as count"
	
	find_topK_results(query, top_K, query_xx, query_xy, query_yy)