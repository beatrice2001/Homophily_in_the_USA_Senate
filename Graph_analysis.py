import networkx as nx
import statistics as stat

G = nx.read_gml("Graph.gml")

def calc_wPH_party(node):
    if G.nodes[node]['party'] == 'rep':
        wPH_party = (1-PR_rep) / (PR_rep-PR[node])
    elif G.nodes[node]['party'] == 'dem':
        wPH_party = (1-PR_dem) / (PR_dem-PR[node])
    elif G.nodes[node]['party'] == 'ind':
        wPH_party = (1-PR_ind) / (PR_ind-PR[node])

    return wPH_party

def calc_wPH_sex(node):
    if G.nodes[node]['sex'] == 'm':
        wPH_sex = (1-PR_male) / (PR_male-PR[node])
    elif G.nodes[node]['sex'] == 'f':
        wPH_sex = (1-PR_female) / (PR_female-PR[node])

    return wPH_sex

def calc_PH_party(node,w):
    if G.out_degree(node) == 0:
        WEI = 0
    else:
        WEI = ( G.nodes[node]['ePH_party'] / w - G.nodes[node]['iPH_party'] ) / ( G.nodes[node]['ePH_party'] / w + G.nodes[node]['iPH_party'] )
    return WEI

def calc_PH_sex(node,w):
    if G.out_degree(node) == 0:
        WEI = 0
    else:
        WEI = ( G.nodes[node]['ePH_sex'] / w - G.nodes[node]['iPH_sex'] ) / ( G.nodes[node]['ePH_sex'] / w + G.nodes[node]['iPH_sex'] )
    return WEI

#calculation of general parameters

rep=0
dem=0
ind=0
male=0
female=0
n_nodes=0
PR = nx.pagerank(G)
PR_tot = sum(PR[node] for node in PR)      #for normalization (if necessary)
PR_rep = 0
PR_dem = 0
PR_ind = 0
PR_male = 0
PR_female = 0

for node, data in G.nodes(data=True):
    if data['party']=='rep':
            rep += 1
            PR_rep += PR[node]
    elif data['party']=='dem':
            dem += 1
            PR_dem += PR[node]
    elif data['party']=='ind':
        ind += 1
        PR_ind += PR[node]

    if data['sex']=='m':
        male += 1
        PR_male += PR[node]
    elif data['sex']=='f':
        female += 1
        PR_female += PR[node]

    n_nodes += 1

if n_nodes != 100:
    print('Errore: nodi contati = ' + str(n_nodes))

fr_male = male/n_nodes
fr_female = female/n_nodes
fr_dem = dem/n_nodes
fr_rep = rep/n_nodes
fr_ind = ind/n_nodes

#calculation of EI/WEI indexes

nx.set_node_attributes(G,0,'i_party')
nx.set_node_attributes(G,0,'i_sex')
nx.set_node_attributes(G,0,'WEI_party')
nx.set_node_attributes(G,0,'WEI_sex')
nx.set_node_attributes(G,0,'EI_party')
nx.set_node_attributes(G,0,'EI_sex')

for node, node_attr in G.nodes(data=True):
    
    #calculation of i_n
    for out_edge in G.out_edges(nbunch=node, data=False):
        if G.nodes[out_edge[1]]['party'] == G.nodes[node]['party']:
            G.nodes[node]['i_party'] += 1
        if G.nodes[out_edge[1]]['sex'] == G.nodes[node]['sex']:
            G.nodes[node]['i_sex'] += 1

    #calculation of w_n
    if node_attr['party'] == 'rep':
        w_party = (100-rep) / (rep-1)
    elif node_attr['party'] == 'dem':
        w_party = (100-dem) / (dem-1)
    elif node_attr['party'] == 'ind':
        w_party = (100-ind) / (ind-1)
    if node_attr['sex'] == 'm':
        w_sex = (100-male) / (male-1)
    elif node_attr['sex'] == 'f':
        w_sex = (100-female) / (female-1)
    
    if G.out_degree(node) == 0:
        G.nodes[node]['WEI_party'] = 0
        G.nodes[node]['EI_party'] = 0
        G.nodes[node]['WEI_sex'] = 0
        G.nodes[node]['EI_sex'] = 0
    else:
        G.nodes[node]['WEI_party'] = ( (G.out_degree(node)-G.nodes[node]['i_party']) / w_party - G.nodes[node]['i_party'] ) / ( (G.out_degree(node)-G.nodes[node]['i_party']) / w_party + G.nodes[node]['i_party'] )
        G.nodes[node]['EI_party'] = (G.out_degree[node] - 2*G.nodes[node]['i_party']) / (G.out_degree(node))
        G.nodes[node]['WEI_sex'] = ( (G.out_degree(node)-G.nodes[node]['i_sex']) / w_sex - G.nodes[node]['i_sex'] ) / ( (G.out_degree(node)-G.nodes[node]['i_sex']) / w_sex + G.nodes[node]['i_sex'] )
        G.nodes[node]['EI_sex'] = (G.out_degree[node] - 2*G.nodes[node]['i_sex']) / (G.out_degree(node))

