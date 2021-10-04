#  Copyright (c) 2021. Mirna El Ghosh (ASTURIAS Project) version 1.0
#   ------------------------------------
#   Status: This code is a beta version.
#   ------------------------------------
#   >>>>>>> The software is under improvement <<<<<<<.
#


import csv
import xml.etree.ElementTree as ET
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

class AssignInstances:
  """This class implements the assignment of the named entities, collected from the articles, as instances.
  1- input: an xml file, representing each article, that contains the named entities collected from the article
            and disambiguated using Wikidata uris.
  2- output: a csv file that contains the named entities (instances) and their hypernyms classes based on Wikidata.
             these classes are considered "most specific classes" and will be used later to build the ontology.
  """


  g1 = 'Data-Articles/xml/articles.csv'
  colname = ['article']
  data = pd.read_csv(g1, names=colname)
  articles = data.article.tolist()
  articles.pop(0)
  for a in articles:

    root = ET.parse('Data-Articles/xml/'+a+'.xml').getroot()
    results=[]
    #print(root.get('year'))
    for ne in root.findall('NE'):
        if((ne.get('type')=='person' or ne.get('type')=='organization' or ne.get('type')=='product' or ne.get('type')=='divers')and ne.get('uri')!=""):
          uri=ne.get('uri')
          #print(uri)
          lengthuri = len(uri)
          prefixlength = 27
          entityid = uri[27:lengthuri]
          print(entityid)

          if (ne.get('type') == 'person'):
              sparql = SPARQLWrapper("https://query.wikidata.org/sparql",
                                     agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')

              sparql_query = """

                           SELECT ?linkedclass 
                    WHERE
                    {
                      wd:""" + entityid + """  wdt:P106 ?linkedclass.

                      # both occupations in one line
                      SERVICE wikibase:label { bd:serviceParam wikibase:language "[en]". }
                    }  """
              # res = return_sparql_query_results(sparql_query)
              sparql.setQuery(sparql_query)
              sparql.setReturnFormat(JSON)

              res = sparql.query().convert()
              res2 = res['results']['bindings']
             # print(res)
              for x in res2:
                  #print(x['linkedclass']['value'])
                  valueid = x['linkedclass']['value']
                  lengthss = len(valueid)
                  valuesp = valueid[31:lengthss]
                  print('Article -'+ a +'-instance of:',valuesp)
                  results.append((entityid,valuesp))
          else:
              sparql = SPARQLWrapper("https://query.wikidata.org/sparql",
                                     agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')

              sparql_query = """

                                         SELECT ?linkedclass 
                                  WHERE
                                  {
                                    wd:""" + entityid + """  wdt:P31 ?linkedclass.

                                    # both occupations in one line
                                    SERVICE wikibase:label { bd:serviceParam wikibase:language "[en]". }
                                  }  """
              # res = return_sparql_query_results(sparql_query)
              sparql.setQuery(sparql_query)
              sparql.setReturnFormat(JSON)

              res = sparql.query().convert()
              res2 = res['results']['bindings']
              for x in res2:
                  valueid = x['linkedclass']['value']
                  lengthss = len(valueid)
                  valuesp = valueid[31:lengthss]
                  print('Article -'+ a + '-instance of:',valuesp)
                  results.append((entityid,valuesp))


    with open('Data-Articles/csv/'+a+'.csv', mode='w',newline='') as csv_file:
     fieldnames = ['instance', 'topic']
     writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

     writer.writeheader()
     for r in results:
       writer.writerow({'instance': r[0], 'topic': r[1]})







