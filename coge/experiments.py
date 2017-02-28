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


def bulk_load(list_of_Experiment_objects, auth=None, task_limit=2):
    if task_limit > 10:
        print("[CoGe API] %s - WARNING - Bulk loading cannot exceed 10 simultaneous tasks. "
              "Limit has been reset to 2 (default)." % datetime.now())
        task_limit = 2

    running = []
    failed = []
    complete = []

    # As long as experiments remain, continue to submit & check for completion.
    while len(list_of_Experiment_objects) > 0:
        if len(running) < task_limit:
            exp = list_of_Experiment_objects.pop(0)
            load_info = exp.add(auth=auth)
            if load_info:
                print('[CoGe API] %s - INFO - Experiment %s submitted for add. See %s'
                      % (datetime.now(), exp.name, load_info['site_url']))
                print('... %s adds remaining.' % len(list_of_Experiment_objects))
                jobid = load_info['id']
                running.append((Job(jobid), exp))
            else:
                failed.append(exp)
        else:
            # Check if jobs are 'Completed', if so mark as complete & queue for removal from running tasks list.
            remove = []
            for r in running:
                j = r[0]  # Job part of tuple.
                e = r[1]  # Experiment part of tuple.
                status = j.update_status()
                if status.lower() == 'completed':
                    print('[CoGe API] %s - INFO - Experiment %s load complete.' % (datetime.now(), e.name))
                    complete.append(e)
                    remove.append(r)
                elif status.lower() == 'failed':
                    print('[CoGe API] %s - WARNING - Experiment %s load failed.' % (datetime.now(), e.name))
                    failed.append(e)
                    remove.append(r)
            # Remove complete tasks.
            for t in remove:
                running.remove(t)
            # Wait 60 seconds before checking again.
            sleep(60)

    # Wait for any remaining tasks to be completed
    while len(running) > 0:
        # Check if jobs are 'Completed', if so mark as complete & queue for removal from running tasks list.
        remove = []
        for r in running:
            j = r[0]  # Job part of tuple.
            e = r[1]  # Experiment part of tuple.
            status = j.update_status()
            if status.lower() == 'completed':
                print('[CoGe API] %s - INFO - Experiment %s load complete.' % (datetime.now(), e.name))
                complete.append(e)
                remove.append(r)
            elif status.lower() == 'failed':
                print('[CoGe API] %s - WARNING - Experiment %s load failed.' % (datetime.now(), e.name))
                failed.append(e)
                remove.append(r)
        # Remove complete tasks.
        for t in remove:
            running.remove(t)
        # Wait 60 seconds before checking again.
        sleep(60)

    # Print completion messages.
    print('[CoGe API] %s - INFO - INFO - Bulk experiment load complete. %s experiments loaded successfully.'
          % (datetime.now(), str(len(complete))))
    if len(failed) > 0:
        print('[CoGe API] %s - WARNING - Not all loads successful (%s failed)' % datetime.now(), str(len(failed)))
    # Return tasks that succeeded and those that failed.
    return complete, failed
