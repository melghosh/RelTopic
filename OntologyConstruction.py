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

import rdflib
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import RDFS, Literal, URIRef, RDF, BNode, OWL
from rdflib import Namespace


class OntologyConstruction(object):
    """this class implements three phases of the ontology construction:
    1- construct the hierarchical tructure based on most specific classes related to each article.
    2- construct the non-hierarchical structure based on the hierarchical.
    3- enrich the hierarchical structure with hierarchy of imported classes from the non-hierarchical structure.
    """

    #build the hierarchy based on the most specific classes
    def sparqltripleslevel2(self, entityid):
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql",
                               agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')

        sparql_query = """
CONSTRUCT {
  ?class a owl:Class . 
  ?class rdfs:subclassOf ?superclass . 
  ?superclass a owl:Class . 
  ?class rdfs:label ?classLabel . 
  ?property rdfs:domain ?class . 
  ?property rdfs:label ?classLabel .
}
WHERE {
 hint:Query hint:optimizer "None".
  BIND(wd:""" + entityid + """ AS ?mainClass) .    

  # Pick one or the other of the following two triple patterns. 
  #?class wdt:P31* ?mainClass.     # Find subclasses of the main class. 

  wd:""" + entityid + """ wdt:P279* ?class.     # Find superclasses of the main class. 

  ?class wdt:P279 ?superclass .     # So we can create rdfs:subClassOf triples
  ?class rdfs:label ?classLabel.

  #OPTIONAL {
   # ?class wdt:P31 ?property.
    #?property rdfs:label ?propertyLabel.
    #FILTER((LANG(?propertyLabel)) = "en")
    #}
  FILTER((LANG(?classLabel)) = "en")
}

"""
        sparql.setQuery(sparql_query)
        sparql.setReturnFormat(JSON)
        res = sparql.query().convert()
        res2 = res['results']['bindings']

        return res2

#return the new classes imported by the non-hierarchical relations and not found in the hiererachy
    def getClassesNotExist(self, tripleslist, g):

        listobject = []
        for tt in tripleslist:
            # for t in tt:
            s = tt['subject']['value']
            p = tt['predicate']['value']
            o = tt['object']['value']
            lengtho = len(o)
            if (lengtho > 31):
                ido = o[31:lengtho]
                listobject.append(ido)

        print("list of new objects in triples", listobject.__len__())
        print("list of new objects in triples", listobject)

        listo = self.getAllClasses(g)

        print("list of objects in g", listo.__len__())
        print("list of objects in g", listo)

        listc = list(set(listobject) - set(listo))
        print("difference", listc)

        return listc


    def getAllClasses(self, g):
        listc = []
        for s, p, o in g.triples((None, RDFS.subClassOf, None)):
            lengths = len(s)
            lengtho = len(o)

            ids = s[31:lengths]
            ido = o[31:lengtho]
            if (listc.__contains__(ids) != True):
                listc.append(ids)
            if (listc.__contains__(ido) != True):
                listc.append(ido)

        return listc