WEI_party = stat.fmean(G.nodes[node]['WEI_party'] for node in G.nodes())
EI_party = stat.fmean(G.nodes[node]['EI_party'] for node in G.nodes())
WEI_sex = stat.fmean(G.nodes[node]['WEI_sex'] for node in G.nodes())
EI_sex = stat.fmean(G.nodes[node]['EI_sex'] for node in G.nodes())

#calculation of PH index (with PageRank)

nx.set_node_attributes(G,0,'PR')
nx.set_node_attributes(G,0,'iPH_party')
nx.set_node_attributes(G,0,'iPH_sex')
nx.set_node_attributes(G,0,'ePH_party')
nx.set_node_attributes(G,0,'ePH_sex')
nx.set_node_attributes(G,0,'PH_party')
nx.set_node_attributes(G,0,'PH_sex')

for node in G.nodes():
    G.nodes[node]['PR'] = PR[node] / PR_tot

for node in G.nodes():

    #claculation of i_n and e_n
    for out_edge in G.out_edges(nbunch=node):
        if G.nodes[out_edge[1]]['party'] == G.nodes[node]['party']:
            G.nodes[node]['iPH_party'] += G.nodes[out_edge[1]]['PR']
        else:
            G.nodes[node]['ePH_party'] += G.nodes[out_edge[1]]['PR']
        if G.nodes[out_edge[1]]['sex'] == G.nodes[node]['sex']:
            G.nodes[node]['iPH_sex'] += G.nodes[out_edge[1]]['PR']
        else:
            G.nodes[node]['ePH_sex'] += G.nodes[out_edge[1]]['PR']

    #calculation of w_n
    if G.nodes[node]['party'] == 'rep':
        wPH_party = (1-PR_rep) / (PR_rep-PR[node])
    elif G.nodes[node]['party'] == 'dem':
        wPH_party = (1-PR_dem) / (PR_dem-PR[node])
    elif G.nodes[node]['party'] == 'ind':
        wPH_party = (1-PR_ind) / (PR_ind-PR[node])
    if G.nodes[node]['sex'] == 'm':
        wPH_sex = (1-PR_male) / (PR_male-PR[node])
    elif G.nodes[node]['sex'] == 'f':
        wPH_sex = (1-PR_female) / (PR_female-PR[node])

    #calculation of PH
    G.nodes[node]['PH_party'] = calc_PH_party(node, wPH_party)
    G.nodes[node]['PH_sex'] = calc_PH_sex(node, wPH_sex)
    if G.out_degree(node) == 0:
        G.nodes[node]['PH_party'] = 0
        G.nodes[node]['PH_sex'] = 0
    else:
        G.nodes[node]['PH_party'] = ( G.nodes[node]['ePH_party'] / wPH_party - G.nodes[node]['iPH_party'] ) / ( G.nodes[node]['ePH_party'] / wPH_party + G.nodes[node]['iPH_party'] )
        G.nodes[node]['PH_sex'] = ( G.nodes[node]['ePH_sex'] / wPH_sex - G.nodes[node]['iPH_sex'] ) / ( G.nodes[node]['ePH_sex'] / wPH_sex + G.nodes[node]['iPH_sex'] )

