import requests
import json
from datetime import datetime

from coge import Organism
import utils
import errors
from constants import API_BASE, ENDPOINTS


def search(term, auth=None):
    """Search CoGe Organisms by Term

    :param term: Search term (str).
    :return: List of search results, stored as Organisms. Empty list if no results.
    """
    # Confirm term is a string.
    term = str(term)

    # Define Search URL
    search_url = API_BASE + ENDPOINTS["organisms_search"]

    # List to store results
    results = []

    # Search.
    response = requests.get(search_url + term)

    # Check for valid response, create Organism() for each result.
    if utils.valid_response(response.status_code):
        response_data = json.loads(response.text)
        for o in response_data['organisms']:
            org = Organism(id=o['id'], name=o['name'], description=o['description'])
            org.fetch()
            results.append(org)
    else:
        raise errors.InvalidResponseError(response)

    # Return list of results.
    return results
