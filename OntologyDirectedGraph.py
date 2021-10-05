#  Copyright (c) 2021. The ASTURIAS Project.
#   ---------------------------------------------------
#   Version: 1.0.1
#   Contributor: Mirna El Ghosh.
#   Status: Beta version.
#   ---------------------------------------------------
#
#
#
#
#

import math
import numpy as np
from abc import abstractmethod, ABCMeta
import networkx as nx

class OntologyToGraph:

    __metaclass__ = ABCMeta

    @abstractmethod
    def convert(self):
        pass

#This class converts the topic ontology into graph of nodes, edges, and cross-references.
class TopicOntologyToGraph(OntologyToGraph):

    def __init__(self,onto):
     self.ontology= onto
     self._root=self.ontology._root


    def convert(self):
        nodes = { n for n in self.ontology.classeslist}
        instances= list(self.ontology.instanceslist)
        op={o for o in self.ontology.objectpropertieslist}
        edges = []
        for i, node in enumerate(nodes):
            subclasses = self.ontology.subClassesOf(node)
            subclasses = [child for child in subclasses if child in nodes]
            for child in subclasses:
                edges.append((node, child))
        for x in instances:
            nodes.add(x)
        listinstanceofclasses=self.ontology.instanceofclasses
        for x in listinstanceofclasses:
           instance=self.ontology.getInstances(x)
           for i in instance:
            edges.append((x,i))
        crossref = []
        for o in op:
            domainlist = (self.ontology.domainOP(o))
            rangelist= (self.ontology.rangeOP(o))
            domain = [d for d in domainlist]
            range= [r for r in rangelist]
            for d in domain:
                for r in range:
                  crossref.append((d, r))
        return nodes, edges, crossref


class DiGraph(object):
    """This class builds the ontology weighted graph based on the nodes and edges transformed
       from the ontology concepts and relations.
       The ontology graph will be used to compute the semantic relatedness between the (assigned) instances
       and the concept nodes.
       In this class, we define our semantic relatedness measure RelTopic that considers the assessment
       of semantic relatedness between instances and concepts nodes.
        """

    def __init__(self, onto):
        self.nodes, self.edges, self.crossref = onto.convert()
        self._root=onto._root
        self.digraph = nx.DiGraph()
        self.subclasses = {}
        self.superclasses = {}
        self.build_weighted_graph(onto)

    def build_weighted_graph(self, onto):

            hypernyms, subclasses = zip(*self.edges)
            #domains, ranges = zip(*self.crossref)
            hypernyms_set = set(hypernyms)
            subclasses_set = set(subclasses)
            not_subclasses = []
            not_hypernyms = []

            for p in hypernyms_set:
                if p not in subclasses:
                    not_subclasses.append(p)

            for p in subclasses_set:
                if p not in hypernyms_set:
                    not_hypernyms.append(p)
            self.digraph.add_nodes_from(self.nodes)

            for hypernym, hyponym in self.edges:

                if(hypernym==self._root):
                 self.digraph.add_edge(hyponym, hypernym, weight=1)
                else:
                    self.digraph.add_edge(hyponym, hypernym, weight=1)

            for d, r in self.crossref:

                self.digraph.add_edge(d, r, weight=0.25)

            for hypernym, hyponym in self.edges:
                self.subclasses.setdefault(hypernym, []).append(hyponym)

            for hypernym, hyponym in self.edges:
                self.superclasses.setdefault(hyponym, []).append(hypernym)


    def root_subclass(self):
        return self.hyponyms(self._root)

    def isReachable(self,tax,c1,c2):
        if(nx.algorithms.tournament.is_reachable(tax, c1, c2)):
            return True

        return False

    def todirected(self):

        return self.digraph.to_directed()

    def is_directed_acyclic(self):

        return nx.is_directed_acyclic_graph(self.digraph)

    def is_directed(self):
        return self.digraph.is_directed()

    def hyponyms(self, node):
        return self.subclasses[node] if node in self.subclasses else []

    def hypernyms(self, node):
        return self.superclasses[node] if node in self.superclasses else []

    def shortest_path_length(self, node1, node2):
        length=0
        if(nx.has_path(self.digraph, node1,node2)):

         length= (nx.shortest_path_length(self.digraph, node1, node2))
        return length

    def shortest_path(self, node1, node2):
        return nx.shortest_path(self.digraph, node1, node2)


    def getneighbours(self, c):
        listn=self.digraph.neighbors(c)

        return list(listn)

#calculate the degree centrality of node c
    def degreeofconcept(self,c):
        listn=self.getneighbours(c)
        sum=0

        for l in listn:
            wn=self.weightnode(l)
            we=self.get_edge_data(c,l)
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
        totalnodes=self.digraph.nodes.__len__()

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


    def superclassof(self,x,y):

        path = nx.dijkstra_path(self.digraph, x, y)
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
        a=nx.ancestors(self.digraph,c)

        return a

    def isancestor(self,c1,c2):
        a=nx.ancestors(self.digraph,c2)
        for x in a:
            if (x==c1):
                return True

        return False


    def ancestors(self,c):
        return list(nx.ancestors(self.digraph,c))


    def has_path(self,x,y):
        return(nx.has_path(self.digraph,x,y))

    #computation of the semantic relatedness measure RelTopic
    def semRelTopicMeasure(self, c1,c2, weight):

         k=0
         relatedness=0

         #consider c1 as instance and c2 as topic concept
         if (nx.has_path(self.digraph,c1,c2) ):
             dijkstrapathlength = nx.dijkstra_path_length(self.digraph, c1, c2, weight)
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
            path = nx.dijkstra_path(self.digraph, x, y)
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
        if(nx.has_path(self.digraph,c1,c2)):
         rel=8-self.shortest_path_length(c1, c2)- self.turns(c1,c2)

        else:
            rel=0

        return rel

    def simRadaTaxonomy(self, c1, c2):
        """ Rada's shortest path """
        if(nx.has_path(self.digraph,c1,c2)):
         path=1 / (1+self.shortest_path_length(c1, c2))
        else:
            path=0

        return path

    def get_edge_data(self, c1,c2):
        return self.digraph.get_edge_data(c1,c2)

    def is_multigraph(self):
        return self.digraph.is_multigraph()