#this functions parse the hierarchical triples
    def parsetripleshierarchical(self, tripleslist, g):

        statementId = BNode()

        n = Namespace("http://asturias.com/topicopa/")
        u = "http://asturias.com/topicopa"
        super=[]
        listc=[]
        for tt in tripleslist:

            s = tt['subject']['value']
            p = tt['predicate']['value']
            o = tt['object']['value']

            if (p == 'http://www.w3.org/2000/01/rdf-schema#subclassOf'):


                g.add((rdflib.term.URIRef(u'' + s + ''), RDFS.subClassOf, rdflib.term.URIRef(u'' + o + '')))
                if(super.__contains__(s)==False):
                     super.append(s)


            if (p == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'):

                g.add((rdflib.term.URIRef(u'' + s + ''), RDF.type, rdflib.term.URIRef(u'' + o + '')))
                if(listc.__contains__(s)==False):
                    listc.append(s)

          #  if (p == 'http://www.w3.org/2000/01/rdf-schema#instanceOf'):

           #     g.add((rdflib.term.URIRef(u'' + s + ''), RDFS.instanceOf, rdflib.term.URIRef(u'' + o + '')))

            if (p == 'http://www.w3.org/2000/01/rdf-schema#label'):

                g.add((rdflib.term.URIRef(u'' + s + ''), RDFS.label, Literal(""+o)))



        print("length of graph", len(g))
        notclass=set(listc)-set(super)

        print(' not subclassesof: ', notclass.__len__())
        root = Namespace('http://www.co-ode.org/ontologies/ont.owl#')
        Root = URIRef(root["Root"])
        g.add((Root, RDF.type, OWL.Class))

        g.add((Root, RDFS.subClassOf, OWL.Thing))

        for s in notclass:
            print(s)
            g.add((rdflib.term.URIRef(u'' + s + ''), RDF.type, OWL.Class))

            g.add((rdflib.term.URIRef(u'' + s + ''), RDFS.subClassOf, Root))

        for ss, pp, oo in g:
            print("triplets added to graph", ss, pp, oo)

        return g


#this functions returns the non hierarchical triples based on the classes of the hierarchy
    def sparqltriplesnonhierarchical(self, entityid):
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql",
                               agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')

        # print("entity id entry: ",entityid)
        sparql_query = """
CONSTRUCT {
  ?domain ?property ?range.
  ?range rdfs:label ?rangeLabel.
 # ?range ?property ?domain.
  ?property rdfs:label ?propertyLabel.
}
WHERE {
  BIND (wd:""" + entityid + """ AS ?domain)
   VALUES ?property { wdt:P1269 wdt:P425 wdt:P101 wdt:P136 wdt:P527 wdt:P1889 wdt:P1557 wdt:P106 wdt:P2388 wdt:P2389 wdt:P361 wdt:P710 wdt:P3095 wdt:P4646 wdt:P641 wdt:P2578 wdt:P366 wdt:P1535 wdt:P2283}
  {?domain ?property ?range.
   ?range rdfs:label ?rangeLabel}
 # UNION
 # {?range ?property ?domain.
   #?range rdfs:label ?rangeLabel}
  OPTIONAL {
   # ?property rdfs:label ?propertyLabel.
    FILTER((LANG(?propertyLabel)) = "en")
    }
  FILTER((LANG(?rangeLabel)) = "en")
}
"""
        # res = return_sparql_query_results(sparql_query)

        sparql.setQuery(sparql_query)
        sparql.setReturnFormat(JSON)

        res = sparql.query().convert()

        res2 = res['results']['bindings']

        return res2



#this functions parse the non hierarchical triples
    def parsetriplesnonhierarchical(self, tripleslist, g):

        statementId = BNode()
        n = Namespace("http://example.org/topicopa/")
        u = "http://www.org/prop/direct/"
        listprop=[]
        i=0
        for tt in tripleslist:

            # for t in tt:
            s = tt['subject']['value']

            p = tt['predicate']['value']
            o = tt['object']['value']
            print('s- '+s)
            print('p- '+p)
            print('o- '+o)

            pid = self.getpid(p)
            oid = self.getid(o)
            if (pid.startswith('P') and oid.startswith('Q')):
                    i += 1

                    istr = f'{i}'
                    plabel = self.getPropLabel(p)

                    pi = (URIRef(u'http://www.wikidata.org/prop/'+pid+'_'+istr+''))
                    #print(pi)
                    olabel = self.getLabel(o)
                    g.add((rdflib.term.URIRef(u'' + o + ''), RDF.type, OWL.Class))
                    g.add((rdflib.term.URIRef(u'' + pi + ''), RDF.type, OWL.ObjectProperty))
                    g.add((URIRef(u'' + pi + ''), RDFS.label, Literal('' + plabel + '-'+olabel+'')))
                    g.add((URIRef(u'' + pi + ''), RDFS.domain,  URIRef(u'' + s + '')))
                    g.add((URIRef(u'' + pi + ''), RDFS.range, URIRef(u'' + o + '')))

            if (p == 'http://www.w3.org/2000/01/rdf-schema#label'):
                 RDFS.Literal = rdflib.term.Literal(u'http://www.w3.org/2000/01/rdf-schema#label', lang='en')

                 g.add((URIRef(u'' + s + ''), RDFS.label, Literal('' + o + '')))

        print("length of graph", len(g))

        for ss, pp, oo in g:
            print("triplets added to graph 3", ss, pp, oo)

        return g


#this functions retrns the lavel of a given uri of a property
    def getPropLabel(self, uri):
        label = ''
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql",
                               agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')
        pid = self.getpid(uri)
        sparql_query = """
SELECT ?property ?propLabel 
  WHERE
  {

   BIND (wdt:""" + pid + """ AS ?property)

  ?prop wikibase:directClaim ?property .

  SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
}       

         """
        # res = return_sparql_query_results(sparql_query)
        sparql.setQuery(sparql_query)
        sparql.setReturnFormat(JSON)
        res = sparql.query().convert()
        res2 = res['results']['bindings']

        label = res2[0]['propLabel']['value']

        return label

#this functions returns the label of a concept wikidata uri
    def getLabel(self, uri):
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql",
                               agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')

        label = ''
        entityid = self.getid(uri)
        sparql_query = """

        SELECT ?item ?itemLabel 
  WHERE
  {
   BIND (wd:""" + entityid + """ AS ?item)
  SERVICE wikibase:label {
    bd:serviceParam wikibase:language "en".
    ?item rdfs:label ?itemLabel.  
  }
    }
    """
        # res = return_sparql_query_results(sparql_query)
        sparql.setQuery(sparql_query)
        sparql.setReturnFormat(JSON)

        res = sparql.query().convert()
        res2 = res['results']['bindings']
        label = res2[0]['itemLabel']['value']

        return label


#return wikidata id of a concept
    def getid(self, uri):
        lengthuri = len(uri)
        id = uri[31:lengthuri]
        return id

#return wikidata id of a property
    def getpid(self, uri):
        lengthuri = len(uri)
        id = uri[36:lengthuri]
        return id

