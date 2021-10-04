#  Copyright (c) 2021. Mirna El Ghosh (ASTURIAS Project) version 1.0
#   ------------------------------------
#   Status: This code is a beta version.
#   ------------------------------------
#   >>>>>>> The software is under improvement <<<<<<<.
#
#

import math
import numpy as np
from abc import abstractmethod, ABCMeta
import networkx as nx

class OntologyTransform:

    __metaclass__ = ABCMeta

    @abstractmethod
    def transform(self):
        """return nodes, labels, and edges (taxonomic and cross-references)"""
        pass


class TopicOntologyTransform(OntologyTransform):

    """This class transforms owl ontology into graph: nodes, edges and cross-references.
          """


    def __init__(self,onto):
     self.ontology= onto
     self._root=self.ontology._root


    def transform(self):
        nodes = { n for n in self.ontology.listclass}
        #print(nodes)
        instances= list(self.ontology.instanceslist)
        op={o for o in self.ontology.objectproperties}
        #print('op: ',op)
        node_id = {n: i for i, n in enumerate(nodes)}
        labels = tuple([self.ontology.labelClassOf(value) for i, value in enumerate(self.ontology.listclass)])

        edges = []
        for i, node in enumerate(nodes):
            children = self.ontology.subClassesOf(node)
            children = [child for child in children if child in nodes]
            for child in children:
                edges.append((node, child))

        counter=0
        for x in instances:
            nodes.add(x)

        listinstanceofclasses=self.ontology.instanceofclasses
        for x in listinstanceofclasses:
           instance=self.ontology.getInstances(x)
           for i in instance:
            #print(i)
            edges.append((x,i))

        crossref = []
        for o in op:
            #print(o)
            domainlist = (self.ontology.domainOP(o))
            rangelist= (self.ontology.rangeOP(o))

            domain = [d for d in domainlist]
            range= [r for r in rangelist]
            for d in domain:
                for r in range:
                 # print(d,r)
                  crossref.append((d, r))


        return nodes, labels, edges, crossref


class Taxonomy(object):
    """This class buils the ontology graph (weighted and unweighted) based on the nodes and edges transformed
       from the ontology concepts and relations.
       The ontology graph will be used to compute the semantic relatedness between the (assigned) instances
       and the concept nodes.

       In this class, we define our semantic relatedness measure RelTopic that considers the assessment
       of semantic relatedness between instances and concepts nodes.
        """

    def __init__(self, onto):
        self._nodes, self._labels, self._edges, self._crossref = onto.transform()
        self._node2id = {value: i for i, value in enumerate(self._nodes)}
        #self._label2id = {value: i for i, value in enumerate(self._labels)}
        # virtual root
        self._root_id = len(self._nodes) + 1
        self._root=onto._root
        self._taxonomy = nx.DiGraph()
        self._hyponyms = {}
        self._hypernyms = {}

        self.build_weighted_graph(onto)

    def build_graph(self, onto):

        print("build graph")
        parents, children = zip(*self._edges)

        domains, ranges = zip(*self._crossref)
        parents_set = set(parents)
        children_set = set(children)
        not_children = []
        not_parent = []
        # nodes with no edges
        #for n in self._nodes:
         #   if n not in parents_set and n not in children_set:
          #      root_children.append(n)


        #find out those parents that are not appeared in children set

        for p in parents_set:
            if p not in children_set:
                not_children.append(p)

        # find out children that are not appeared in parent set
        for p in children_set:
            if p not in parents_set:
                not_parent.append(p)

        self._taxonomy.add_nodes_from(self._nodes)

        # add taxonomical edges
        for parent, child in self._edges:

            self._taxonomy.add_edge(child, parent)


        for d, r in self._crossref:
            print(d,r)

            self._taxonomy.add_edge(d,r)



        # hyponyms and hypernyms
        for parent, child in self._edges:
            self._hyponyms.setdefault(parent,[]).append(child)

        for parent, child in self._edges:
            self._hypernyms.setdefault(child, []).append(parent)


    def build_weighted_graph(self, onto):


            parents, children = zip(*self._edges)
            domains, ranges = zip(*self._crossref)
            parents_set = set(parents)
            children_set = set(children)

            not_children = []
            not_parent = []


            # find out those parents that are not appeared in children set

            for p in parents_set:
                if p not in children_set:
                    not_children.append(p)

            # find out children that are not appeared in parent set
            for p in children_set:
                if p not in parents_set:
                    not_parent.append(p)

            self._taxonomy.add_nodes_from(self._nodes)

            # add taxonomical edges
            #add weights to taxonomical edges depending on level
            for parent, child in self._edges:

                if(parent==self._root):
                 self._taxonomy.add_edge(child, parent, weight=1)
                else:
                    self._taxonomy.add_edge(child, parent, weight=1)

            for d, r in self._crossref:

                self._taxonomy.add_edge(d, r, weight=0.25)

            # hyponyms and hypernyms
            for parent, child in self._edges:
                self._hyponyms.setdefault(parent, []).append(child)

            for parent, child in self._edges:
                self._hypernyms.setdefault(child, []).append(parent)


    def root_children(self):
        return self.hyponyms(self._root)

    def isReachable(self,tax,c1,c2):
        if(nx.algorithms.tournament.is_reachable(tax, c1, c2)):
            return True

        return False

    def todirected(self):

        return self._taxonomy.to_directed()



    def is_directed_acyclic(self):

        return nx.is_directed_acyclic_graph(self._taxonomy)



    def is_directed(self):
        return self._taxonomy.is_directed()


    def hyponyms(self, node):
        return self._hyponyms[node] if node in self._hyponyms else []

    def hypernyms(self, node):
        return self._hypernyms[node] if node in self._hypernyms else []



    def shortest_path_length(self, node1, node2):
        length=0
        if(nx.has_path(self._taxonomy, node1,node2)):

         length= (nx.shortest_path_length(self._taxonomy, node1, node2))
        return length

    def shortest_path(self, node1, node2):
        return nx.shortest_path(self._taxonomy, node1, node2)

    def depth(self, node):
        return self.shortest_path_length(self._root, node)


    #get the neighbours of a node c
    def getneighbours(self, c):
        listn=self._taxonomy.neighbors(c)

        return list(listn)

