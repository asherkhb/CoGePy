import utils
from constants import API_BASE, AUTH, PARAMS
import requests
import json


class Organism(object):
    """Organism Class"""

    def __init__(self, id, fetch=False):
        self.id = id
        self.resolved = False
        self.name = None
        self.description = None
        self.genomes = None
        self.linked_genomes = None  # TODO: Add ability to link genomes.
        if fetch:
            self.fetch(API_BASE)

    def __repr__(self):
        if self.resolved:
            return "< ORGANISM id%s (resolved) >" % str(self.id)
        else:
            return "< ORGANISM id%s (empty) >" % str(self.id)

    def __str__(self):
        if self.resolved:
            return "Organism (id%s): %s" % (str(self.id), self.name)
        else:
            return "Unresolved organism (id%s)" % str(self.id)

    def fetch(self, api_base):
        organisms_endpoint = 'organisms/'
        # Get organism information
        if AUTH:
            response = requests.get(api_base + organisms_endpoint + str(self.id), params=PARAMS)
        else:
            response = requests.get(api_base + organisms_endpoint + str(self.id))
        # Set name, description, and genomes.
        if utils.response_is_valid(response.status_code):
            response_data = json.loads(response.text)
            self.name = response_data.get('name', None)
            self.description = response_data.get('description', None)
            self.genomes = response_data.get('genomes', None)
            self.resolved = True
        else:
            utils.report_invalid_response(response)


def get_organisms_by_id(id_or_list_of_ids):
    """Get Organism(s) by ID

    :param id_or_list_of_ids: single ID, or a list of IDs.
    :return: Organism or [Organism, list].
    """
    results = None
    if type(id_or_list_of_ids) == list:
        try:
            results = []
            id_list = [int(d) for d in id_or_list_of_ids]
            for id in id_list:
                results.append(Organism(id, fetch=True))
        except ValueError:
            print("Invalid argument (%s)" % id_or_list_of_ids)
    else:
        try:
            id = int(id_or_list_of_ids)
            results = Organism(id, fetch=True)
        except ValueError:
            print("Invalid argument (%s)" % id_or_list_of_ids)
    return results


def search_organisms(term):
    """Search CoGe Organisms by Term

    :param term: Search term (str).
    :return: List of search results, as dictionaries with keys "id", "name" & "description". Empty list if no results.
    """
    search_endpoint = 'organisms/search/'

    if AUTH:
        response = requests.get(API_BASE + search_endpoint + str(term), params=PARAMS)
    else:
        response = requests.get(API_BASE + search_endpoint + str(term))

    if utils.response_is_valid(response.status_code):
        data = json.loads(response.text)
        return data["organisms"]
    else:
        utils.report_invalid_response(response)
        return False


def add_organism():
    pass