PH_party = 0
PH_sex = 0
for node in G.nodes():
    PH_party += G.nodes[node]['PH_party'] * G.nodes[node]['PR']
    PH_sex += G.nodes[node]['PH_sex'] * G.nodes[node]['PR']

PH_rep = 0
WEI_rep = 0
EI_rep = 0
PH_dem = 0
WEI_dem = 0
EI_dem = 0
PH_ind = 0
WEI_ind = 0
EI_ind = 0
PH_male = 0
WEI_male = 0
EI_male = 0
PH_female = 0
WEI_female = 0
EI_female = 0
for node in G.nodes():
    if G.nodes[node]['party'] == 'rep':
        PH_rep += G.nodes[node]['PH_party']*G.nodes[node]['PR']
        WEI_rep += G.nodes[node]['WEI_party']
        EI_rep += G.nodes[node]['EI_party']
    elif G.nodes[node]['party'] == 'dem':
        PH_dem += G.nodes[node]['PH_party']*G.nodes[node]['PR']
        WEI_dem += G.nodes[node]['WEI_party']
        EI_dem += G.nodes[node]['EI_party']
    elif G.nodes[node]['party'] == 'ind':
        PH_ind += G.nodes[node]['PH_party']*G.nodes[node]['PR']
        WEI_ind += G.nodes[node]['WEI_party']
        EI_ind += G.nodes[node]['EI_party']
    if G.nodes[node]['sex'] == 'm':
        PH_male += G.nodes[node]['PH_sex']*G.nodes[node]['PR']
        WEI_male += G.nodes[node]['WEI_sex']
        EI_male += G.nodes[node]['EI_sex']
    elif G.nodes[node]['sex'] == 'f':
        PH_female += G.nodes[node]['PH_sex']*G.nodes[node]['PR']
        WEI_female += G.nodes[node]['WEI_sex']
        EI_female += G.nodes[node]['EI_sex']
PH_dem /= PR_dem
WEI_dem /= dem
EI_dem /= dem
PH_rep /= PR_rep
WEI_rep /= rep
EI_rep /= rep
PH_ind /= PR_ind
WEI_ind /= ind
EI_ind /= ind
PH_male /= PR_male
WEI_male /= male
EI_male /= male
PH_female /= PR_female
WEI_female /= female
EI_female /= female

#results printing and exporting

print("Out_Degree = " + str(stat.fmean(G.out_degree[node] for node in G.nodes)) )
print("In_Degree = " + str(stat.fmean(G.in_degree[node] for node in G.nodes)) )
print("Dem = " + str(fr_dem*100) + "%")
print("Rep = " + str(fr_rep*100) + "%")
print("Ind = " + str(fr_ind*100) + "%")
print("Males = " + str(fr_male*100) + "%")
print("Females = " + str(fr_female*100) + "%")

print("PageRank = " + str(stat.fmean(G.nodes[node]['PR'] for node in G.nodes())))
print("PR_max = " + str(max( G.nodes[node]['PR'] for node in G.nodes()) ))
print("PR_min = " + str(min( G.nodes[node]['PR'] for node in G.nodes()) ))
print("\n")

print('WEI_party = ' + str(WEI_party))
print('EI_party = ' + str(EI_party))
print('PH_party = ' + str(PH_party))
print('WEI_sex = ' + str(WEI_sex))
print('EI_sex = ' + str(EI_sex))
print('PH_sex = ' + str(PH_sex))
print("\n")

print("PH_dem = " + str(PH_dem))
print("WEI_dem = " + str(WEI_dem))
print("EI_dem = " + str(EI_dem))
print("PH_rep = " + str(PH_rep))
print("WEI_rep = " + str(WEI_rep))
print("EI_rep = " + str(EI_rep))
print("PH_ind = " + str(PH_ind))
print("WEI_ind = " + str(WEI_ind))
print("EI_ind = " + str(EI_ind))
print("PH_male = " + str(PH_male))
print("WEI_male = " + str(WEI_male))
print("EI_male = " + str(EI_male))
print("PH_female = " + str(PH_female))
print("WEI_female = " + str(WEI_female))
print("EI_female = " + str(EI_female))

nx.write_gml(G, "Graph_data.gml")