from functions import *

if __name__ == '__main__':

	query = str(sys.argv[1])
	top_K = int(sys.argv[2])
	
	#xx
	query_xx = "MATCH (a:actor {name:'"+query+"'})-[r1:ACTED_IN]->(m:movie) \
				MATCH (m)<-[r2:ACTED_IN]-(a1:actor) \
				MATCH (a1)-[r3:ACTED_IN]->(m2:movie) \
				MATCH (m2)<-[r4:ACTED_IN]-(a) \
				RETURN a as actor, count(a.name) as count" 
	
	#xy
	query_xy = "MATCH (a:actor {name:'"+query+"'})-[r1:ACTED_IN]->(m:movie) \
				MATCH (m)<-[r2:ACTED_IN]-(a1:actor) \
				MATCH (a1)-[r3:ACTED_IN]->(m2:movie) \
				MATCH (m2)<-[r4:ACTED_IN]-(a2:actor) \
				WHERE a2.name <> '"+query+"' \
				RETURN a2 as actor, count(a2.name) as count"
	
	#yy
	query_yy = "MATCH (a:actor {name:'"+query+"'})-[r1:ACTED_IN]->(m:movie) \
				MATCH (m)<-[r2:ACTED_IN]-(a1:actor) \
				MATCH (a1)-[r3:ACTED_IN]->(m2:movie) \
				MATCH (m2)<-[r4:ACTED_IN]-(a2:actor) \
				WHERE a2.name <> '"+query+"' \
				MATCH (a2:actor)-[r5:ACTED_IN]->(m3:movie) \
				MATCH (m3)<-[r6:ACTED_IN]-(a3:actor) \
				MATCH (a3)-[r7:ACTED_IN]->(m4:movie) \
				MATCH (m4)<-[r8:ACTED_IN]-(a2) \
				RETURN a2 as actor,count(a2.name) as count"
	
	find_topK_results(query, top_K, query_xx, query_xy, query_yy)