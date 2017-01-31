import os
import sys
sys.path.insert(0, os.path.abspath('..'))
import coge

from pprint import pprint

def main():
    # # ------------------------------------------- # #
    # # AUTHENTICATION
    # # TODO: Create authentication capacity.
    # # ------------------------------------------- # #

    # # Create an authentication object.
    # my_auth = coge.auth.AuthToken(username='USERNAME', password='PASSWORD')

    # # Access features of authentication
    # usr = my_auth.username
    # tkn = my_auth.token
    # exp = my_auth.expiration

    # # ------------------------------------------- # #
    # # SEARCHES
    # # TODO: Include examples with authentication, fetching features.
    # # ------------------------------------------- # #

    # # Search organisms
    # organism_search_results = coge.organisms.search("Col-0")  # TODO: Example with authentication, fetching
    # pprint(organism_search_results)
    #
    # # Search genomes
    # genome_search_results = coge.genomes.search("Col-0")  # TODO: Example with authentication, fetching
    # pprint(genome_search_results)
    #
    # # Search experiments
    # experiment_search_results = coge.experiments.search("Col-0")  # TODO: Example with authentication, fetching
    # pprint(experiment_search_results)

    # # ------------------------------------------- # #
    # # FETCHES
    # # TODO: Include examples with authentication.
    # # TODO: Expand to organisms, genomes.
    # # ------------------------------------------- # #

    # Fetch organism using organisms module.
    my_organism = coge.organisms.fetch(1)
    print my_organism

    # Create & fetch an organism using Organism class.
    my_organism = coge.Organism(1, fetch=True)
    print my_organism

    # Create an organism using Organism class, then fetch afterwards.
    my_organism = coge.Organism(1)
    my_organism.fetch()  # Could use username=X token=Y for authentication
    print my_organism

    # Fetch multiple organisms using organisms module fetch function.
    my_organisms = coge.organisms.fetch([1, 3, 4])
    for my_organism in my_organisms:
        print my_organism



    # Test adding organism.
    # my_organism = coge.Organism(name="Test", description="A demo test organism")
    # coge.organisms.add(my_organism)




if __name__ == '__main__':
    main()
    sys.exit(0)
