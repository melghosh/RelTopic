#  Copyright (c) 2021. Mirna El Ghosh (ASTURIAS Project) version 1.0
#   ------------------------------------
#   Status: This code is a beta version.
#   ------------------------------------
#   >>>>>>> The software is under improvement <<<<<<<.
#

#import AssignInstances
#import OntologyConstructionApplication
#import TopicLabeling

class Main():
    """This class executes the topic labeling process by applying the following steps:
    1- assign the named entities as instances;
    2- create Topic-OPA ontology based on the assigned named entities;
    3- apply the topic labeling process. To do this, the ontology is transformed into a directed weighted graph and RelTopic is applied.
      """

   # TopicLabeling()