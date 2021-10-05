#  Copyright (c) 2021. The ASTURIAS Project.
#   ---------------------------------------------------
#   Version: 1.0.1
#   Contributor: Mirna El Ghosh.
#   Status: Beta version.
#   ---------------------------------------------------
#

import TopicLabeling

class Main():
    """This class executes the topic labeling process
      """
    type_press_list = ['', 'recent-press/']
    ontology_old_press = 'ontology/Topic-OPA.owl'
    ontology_recent_press = 'ontology/Topic-RPA.owl'

    t=TopicLabeling.TopicLabeling()

    #uncomment to apply the labeling of recent press articles
    #t.labeling_process(ontology_recent_press, type_press_list[1])

    #labeling old press articles
    #type_press_list[0] is for the old press
    t.labeling_process(ontology_old_press, type_press_list[0])
