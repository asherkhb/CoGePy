import os
import sys
sys.path.insert(0, os.path.abspath('..'))
import coge


def main():
    # my_organism = coge.Organism(1, fetch=True)
    # my_organism.fetch(coge.API_BASE)
    # my_organisms = coge.get_organisms_by_id([1, 3, 4])
    # for my_organism in my_organisms:
    #     print repr(my_organism)
    #     print str(my_organism)
    #     print type(my_organism)
    #
    #     print my_organism.name
    #     print my_organism.description
    #     print my_organism.genomes

    search_results = coge.search_organisms("Confusing search term")
    print search_results

if __name__ == '__main__':
    main()
    sys.exit(0)
