
![image](https://user-images.githubusercontent.com/91874965/137097883-86402806-3fa4-4f91-ac29-efab2eb29962.png)

# RelTopic: A Graph-Based Semantic Relatedness Measure in Topic Ontologies 

We present RelTopic, a novel graph-based semantic relatedness measure in topic ontologies for topic labeling purposes. RelTopic aims to assess the semantic relatedness between instances and concepts in topic ontologies by computing weights of nodes and edges, degree centrality of nodes, and shortest paths. RelTopic is applied in the context of `Cultural Heritage`, specifically old press articles. To apply RelTopic, a topic ontology named Topic-OPA is developed from the articles represented by a set of named entities that are disambiguated using *Wikidata* URIs. RelTopic is also tested in recent newspaper articles.

**This study is part of the European project `ASTURIAS` (Structural Analysis and Semantic Indexing of Newspaper Articles)**

#### Publications: 
This research work is addressed in the following papers:

1- El Ghosh, M., Zanni-Merk, C., Delestre, N., Kotowicz, J.P., Abdulrab, H.: Topic-OPA: A Topic Ontology for Modeling Topics of Old Press Articles. In proceedings of the 12th International conference on Knowledge Engineering and Ontology Development (KEOD 2020). pp. 275-282, November 2020

2- El Ghosh, M., Delestre, N., Zanni-Merk, C., Kotowicz, J.P., Abdulrab, H.: RelTopic: A Graph-Based Semantic Relatedness Measure in Topic Ontologies and its Applicability for Topic Labeling of Old Press Articles, [Semantic Web Journal](http://www.semantic-web-journal.net/content/reltopic-graph-based-semantic-relatedness-measure-topic-ontologies-and-its-applicability-1).

------------------------------------------------------------------------------------------
### The code is beta version (Python 3.8 is required) - The project is under improvement
------------------------------------------------------------------------------------------
#### Data Sources
The main data sources are the named entities collected from old press articles and encoded in `XML` files. These files are located in `/Data-Articles/xml/`. For recent press, the named entities are represented (particularly) in `CSV` files located in `/Data-Articles/recent-press/xml/`.

#### Source Code
The source code is composed of the following files:

* **AssignInstances**: assign the named entities as instances of *Wikidata* classes. The inputs are the `XML` files and the outputs are `CSV` files located in `/Data-Articles/csv`.

* **OntologyConstruction**: define a set of SPARQL queries to build topic ontologies. The building process is composed of three main phases: 1) construct the hierarchical structure; 2) construct the non-hierarchical structure; 3) enrich the hierarchy of the ontology.

* **OntologyConstructionApplication**: apply the ontology development in the context of old press articles specifically the old french newspaper `Le Matin`. The inputs are the `CSV` files and the output is an OWL ontology (e.g., Topic-OPA.owl) located in `/ontology/`.

* **TopicOntology**: implement the topic ontology and add the instances. 

* **OntologyDirectedGraph**: transform the topic ontology into a directed weighted graph. The semantic relatedness measure RelTopic is defined based on ontology graph.

* **TopicLabeling**: define the topic labeling process using RelTopic and Topic-OPA. The output is the topic labeling results located in `/labeling-results/csv/`.

* **Main1**: execute the ontology construction process (i.,e. assignment of instances, application of ontology construction). By executing **Main1**, the existent data (ontology+assigned instances) will be replaced.

* **Main2**: execute the topic labeling process. To check and verify the published labeling results of `Le Matin` and recent press articles, execute **Main2** by considering the previously developed ontologies located in `/ontology/`. Please see **IMPORTANT NOTE** below.


#### Labeling Results
The labeling results are `CSV` files located in `/labeling-results/csv/`

-------------------------------------------------------
### IMPORTANT NOTE
-------------------------------------------------------
In this study, the latest version of Topic-OPA is harvested from Wikidata in July `2020`. Applying the ontology construction process currently or in the future will produce a slightly different Topic-OPA since *Wikidata* is continually growing. We show below examples of differences in metrics and hierarchies between Topic-OPA 2020 (created on July 11, 2020) and Topic-OPA 2021 (created on September 28, 2021). These changes will affect RelTopic computations such as *average depth*, *average of relatedness values*, *threshold*, etc. Therefore, the labeling results will be affected. To overcome this limitation, it is advised to curate Topic-OPA under the supervision of domain experts and admit a pertinent version of the ontology.

![image](https://user-images.githubusercontent.com/91874965/135832335-e8510443-8fdc-4fe7-917b-d170ae962de4.png)

![image](https://user-images.githubusercontent.com/91874965/135831768-a222a93d-9b4d-4f65-b51a-a53ab3a7bd60.png)

>>> Recently (October 6 and 7, 2021), we found some errors in Wikidata (thereby in Topic-OPA) such as cyclic subClassOf relations (below we show an example of a class that is subClassOf itself!). Such errors, which a human intervention may cause since *Wikidata* is **human editable**, will prevent the execution of the labeling process. The intervention of the experts remains essential to correct and remove these errors from the developed topic ontology.

![image](https://user-images.githubusercontent.com/91874965/136366523-bde0acef-51d4-419f-906b-5867d8af4b09.png)

-------------------------------------------------------
### TO-DO
-------------------------------------------------------
* **Code**: to improve the topic labeling algorithm and enhance the code.

* **Ontology**: to curate the topic ontology Topic-OPA, apply the labeling process on the curated version, and assess the pertinence of the labeling results .
 
