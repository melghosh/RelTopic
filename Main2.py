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

import TopicLabeling

if __name__ == "__main__":
    #apply topic labeling
    t = TopicLabeling.TopicLabeling()
    t.labeling_process('ontology/Topic-OPA.owl', '')
    #t.labeling_process('ontology/Topic-RPA.owl', 'recent-press/')
