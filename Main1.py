#  Copyright (c) 2021. The ASTURIAS Project.
#   ---------------------------------------------------
#   Version: 1.0.1
#   Contributor: Mirna El Ghosh.
#   Status: Beta version.
#   ---------------------------------------------------
#
import AssignInstances
import OntologyConstructionApplication

class Main():
    """This class executes the ontology construction process by applying the following steps:
    1- assign the named entities as instances;
    2- create Topic-OPA or Topic-RPA ontology based on the assigned named entities;
      """

    #Step1- to assign named entities as instances
    #this step is under improvement to cover different types of entry files (e.g., XML, CSV) -
    #named entities of old press are represented in XML files
    # named entities of recent press  are represented in CSV files.

    #to execute the process on old press articles uncomment the following
    i=AssignInstances.AssignInstances()
    sourcelist='Data-Articles/xml/articles.csv'
    source='Data-Articles/xml/'
    output='Data-Articles/csv/'
    i.assign_instances(sourcelist, source,output)


    #Step2- to develop the topic ontology
    type_press_list = ['', 'recent-press/']
    ontology_old_press = 'Topic-OPA.owl'
    ontology_recent_press = 'Topic-RPA.owl'
    a=OntologyConstructionApplication.OntologyConstructionApplication()

    #develop Topic-OPA for old press
    a.develop_ontology(ontology_old_press,type_press_list[0])

    #uncomment to develop ontology for recent press
    #a.develop_ontology(ontology_recent_press,type_press_list[1])


