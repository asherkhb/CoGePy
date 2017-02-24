import requests
import json
from datetime import datetime
from time import sleep

from coge import Experiment, Job
import utils
import errors
from constants import API_BASE, ENDPOINTS


def search(term, fetch=False, username=None, token=None):
    """Search CoGe Experiments by Term

    :param term: Search term (str).
    :param fetch: Should results be fetched/synced with server? Bool.
    :param username: OPTIONAL - CoGe Username.
    :param token: OPTIONAL - CoGe authentication token.
    :return: List of search results, stored as python dictionary. Empty list if no results.
    """
    # Define Search URL
    search_url = API_BASE + ENDPOINTS["experiments_search"] + term

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


def bulk_load(list_of_Experiment_objects, auth_token, task_limit=2):
    if task_limit > 10:
        print("[CoGe API] %s - WARNING - Bulk loading cannot exceed 10 simultaneous tasks. "
              "Limit has been reset to 2 (default)." % datetime.now())
        task_limit = 2

    running = []
    complete = []

    # As long as experiments remain, continue to submit & check for completion.
    while len(list_of_Experiment_objects) > 0:
        if len(running) < task_limit:
            exp = list_of_Experiment_objects.pop(0)
            jid = exp.add(auth_token)
            running.append(Job(jid))
        else:
            # Check if jobs are 'Completed', if so mark as complete & queue for removal from running tasks list.
            remove = []
            for j in running:
                status = j.get_status()
                if status == 'Completed':
                    complete.append(j)
                    remove.append(j)
            # Remove complete tasks.
            for r in remove:
                running.remove(r)

            sleep(60)

    # Wait for any remaining tasks to be completed
    while len(running) > 0:
        # Check if jobs are 'Completed', if so mark as complete & queue for removal from running tasks list.
        remove = []
        for j in running:
            status = j.get_status()
            if status == 'Completed':
                complete.append(j)
                remove.append(j)
        # Remove complete tasks.
        for r in remove:
            running.remove(r)
        # Wait 60 seconds.
        sleep(60)
