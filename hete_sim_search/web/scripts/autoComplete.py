from functions import *

if __name__ == '__main__':
	label = str(sys.argv[1])
	query = str(sys.argv[2])

	auto_complete_query =  " MATCH (n: "+label+") "
	if (label == 'movie'):
		auto_complete_query += " WHERE n.title =~ '(?i)"+query+".*' "
	else:
		auto_complete_query += " WHERE n.name =~ '(?i)"+query+".*' "
	
	auto_complete_query += " RETURN n as query_result LIMIT 10 "
	
	graph = connect_graph()
	result = execute_query(auto_complete_query, graph)

	output_suggestion = []
	for r in result:
		if label == 'movie':
			key = r.query_result['title']
		else:
			key = r.query_result['name']
		output_suggestion.append(key)
	outputJson = {"suggestions": output_suggestion[0:min(len(output_suggestion),10)]}
	print(json.dumps(outputJson))






