import argparse
import math
from pprint import pprint
import itertools as iter

parser = argparse.ArgumentParser()
parser.add_argument("filename", help="name of input file")
parser.add_argument("-n",  "--team_number", type=int)
args = parser.parse_args()


g = {}
with open(args.filename) as graph_input:
    for line in graph_input:
        # split line and convert line parts to integers
        nodes = [int(x) for x in line.split()]
        if len(nodes) != 2:
            continue
        if nodes[0] not in g:
            g[nodes[0]] = []
        if nodes[1] not in g:
            g[nodes[1]] = []
        g[nodes[0]].append(nodes[1])
        g[nodes[1]].append(nodes[0])


#print("GRAPH:",g)
team_list = [[] for x in g.keys()]

for i,k in g.items():
    team_list[i-1].append(i)

n = sum(len(v) for v in g.values())

Ai = 0
Q = 0
elements=[]

for i in g.keys():
    for j in g[i]:
        Ai= (Ai + 1) /n
    Q = Q -math.pow(Ai,2)

def eii(team):
    Eii = 0
    for i in team:
        if len(team) == 1:
            Eii =+ 0
        else:
            Eii = Eii + 2
    return Eii/n


def eij(i, j):
    for w in i:
        for q in j:
            if q in g[w] and q not in i:
                Eij =+ 1
    return Eij / n

g1={}
f=0
s=0
#DQ=0
#DQmax = 0

if args.team_number:
    f = args.team_number
else:
    f = 2
while len(team_list) > f :
    elements=[]
    s=0
    for team in iter.combinations(team_list, 2):
        for i in team[0]:
            for k in team[1]:
                if k in g[i] and k not in team[0]:
                    g1[s] = []
                    if [team[0],team[1]] not in g1.values():
                        g1[s].append(team[0])
                        g1[s].append(team[1])
                    s = s+1
    team1 = []
    team2= []
    for key in list(g1):
        if g1[key] == []:
            del g1[key]
    #print("g1 without empty lists:", g1)
    DQmax= -100
    for key,value in g1.items():
        DQ = 0
        EJJ = 0
        EIJ = 0
        EII = 0
        ai=0
        aj=0
        EIJ = eij(value[0],value[1])
        EII = eii(value[0])
        EJJ = eii(value[1])
        ai = EIJ + EII
        aj = EIJ + EJJ
        DQ = 2*(EIJ - ai*aj)
        if DQ > DQmax :
            DQmax = DQ
            team1 = value[0]
            team2 = value[1]
    for element in team1:
        if element not in elements:
            elements.append(element)
    for element in team2:
        if element not in elements:
            #print("element:",element)
            elements.append(element)
    #print ("This is DQ max", DQmax," for the team: ",team1," and the team: ", team2)
    #print("This is the element list:", elements)
    #print("this is team_list:",team_list)
    team_list.append(elements)
    team_list.remove(team1)
    team_list.remove(team2)
    for key in list(g1):
        del g1[key]

    Q = Q + DQmax


for team in team_list:
    EII = eii(team)
    print(sorted(team))
print("Q = ",round(Q,4))
