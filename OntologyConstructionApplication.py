#  Copyright (c) 2021. Mirna El Ghosh (ASTURIAS Project) version 1.0
#   ------------------------------------
#   Status: This code is a beta version.
#   ------------------------------------
#   >>>>>>> The software is under improvement <<<<<<<.
#
#

import rdflib
from rdflib import URIRef
from rdflib.namespace import OWL, RDF
import OntologyConstruction
import pandas as pd
import time



class OntologyConstructionApplication:
   """this class implements the application of ontology construction in Le Matin:
       1- inputs (most specific classes) are csv files located in Data-Articles/csv repository.
       2- output: OWL ontology.
       """

   listSpecificTopics = []
   ax = 'Data-Articles/csv/articles.csv'
   colname = ['article']
   data = pd.read_csv(ax, names=colname)
   articles = data.article.tolist()
   articles.pop(0)
   for a in articles:
      file = "Data-Articles/csv/" + a + ".csv"
      colnames = ['instance', 'topic']
      data = pd.read_csv(file, names=colnames)
      topics = data.topic.tolist()
      topics.pop(0)
      for t in topics:
          if(listSpecificTopics.__contains__(t)!=True):
           listSpecificTopics.append(t)


   onto=OntologyConstruction.OntologyConstruction()


   listclasses = []
   listtriples=[]
   listtriples3=[]
   listtriples5=[]

   listtest2=[]
   listtest3=[]




   label=''
   uri=''
   uri2=''
   listtest = []
   glist=[]

   print('Most specific concepts:')
   for t in listSpecificTopics:
       time.sleep(7)


       uri='http://www.wikidata.org/entity/'+t;
       labelo=onto.getLabel(uri)
       print(labelo,"-",uri)

       resp = onto.sparqltripleslevel2(t)
       for re in resp:
           if (listtest.__contains__(re) != True):
               listtest.append(re)

               if (listtriples.__contains__(re) != True):

                   s = re['subject']['value']
                   slabel = onto.getLabel(s)
                   o = re['object']['value']
                   p = re['predicate']['value']
                   o1 = ''

                   p1 = ''
                   if (p == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'):
                       p1 = ' AS '
                   if (p == 'http://www.w3.org/2000/01/rdf-schema#subclassOf'):
                       p1 = ' subClassOf '
                   if (p == 'http://www.w3.org/2000/01/rdf-schema#label'):
                       p1 = ' label '
                   msg = ""
                   oid  = onto.getid(o)
                   if (oid.startswith('Q')):
                       olabel = onto.getLabel(o)
                       msg = "Add /" + s + "(" + slabel + ")/ -> " + p1 + " -> " + olabel + " ?"
                   else:
                       if (o == 'http://www.w3.org/2002/07/owl#Class'):
                           msg = "Add /" + s + "(" + slabel + ")/ -> " + p1 + " ->  Class  ?"
                       else:
                           msg = "Add /" + s + "(" + slabel + ")/ -> " + p1 + " -> " + o + " ?"


                   listtriples.append(re)
                   print(msg)




   g = rdflib.ConjunctiveGraph()

   g1 = onto.parsetripleshierarchical(listtriples, g)  # all the triples of all requests to be added to graph

   listc3 = onto.getAllClasses(g1)
   nb = listc3.__len__()
   print(nb, " topic concepts are added to the hierarchical scheme of the ontology")
   print("CONSTRUCT the non-hierarchical scheme of the ontology")

       # get all the ids of the concepts from graph g, construct triples, then parse triples
   for c in listc3:
          print(c)


          if(str(c).startswith('Q')):
           resp3 = onto.sparqltriplesnonhierarchical(c)

           time.sleep(7)

           for re3 in resp3:
               if (listtest2.__contains__(re3) != True):
                   listtest2.append(re3)
                   if (listtriples3.__contains__(re3) != True):
                       s = re3['subject']['value']
                       slabel = onto.getLabel(s)
                       o = re3['object']['value']
                       p = re3['predicate']['value']
                       # print(s,p,o)
                       pid = onto.getpid(p)
                       oid = onto.getid(o)


                       if (pid.startswith('P') and oid.startswith('Q')):
                           plabel = onto.getPropLabel(p)
                           olabel = onto.getLabel(o)

                           msg = "Add /" + s + "(" + slabel + ")/-> " + plabel + "-> " + olabel + " ? "



                       listtriples3.append(re3)

       # print("length of all triples added non hierarchical:", listtriples3.__len__())

   g2=rdflib.ConjunctiveGraph()
   g3 = onto.parsetriplesnonhierarchical(listtriples3, g2)  # all the triples of all requests to be added to graph
       # print("Find new concepts that don't exist in the hierarchical scheme")
   listx = onto.getClassesNotExist(listtriples3, g1)
   print("New topics to add to the ontology:", listx.__len__())

   print("ENRICH the ontology with new topics")
   g4=rdflib.ConjunctiveGraph()

   for x in listx:
     # print('test',x)
      xstr=f'"{x}"'
      print(xstr)
      if(x.startswith('Q')):
       print("newclass: ", x)
       resp = onto.sparqltripleslevel2(x)
       # print(resp)
       for re in resp:
           if (listtest.__contains__(re) != True):
               listtest.append(re)

               if (listtriples.__contains__(re) != True and listtriples5.__contains__(re) != True):

                   s = re['subject']['value']
                   slabel = onto.getLabel(s)
                   o = re['object']['value']
                   p = re['predicate']['value']
                   o1 = ''

                   p1 = ''
                   if (p == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'):
                       p1 = ' AS '
                   if (p == 'http://www.w3.org/2000/01/rdf-schema#subclassOf'):
                       p1 = ' subClassOf '
                   if (p == 'http://www.w3.org/2000/01/rdf-schema#label'):
                       p1 = ' label '
                   msg = ""
                   oid = onto.getid(o)
                   if (oid.startswith('Q')):
                       olabel = onto.getLabel(o)
                       msg = "Add /" + s + "(" + slabel + ")/ -> " + p1 + " -> " + olabel + " ?"
                   else:
                       if (o == 'http://www.w3.org/2002/07/owl#Class'):
                           msg = "Add /" + s + "(" + slabel + ")/ -> " + p1 + " ->  Class  ?"
                       else:
                           msg = "Add /" + s + "(" + slabel + ")/ -> " + p1 + " -> " + o + " ?"


                   listtriples5.append(re)


   g5 = onto.parsetripleshierarchical(listtriples5, g4)  # all the triples of all requests to be added to graph

   g6=g3+g1+g5

  # g6.add((URIRef('https://asturias/topic-opa.owl'), RDF.type, OWL.Ontology))

   g6.serialize(destination='ontology/Topic-OPA-2021.owl', format='xml')