#calculate the degree centrality of node c
    def degreeofconcept(self,c):
        listn=self.getneighbours(c)
        sum=0

        for l in listn:
            wn=self.weightnode(l)
            #print(wn)
            we=self.get_edge_data(c,l)
           # print(we["weight"])
            v=wn*we["weight"]
            sum+=v


        return sum

# calculate the degree centrality of node c
    def degreeofinstance(self, c):

        d = 0
        listdegreehyper = []
        hypernyms = self.hypernyms(c)
        if (hypernyms.__len__() == 1):
            d = self.degreeofconcept(hypernyms[0])
        else:
            for h in hypernyms:
                listdegreehyper.append(self.degreeofconcept(h))

            d = np.mean(listdegreehyper)

        return d


    #calculae the weight of node c1
    def weightnode(self,c1):
        weightofnode = 0

        nbofneighbours=self.getneighbours(c1).__len__()
        totalnodes=self._taxonomy.nodes.__len__()

        if(nbofneighbours==0):
            weightofnode=0
        else:
            weightofnode=-math.log((nbofneighbours)/(totalnodes))

        return weightofnode



#calculate the weight of an instance c1
    def weightnodeinstance(self,c1):
        weight=0
        listweighthyper=[]
        hypernyms=self.hypernyms(c1)
        if(hypernyms.__len__()==1):
            weight=self.weightnode(hypernyms[0])
        else:
            for h in hypernyms:
                listweighthyper.append(self.weightnode(h))

            weight = np.mean(listweighthyper)


        return weight


    #check if x is a superclass of y
    def superclassof(self,x,y):

        path = nx.dijkstra_path(self._taxonomy, x, y)
        i=0
        while(i<path.__len__()-1):
         nextnode=path.__getitem__(i+1)
         listhypernym=self.hypernyms(nextnode)
         node=path.__getitem__(i)
         for h in listhypernym:
             if h==node:
                 return True
         i=i+1

        return False


    def ancestors(self,c):
        a=nx.ancestors(self._taxonomy,c)

        return a

    def isancestor(self,c1,c2):
        a=nx.ancestors(self._taxonomy,c2)
        for x in a:
            if (x==c1):
                return True

        return False


    def ancestors(self,c):
        return list(nx.ancestors(self._taxonomy,c))


    def has_path(self,x,y):
        return(nx.has_path(self._taxonomy,x,y))



    #computation of the semantic relatedness measure RelTopic
    def semRelTopicMeasure(self, c1,c2, weight):

         k=0
         relatedness=0

         #consider c1 as instance and c2 as topic concept
         if (nx.has_path(self._taxonomy,c1,c2) ):
             dijkstrapathlength = nx.dijkstra_path_length(self._taxonomy, c1, c2, weight)
             #print('length of path',dijkstrapathlength)

             w1=self.weightnodeinstance(c1)
             w2 = self.weightnode(c2)
             d1 = self.degreeofinstance(c1)
             d2 = self.degreeofconcept(c2)

             if (self.superclassof(c1, c2) == True or dijkstrapathlength==0):
                 k = 0
                 #print('direction changed')

             else:
                 k = 1

             relatedness = (1 / ( 1+(dijkstrapathlength))) + k * (math.log((d1 + d2)) / (w1 + w2)) if dijkstrapathlength != 0 else 0

         else:
             relatedness=0


         return relatedness


    def turns(self, x, y):

            nbturns=0
            path = nx.dijkstra_path(self._taxonomy, x, y)
            i = 0
            while (i < path.__len__() - 1):
                nextnode = path.__getitem__(i + 1)
                listhypernym = self.hypernyms(nextnode)
                node = path.__getitem__(i)
                for h in listhypernym:
                    if h == node:
                        nbturns+=1
                i = i + 1

            return nbturns


    def relHS(self, c1, c2):
        """ Hirst and St-Onge’s measure """
        if(nx.has_path(self._taxonomy,c1,c2)):
         rel=8-self.shortest_path_length(c1, c2)- self.turns(c1,c2)

        else:
            rel=0

        return rel

    def simRadaTaxonomy(self, c1, c2):
        """ Rada's shortest path """
        if(nx.has_path(self._taxonomy,c1,c2)):
         path=1 / (1+self.shortest_path_length(c1, c2))
        else:
            path=0

        return path



    def get_edge_data(self, c1,c2):
        return self._taxonomy.get_edge_data(c1,c2)

    def is_multigraph(self):
        return self._taxonomy.is_multigraph()

