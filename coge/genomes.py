import requests
import json

from coge import Genome
import utils
import errors
from constants import API_BASE, ENDPOINTS


def search(term, auth=None):
    """Search CoGe Genomes by Term

    :param term: Search term (str).
    :param auth: Valid AuthToken().
    :return: List of search results, stored as Genomes. Empty list if no results.
    """
    # Confirm term is a string.
    term = str(term)

    # Define Search URL.
    search_url = API_BASE + ENDPOINTS["genomes_search"]

    # Search (use authentication if provided).
    if auth:
        response = requests.get(search_url + term, params={'username': auth.username, 'token': auth.token})
    else:
        response = requests.get(search_url + term)

    # List for results.
    results = []

    # Check for valid response, create Organism() for each result.
    if utils.valid_response(response.status_code):
        response_data = json.loads(response.text)
        for g in response_data['genomes']:
            gid = g.get('id', None)
            if gid is not None:
                genome = Genome(id=gid)
                genome.fetch(auth=auth)
                results.append(genome)
    else:
        # Die on invalid response.
        raise errors.InvalidResponseError(response)

    return results
