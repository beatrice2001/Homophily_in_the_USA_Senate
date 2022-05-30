# Homophily_in_the_USA_Senate
Codes for the creation of a follower/following graph with data taken through Twitter API and for the analysis of homophily.

Instructions:
- Senators_gather.py uses the data in Senate.txt (an example for how to format this file can be found) and extracts the Senators' Twitter accounts' IDs, generating the file Senate_ids.txt
- Graph_gen.py usws the data in Senate_ids.txt and creates a Graph.gml file, in which the follower/following network is created
- Graph_analysis.py uses the data in Graph.gml to compute metrics for homophily
