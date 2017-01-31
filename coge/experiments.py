import requests
import json

# import coge
import utils
import errors
from constants import DEV_BASE, ENDPOINTS


def search(term, fetch=False, username=None, token=None):
    """Search CoGe Experiments by Term

    :param term: Search term (str).
    :param fetch: Should results be fetched/synced with server? Bool.
    :param username: OPTIONAL - CoGe Username.
    :param token: OPTIONAL - CoGe authentication token.
    :return: List of search results, stored as python dictionary. Empty list if no results.
    """
    # Define Search URL
    search_url = DEV_BASE + ENDPOINTS["experiments_search"] + term

    # Submit search query. Use authentication if provided.
    if username and token:
        response = requests.get(search_url, params={'username': username, 'token': token})
    else:
        response = requests.get(search_url)

    # Check for valid response, exception for non-200 response.
    results = []
    if utils.valid_response(response.status_code):
        experiments = json.loads(response.text)['experiments']
        for e in experiments:
            # TODO: Create Experiment() from e, append to results instead.
            # result = coge.Experiment(e, fetch=fetch)
            # results.append(result)
            results.append(e)
    else:
        # Die on invalid response.
        raise errors.InvalidResponseError(response)

    return results
