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

import csv
from collections import Counter
import numpy as np
import pandas as pd
from SPARQLWrapper import JSON, SPARQLWrapper
import TopicOntology
import OntologyDirectedGraph


class TopicLabeling:

 """This class implements the topic pabeling process of articles.
    input: list of articles (csv).
    output: list of topics associated for each article.
  """

 def getLabel(c1):
     c11 = c1.strip('"')

     sparql = SPARQLWrapper("https://query.wikidata.org/sparql",
                            agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')

     sparql_query = """
                                      SELECT ?topic ?topicLabel
                               WHERE
                               {
                                 wd:""" + c11 + """  rdfs:label ?topicLabel.
                                 SERVICE wikibase:label { bd:serviceParam wikibase:language "[en]". }
                               }  """
     # res = return_sparql_query_results(sparql_query)
     sparql.setQuery(sparql_query)
     sparql.setReturnFormat(JSON)

     res = sparql.query().convert()
     res2 = res['results']['bindings']
     # print(res2)
     valueid = ""
     for x in res2:
         if (x['topicLabel']['xml:lang'] == 'en'):
             # print(x['linkedclass']['value'])
             valueid = x['topicLabel']['value']
     return valueid

 def getid(self, entity):

     str = f"'{entity}'"
     lengttopic = len(str)
     entityid = str[8:lengttopic - 1]

     return entityid

 def isSubclassOf(c1, c2):
     c11 = c1.strip('"')
     c22 = c2.strip('"')

     sparql = SPARQLWrapper("https://query.wikidata.org/sparql",
                            agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')

     sparql_query = """
                                 SELECT ?superclass
                          WHERE
                          {
                            wd:""" + c11 + """  wdt:P279* ?superclass.
                            # both occupations in one line
                            SERVICE wikibase:label { bd:serviceParam wikibase:language "[en]". }
                          }  """
     # res = return_sparql_query_results(sparql_query)
     sparql.setQuery(sparql_query)
     sparql.setReturnFormat(JSON)

     res = sparql.query().convert()
     res2 = res['results']['bindings']
     for x in res2:
         # print(x['linkedclass']['value'])
         valueid = x['superclass']['value']
         lengthss = len(valueid)
         valuesp = valueid[31:lengthss]
         if (c2 == valuesp):
             return True
     return False

 def allhyper(c1):
     c11 = c1.strip('"')

     sparql = SPARQLWrapper("https://query.wikidata.org/sparql",
                            agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')

     sparql_query = """
                                 SELECT ?superclass
                          WHERE
                          {
                            wd:""" + c11 + """  wdt:P279* ?superclass.
                            # both occupations in one line
                            SERVICE wikibase:label { bd:serviceParam wikibase:language "[en]". }
                          }  """
     # res = return_sparql_query_results(sparql_query)
     sparql.setQuery(sparql_query)
     sparql.setReturnFormat(JSON)

     res = sparql.query().convert()
     res2 = res['results']['bindings']
     listid = []
     for x in res2:
         # print(x['linkedclass']['value'])
         valueid = x['superclass']['value']
         lengthss = len(valueid)
         valuesp = valueid[31:lengthss]
         listid.append(valuesp)

     return listid

 #problem in A_23 (instance:Q6063)
 g1='Data-Articles/recent-press/csv/articles.csv'
 colname = ['article']
 data = pd.read_csv(g1, names=colname)
 articles = data.article.tolist()
 articles.pop(0)
 resultsLabeling = []

 for a in articles:
  topicsa=[]
  listSpecificTopics=[]
  arrayoftopics=[]
  arrayoftopicslabel=[]

 # for each article get the instances and specific topic concepts
  print('----------------')
  print("Article: "+a)
  file="Data-Articles/recent-press/csv/"+a+".csv"
  colnames = ['instance', 'topic']
  data = pd.read_csv(file, names=colnames)
  topics = data.topic.tolist()
  topics.pop(0)
  instances = data.instance.tolist()
  instances.pop(0)
  nonrepeatinstances=[]
  for i in instances:
      if nonrepeatinstances.__contains__(i)!=True:
          nonrepeatinstances.append(i)

  #load he ontology with the instances
  onto2=TopicOntology.TopicOnto("ontology/Topic-RPA.owl",file)
  print('test')
  og = OntologyDirectedGraph.TopicOntologyToGraph(onto2)
  tax = OntologyDirectedGraph.DiGraph(og)
  alltopics=onto2.classeslist

  #the list of specific topics
  for t in topics:
      tiri='http://www.wikidata.org/entity/'+t+''
      tx=onto2.ontology.search_one(iri=tiri)
      if (listSpecificTopics.__contains__(tx) ==False):
          listSpecificTopics.append(tx)


  #for each article there is a list of results
  results=[]

  #calculate the average of depths in the ontology
  rootiri = 'http://www.co-ode.org/ontologies/ont.owl#Root'
  rootx = onto2.ontology.search_one(iri=rootiri)
  listdepthx = []
  for c in onto2.classes:
      if (tax.has_path(c, rootx)==True):
          listdepthx.append(tax.shortest_path_length(c, rootx))
  avgdepth = round(np.mean(listdepthx),0)
  print('Average of depth=', avgdepth)

#INSTANCE-TOPIC Mapping
#calculate the RelTopic among the instances and the topics of Topic-OPA
  for x in onto2.getNonRepeatedInstances():

      for c in alltopics:
         relatedness=tax.semRelTopicMeasure(x, c, 'weight')
         if(relatedness>0 and c!=rootx):
           results.append((x,c,relatedness))

  #calculate the average of relatedness values for all the topic concepts and the instances
  resultsavg=[]
  avg=0
  for r in results:
    resultsavg.append(r[2])
  avg=np.round(np.mean(resultsavg),2)

  print('Average of relatedness values for all the instances, avg=',avg,'')

#select the topics which the value of relatedness values are above the threshold
# here two values of threshold are proposed:
# 1- if Topic-OPA ia curated: threshold=average of relatedness values
# 2- if Topic-OPA not curated: average of relatedness values if very low (around 0.27); thus, threshold is shifted
# using logarithm function (threshold=np.round(-np.log10(avg),2)).


  # uncomment threshold= avg if the topic ontology Topic-OPA is curated.
  #threshold=avg

  # shift the threshold value using logarithm
  threshold=np.round(-np.log10(avg),2)


  print('threshold=',threshold)

  relatedtopics=[]
  for r in results:
     if (r[2]>=threshold):
      r2str=f'"{r[1]}"'
      lengthr2=len(r2str)
      r2x=r2str[8:lengthr2]
      r2label=getLabel(r2x)
      #print('mean results: ',r[0],r2label,r[2])
      relatedtopics.append(r[1])

     # 4-compute the most common topics
  commontopic = Counter(relatedtopics).most_common()
  print('common topics:', commontopic)

  #RANKING AND SELECTION PROCESS
#1-eliminate the abstract concepts
  commontopic2=[]
  for t in commontopic:

     level=tax.shortest_path_length(t[0],rootx)
     if(level>=avgdepth):
        if(commontopic2.__contains__(t)==False):
         commontopic2.append(t)

#2-eliminate the concepts that are hypernyms of the instances
  commontopic3=[]
  for t in commontopic2:
    if(listSpecificTopics.__contains__(t[0])==False):
     if (commontopic3.__contains__(t) == False):
       commontopic3.append(t)

  commontopic4 = []
  for t in commontopic3:
      for i in listSpecificTopics:
       istr = f"'{i}'"
       ilengttopic = len(istr)
       ientityid = istr[8:ilengttopic - 1]

      hyper=allhyper(ientityid)
      tstr = f"'{t[0]}'"
      tlengttopic = len(tstr)
      tentityid = tstr[8:ilengttopic - 1]
      if (hyper.__contains__(tentityid)==False):
            if (commontopic4.__contains__(t) == False):
             commontopic4.append(t)

#eliminate the topic concepts that are hyponyms of person, organization, product and location
  piri = 'http://www.wikidata.org/entity/Q215627'
  person = onto2.ontology.search_one(iri=piri)
  pstr = f"'{person}'"
  plengttopic = len(pstr)
  pentityid = pstr[8:plengttopic - 1]

  oiri = 'http://www.wikidata.org/entity/Q43229'
  organization = onto2.ontology.search_one(iri=oiri)
  ostr = f"'{organization}'"
  olengttopic = len(ostr)
  oentityid = ostr[8:olengttopic - 1]

  priri = 'http://www.wikidata.org/entity/Q15401930'
  product = onto2.ontology.search_one(iri=priri)
  prstr = f"'{product}'"
  prlengttopic = len(prstr)
  prentityid = prstr[8:prlengttopic - 1]

  liri = 'http://www.wikidata.org/entity/Q17334923'
  location = onto2.ontology.search_one(iri=liri)
  lstr = f"'{location}'"
  llengttopic = len(lstr)
  lentityid = lstr[8:llengttopic - 1]

  commontopic5 = []
  for t in commontopic4:
      str = f"'{t[0]}'"
      lengttopic = len(str)
      entityid = str[8:lengttopic - 1]
      hyper = allhyper(entityid)
      if (hyper.__contains__(pentityid) == False and hyper.__contains__(oentityid) == False and hyper.__contains__(prentityid) == False and hyper.__contains__(lentityid) == False):
          if (commontopic5.__contains__(t) == False):
              commontopic5.append(t)


  listcounter=[]
  listtopicfinal=[]
  listdegree = []
  listdegree2 = []
  listavgdegree = []

#compute the most common topic concepts
  for c in commontopic5:
   listcounter.append(c[1])
  maxx=max(listcounter)
  for c in commontopic5:
   if (c[1]==maxx):
     listtopicfinal.append(c[0])


#5-compute the size of listtopicfinal
  if(listtopicfinal.__len__()==1):
      print('---->Unique Topic labeling is: ',listtopicfinal[0])
      str = f"'{listtopicfinal[0]}'"
      lengttopic = len(str)
      prefixlength = 64
      entityid = str[8:lengttopic - 1]
      # print('entityid',entityid)
      if (arrayoftopics.__contains__(entityid) != True):
          arrayoftopics.append(entityid)
      itemtop = onto2.ontology.__getitem__(entityid)

      if (topicsa.__contains__(itemtop) != True):
          topicsa.append(itemtop)


  else:
   #calculate the average of relatedness for all the related topic concepts
   listavgtopics = []
   listavgtopics2 =[]
   for t in listtopicfinal:
      listavgtopics1 = []
      for r in results:
          if (t == r[1]):
              listavgtopics1.append(r[2])
      avgtopic = np.mean(listavgtopics1)
      #print(avgtopic,t)

     #eliminate the topics which their average of relatedness is less than the threshold
      if(avgtopic>=threshold):
       listavgtopics.append((t, avgtopic))
      else:
          listavgtopics2.append((t,avgtopic))


  #6-select the topic with the maximum average of relatedness
   listavg=[]
   print('length: ',len(listavgtopics))

   if(len(listavgtopics)==0):
       for l in listavgtopics2:
           #degree = tax.degreeofconcept(l[0])
           degree=l[1]
           listdegree.append(degree)
           listdegree2.append((l[0], degree))
       maxd = max(listdegree)

       for l in listdegree2:
           print(l)
           if (l[1] == maxd):
               print("--->Relatedness-Guided Topic labeling of " + a + " is:", l[0])
               str = f"'{l[0]}'"
               lengttopic = len(str)
               entityid = str[8:lengttopic - 1]

               if (arrayoftopics.__contains__(entityid) != True):
                   arrayoftopics.append(entityid)
               itemtop = onto2.ontology.__getitem__(entityid)

               if (topicsa.__contains__(itemtop) != True):
                   topicsa.append(itemtop)

   if(len(listavgtopics)>0):
    for l in listavgtopics:
     listavg.append(l[1])
     print(l[0],l[1])
    maxavg=max(listavg)

    for l in listavgtopics:
     if(l[1]==maxavg):
      print('--->Relatedness-Guided Topic Labeling of '+a+' is: ',l[0])
      str=f"'{l[0]}'"
      lengttopic = len(str)
      prefixlength = 64
      entityid = str[8:lengttopic-1]
      if(arrayoftopics.__contains__(entityid)!=True):
          arrayoftopics.append(entityid)
      itemtop = onto2.ontology.__getitem__(entityid)

      if(topicsa.__contains__(itemtop)!=True):
       topicsa.append(itemtop)


   for l in listavgtopics:
      degree= tax.degreeofconcept(l[0])
      listdegree.append(degree)
      listdegree2.append((l[0],degree))


   if(listdegree.__len__()==0):
       print('test: ',listavgtopics2)
       for l in listavgtopics2:
        str = f"'{l[0]}'"
        lengttopic = len(str)
        entityid = str[8:lengttopic - 1]


        if (arrayoftopics.__contains__(entityid) != True):
           arrayoftopics.append(entityid)
        itemtop = onto2.ontology.__getitem__(entityid)

        if (topicsa.__contains__(itemtop) != True):
           topicsa.append(itemtop)

   else:
    maxd=max(listdegree)


    for l in listdegree2:
     print(l)
     if(l[1]==maxd):
        print("--->Centrality-Guided Topic labeling of " + a + " is:", l[0])
        str = f"'{l[0]}'"
        lengttopic = len(str)
        entityid = str[8:lengttopic - 1]


        if (arrayoftopics.__contains__(entityid) != True):
            arrayoftopics.append(entityid)
        itemtop = onto2.ontology.__getitem__(entityid)

        if (topicsa.__contains__(itemtop) != True):
            topicsa.append(itemtop)

  for at in arrayoftopics:
      arrayoftopicslabel.append(getLabel(at))
  resultsLabeling.append((a,arrayoftopics,arrayoftopicslabel))

 with open('labeling-results/csv/results-Topic-Labeling-Test.csv', mode='w', newline='') as csv_file:
    fieldnames = ['Article', 'Topic-WikidataID', 'Topic-Label']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    for r in resultsLabeling:
        article=r[0]
        topicid=r[1]
        topiclabel=r[2]

        writer.writerow({'Article': article, 'Topic-WikidataID':topicid, 'Topic-Label':topiclabel})