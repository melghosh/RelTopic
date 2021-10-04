#  Copyright (c) 2021. Mirna El Ghosh (ASTURIAS Project) version 1.0
#   ------------------------------------
#   Status: This code is a beta version.
#   ------------------------------------
#   >>>>>>> The software is under improvement <<<<<<<.
#
#

from owlready2 import *
import pandas as pd

class TopicOnto(object):
    """this class implements topic ontologies.
    The named entities are added to the ontology as instances (based on the csv files obtained from AssignInstances.py).

    """

    def __init__(self, src,file):

      self.onto = owlready2.get_ontology(src).load()
      self.classes = [s for s in self.onto.classes()]
      self.classeslist=list(self.onto.classes())
      self.ontology=self.onto
      rootiri = 'http://www.co-ode.org/ontologies/ont.owl#Root'
      root = self.ontology.search_one(iri=rootiri)
      self._root = root
      self.objectpropertieslist=list(self.onto.object_properties())
      self.instanceofclasses=self.assignInstances(file)
      self.instanceslist=self.getNonRepeatedInstances()


    def clearInstances(self):
        listclasses=self.classes;
        for c in listclasses:
            for i in c.instances():
             destroy_entity(i)

    def getInstances(self,c):
        list=c.instances()
        return list

    def assignInstances(self,file):
        self.clearInstances()
        ziplist=self.getEdgesInstances(file)
        itemtoplist=[]
        instancelist=[]


        for r in ziplist:
            instancestr=r[1]
            top = r[0]
            iri1='http://www.wikidata.org/entity/'+top+''

            i=self.ontology.search_one(iri=iri1)
            iri2=i.iri

            if(instancelist.__contains__(instancestr)!=True):
             instancelist.append(instancestr)

             i(instancestr)
            else:
                instancelist.append(instancestr)
                instanceiri = 'http://www.wikidata.org/entity/' + instancestr + ''
                instance = self.ontology.search_one(iri=instanceiri)
                instance.is_a.append(i)

            if(itemtoplist.__contains__(i)!=True):
             itemtoplist.append(i)

        return itemtoplist


    def getNonRepeatedInstances(self):
        listinstances=[]
        for c in self.instanceofclasses:

            for i in self.getInstances(c):
                if(listinstances.__contains__(i)!=True):
                 listinstances.append(i)

        return listinstances



    def getEdgesInstances(self,file):
        colnames = ['instance', 'topic']

        data = pd.read_csv(file, names=colnames)
        instances = data.instance.tolist()
        instances.pop(0)
        topics = data.topic.tolist()
        topics.pop(0)
        ziplist = list(zip(topics, instances))

        return ziplist


    def addInstances(self):
        colnames = ['instance', 'topic']
        data = pd.read_csv('instance.csv', names=colnames)
        instances = data.instance.tolist()
        instances.pop(0)
        topics=data.topic.tolist()
        topics.pop(0)

        ziplist=zip(topics, instances)

        for r in ziplist:
            instancestr=f'"{r[1]}"'
            top=r[0]
            itemtop=self.onto.__getitem__(top)
            itemtop(instancestr)

    def getInstances(self, c):
        return c.instances()

    def is_a(self,c):
        return c.is_a

    def ancestorsOf(self,c):
        return c.ancestors()

    def subClassesOf(self,c):
        return list(c.subclasses())

    def allSubclassesOf(self,c, all=[]):

        for sub in self.subClassesOf(c):
            all.append(sub)
            self.allSubclassesOf(sub)

        return all

    def siblings(self,c):
        sib=[]
        for parent in self.is_a(c):
            for child in self.subClassesOf(parent):
                if child != c:
                    sib.append(child)

        return sib

    def domainOP(self,p):

        return  p.domain

    def rangeOP(self,p):

        return p.range


    def objectProperty(self,c):
        op = []
        for o in self.objectproperties:
            for d in o.domain:
                if d== c:
                    op.append(o)
            for r in o.range:
                if r == c:
                    op.append(o)
        return op

    def labelClassOf(self,c):
       return c.label

    def wikidataID(self,c):
        return c.Wikidata_id
