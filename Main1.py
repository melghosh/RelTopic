#  Copyright (c) 2021. The ASTURIAS Project.
#   ---------------------------------------------------
#   Version: 1.0.1
#   Contributor: Mirna El Ghosh.
#   Status: Beta version.
#   ---------------------------------------------------
#
import OntologyConstructionApplication

class Main():
    """This class executes the ontology construction process by applying the following steps:
    1- assign the named entities as instances;
    2- create Topic-OPA or Topic-RPA ontology based on the assigned named entities;
      """

    #Step2- to develop the topic ontology
    type_press_list = ['', 'recent-press/']
    ontology_old_press = 'Topic-OPA.owl'
    ontology_recent_press = 'Topic-RPA.owl'
    a=OntologyConstructionApplication.OntologyConstructionApplication()

    #develop Topic-OPA for old press
    a.develop_ontology(ontology_old_press,type_press_list[0])

    #uncomment to develop ontology for recent press
    #a.develop_ontology(ontology_recent_press,type_press_list[1])


