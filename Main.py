#  Copyright (c) 2021. Mirna El Ghosh (ASTURIAS Project) version 1.0
#   ------------------------------------
#   Status: This code is a beta version.
#   ------------------------------------
#   >>>>>>> The software is under improvement <<<<<<<.
#

import TopicLabeling

class Main():
    """This class executes the topic labeling process by applying the following steps:
    1- assign the named entities as instances;
    2- create Topic-OPA ontology based on the assigned named entities;
    3- apply the topic labeling process.
    To do this, the ontology is transformed into a directed weighted graph and RelTopic is applied.
      """

    type_press_list=['','recent-press/']
    ontology_old_press='ontology/Topic-OPA.owl'
    ontology_recent_press='ontology/Topic-RPA.owl'

    t=TopicLabeling.TopicLabeling()

    #uncomment to test the labeling results of recent press articles
    #t.labeling_process(ontology_recent_press, type_press_list[1])

    #labeling old press articles
    #type_press_list[0] is the old press
    t.labeling_process(ontology_old_press, type_press_list[0])
