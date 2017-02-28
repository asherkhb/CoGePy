import os
import sys
sys.path.insert(0, os.path.abspath('..'))
import coge

import pandas as pd
from pprint import pprint

def main():
    # # ------------------------------------------- # #
    # # AUTHENTICATION
    # # TODO: Authenticate from username/password.
    # # TODO: Check validity of token.
    # # ------------------------------------------- # #

    # # Create an authentication object.
    my_auth = coge.auth.AuthToken(username='', token='')

    # my_auth = coge.auth.AuthToken(username='USERNAME', password='PASSWORD')

    # # Access features of authentication
    # usr = my_auth.username
    # tkn = my_auth.token
    # exp = my_auth.expiration

    # # ------------------------------------------- # #
    # # EXPERIMENTS
    # # ------------------------------------------- # #

    # Fetch experiment.
    # my_exp = coge.Experiment(id=10115, auth=my_auth)
    # print(my_exp)

    # # Load experiment(s).
    # my_experiments = pd.read_csv('experiments.tsv', sep='\t', header=0)
    #
    # # Define some basic analysis parameters.
    # my_parameters = [{'read_params': {'read_type': 'paired', "encoding": 33}},
    #                  {'trimming_params': {'trimmer': 'cutadapt'}},
    #                  {'incorrect_params': []}]
    # # Single experiment.
    # exp_info = my_experiments.ix[0]
    # my_exp = coge.Experiment(name=exp_info['name'],
    #                          description=exp_info['description'],
    #                          version=exp_info['version'],
    #                          source=exp_info['source'],
    #                          restricted=True,
    #                          genome_id=exp_info['genome_id'],
    #                          notebook_id=exp_info['notebook_id'],
    #                          tags=[t for t in exp_info['tags'].split(',')],
    #                          source_data={'type': 'irods', 'path': exp_info['source_data']},
    #                          analysis_parameters=my_parameters)
    # my_exp.add(auth=my_auth)

    # Bulk loading experiments.
    # experiment_objs = []
    # for exp in my_experiments.iterrows():
    #    experiment = coge.Experiment()

    # Update an experiment.
    my_exp = coge.Experiment(id=9012, auth=my_auth)
    print(my_exp.name)
    my_exp.name = 'New Name!'
    my_exp.description = "A fun, updated description to tell about my experiment."
    update_status = my_exp.update(update_properties=['name', 'description'], auth=my_auth)
    print("Update success: %s" % str(update_status))

    # # Delete experiment
    # my_exp = coge.Experiment(id=9012, auth=my_auth)
    # my_exp.delete(auth=my_auth)

    # # ------------------------------------------- # #
    # # JOBS
    # # ------------------------------------------- # #
    #my_job = coge.Job(id=44285)
    #print(my_job.status)




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

    # # Fetch organism using organisms module.
    # my_organism = coge.organisms.fetch(1)
    # print my_organism
    #
    # # Create & fetch an organism using Organism class.
    # my_organism = coge.Organism(1, fetch=True)
    # print my_organism
    #
    # # Create an organism using Organism class, then fetch afterwards.
    # my_organism = coge.Organism(1)
    # my_organism.fetch()  # Could use username=X token=Y for authentication
    # print my_organism
    #
    # # Fetch multiple organisms using organisms module fetch function.
    # my_organisms = coge.organisms.fetch([1, 3, 4])
    # for my_organism in my_organisms:
    #     print my_organism



    # Test adding organism.
    # my_organism = coge.Organism(name="Test", description="A demo test organism")
    # coge.organisms.add(my_organism)




if __name__ == '__main__':
    main()
    sys.exit(0)
