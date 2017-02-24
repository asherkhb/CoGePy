import requests
import json
from datetime import datetime

from coge import Organism
import utils
import errors
from constants import API_BASE, ENDPOINTS


def search(term, fetch=False, username=None, token=None):
    """Search CoGe Organisms by Term

    :param term: Search term (str).
    :param fetch: Should results be fetched/synced with server? Bool.
    :param username: OPTIONAL - CoGe Username.
    :param token: OPTIONAL - CoGe authentication token.
    :return: List of search results, stored as Organisms. Empty list if no results.
    """
    # Define Search URL
    search_url = API_BASE + ENDPOINTS["organisms_search"] + term

    # Submit search query. Use authentication if provided.
    if username and token:
        response = requests.get(search_url, params={'username': username, 'token': token})
    else:
        response = requests.get(search_url)

    # Check for valid response, exception for non-200 response.
    results = []
    if utils.valid_response(response.status_code):
        organisms = json.loads(response.text)['organisms']
        for o in organisms:
            # TODO: Create Organism() from o, append to results instead.
            #result = coge.Organism(id=o["id"], name=o["name"], description=o["description"], fetch=fetch)
            #results.append(result)
            results.append(o)
    else:
        # Die on invalid response.
        raise errors.InvalidResponseError(response)

    return results


def fetch(id_or_list_of_ids, username=None, token=None):

    # Convert single ID to list.
    if type(id_or_list_of_ids) is not list:
        id_or_list_of_ids = [id_or_list_of_ids]

    # Convert IDs to integers, raise InvalidIDError if cannot convert.
    try:
        ids = [int(i) for i in id_or_list_of_ids]
    except ValueError:
        raise errors.InvalidIDError(id_or_list_of_ids)

    # Fetch each organism.
    results = []
    for organism_id in ids:
        try:
            results.append(Organism(id=organism_id, fetch=True, username=username, token=token))
        except errors.InvalidResponseError:
            print("%s - WARNING - Unable to fetch organism id%d" % (datetime.now(), organism_id))
    # Return either single result, or list of results.
    if len(results) == 1:
        return results[0]
    else:
        return results


# def fetch(id_or_list_of_ids):
#     """Get Organism(s) by ID
#
#     :param id_or_list_of_ids: single ID, or a list of IDs.
#     :return: Organism or [Organism, Organism, ...].
#     """
#     results = None
#     if type(id_or_list_of_ids) == list:
#         try:
#             results = []
#             id_list = [int(d) for d in id_or_list_of_ids]
#             for id in id_list:
#                 results.append(coge.Organism(id, fetch=True))
#         except ValueError:
#             print("Invalid argument (%s)" % id_or_list_of_ids)
#             # TODO: Raise exception.
#     else:
#         try:
#             id = int(id_or_list_of_ids)
#             results = coge.Organism(id, fetch=True)
#         except ValueError:
#             print("Invalid argument (%s)" % id_or_list_of_ids)
#             # TODO: Raise exception.
#     return results


# def add(Organism):
#     """Add an organism to CoGe
#
#     :param Organism: Organism object with name & description
#     :return:
#     """
#     # Fail if genome has an ID.
#     if Organism.id is not None:
#         # TODO: Raise exception.
#         return False
#
#     # Fail if genome object doesn't have
#     if Organism.name is None or Organism.description is None:
#         # TODO: Raise exception.
#         return False
#
#     # Fail if user is not authenticated.
#     if not AUTH:
#         raise errors.AuthError("User is not authenticated.")
#
#     # Construct payload.
#     payload = {'name': Organism.name,
#                'description': Organism.description}
#
#     # Submit PUT request.
#     response = requests.put(API_BASE + ENDPOINTS["organisms_add"],
#                             params=PARAMS,
#                             headers={'Content-Type': 'application/json'},
#                             data=json.dumps(payload))
#     if utils.valid_response(response.status_code):
#         data = json.loads(response.text)
#         return data['id']
#
#     else:
#         # TODO: Raise some exception.
#         return False
