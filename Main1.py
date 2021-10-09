#  Copyright (c) 2021. The ASTURIAS Project.
#   -----------------------------------------------------------------------
#   Version: 1.0.1
#   Contributor: Mirna El Ghosh.
#   Status: Beta version.
#   -----------------------------------------------------------------------
#
#
#
#
import AssignInstances
import OntologyConstructionApplication

if __name__ == "__main__":
    # the ontology construction process:
    # Step1- assign the named entities of old press articles
    i = AssignInstances.AssignInstances()
    sourcelist = 'Data-Articles/xml/articles.csv'
    source = 'Data-Articles/xml/'
    output = 'Data-Articles/csv/'
    i.assign_instances(sourcelist, source, output)

    # Step2- develop the topic ontology
    a = OntologyConstructionApplication.OntologyConstructionApplication()
    a.develop_ontology('ontology/Topic-OPA-2021', '')
