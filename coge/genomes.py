import requests
import json

from coge import Genome
import utils
import errors
from constants import API_BASE, ENDPOINTS


def search(term, fetch=False, username=None, token=None):
    """Search CoGe Genomes by Term

    :param term: Search term (str).
    :param fetch: Should results be fetched/synced with server? Bool.
    :param username: OPTIONAL - CoGe Username.
    :param token: OPTIONAL - CoGe authentication token.
    :return: List of search results, stored as python dictionary. Empty list if no results.
    """
    # Define Search URL.
    search_url = API_BASE + ENDPOINTS["genomes_search"] + term

    # Submit search query. Use authentication if provided.
    if username and token:
        response = requests.get(search_url, params={'username': username, 'token': token})
    else:
        response = requests.get(search_url)

    # Check for valid response, exception for non-200 response.
    results = []
    if utils.valid_response(response.status_code):
        genomes = json.loads(response.text)['genomes']
        for g in genomes:
            # TODO: Create Genome() from g, append to results instead.
            # result = Genome(g, fetch=fetch)
            # results.append(result)
            results.append(g)
    else:
        # Die on invalid response.
        raise errors.InvalidResponseError(response)

    return results


def fetch(id_or_list_of_ids, username=None, token=None):

    # Define Fetch URL.
    fetch_url = API_BASE + ENDPOINTS["genomes_fetch"]

    # Convert single ID to list.
    if type(id_or_list_of_ids) is not list:
        id_or_list_of_ids = [id_or_list_of_ids]

    # Convert IDs to integers, raise InvalidIDError if cannot convert.
    try:
        ids = [int(i) for i in id_or_list_of_ids]
    except ValueError:
        raise errors.InvalidIDError(id_or_list_of_ids)

    # Fetch each genome.
    results = []
    for genome_id in ids:
        try:
            results.append(Genome(id=genome_id, fetch=True))
        except errors.InvalidResponseError:
            print("Unable to fetch genome for ID %d" % genome_id)

    # Return either single result, or list of results.
    if len(results) == 1:
        return results[0]
    else:
        return results