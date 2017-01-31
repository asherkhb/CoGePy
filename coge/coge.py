import requests
import json

# CoGe API Imports
from constants import *
import utils
import auth
import errors


class Organism(object):
    """Organism Class"""

    def __init__(self, id=None, name=None, description=None, genomes=None, fetch=False, username=None, token=None):
        self.id = id
        self.name = name
        self.description = description
        self.genomes = genomes

        self.sync = False
        self.sync_msg = None

        self.linked_genomes = None  # TODO: Add ability to link genomes.

        if fetch and id is not None:
            if name or description or genomes:
                # TODO: Raise Warning for overwrite?. Could have undesirable effects with search, creating, etc.
                pass
            self.fetch(username=username, token=token)

    def __repr__(self):
        if self.sync:
            return "< ORGANISM id%s (synced) >" % str(self.id)
        else:
            return "< ORGANISM id%s (local) >" % str(self.id)

    def __str__(self):
        if self.sync:
            return "Synced Organism (id%s): %s" % (str(self.id), self.name)
        else:
            return "Local Organism (id%s): %s" % (str(self.id), self.name)

    def fetch(self, username=None, token=None):
        # Define Fetch URL.
        fetch_url = DEV_BASE + ENDPOINTS["organisms_fetch"]

        # Fetch organism, with authentication if provided.
        if username and token:
            response = requests.get(fetch_url + str(self.id), params={'username': username, 'token': token})
        else:
            response = requests.get(fetch_url + str(self.id))

        # Set name, description, and genomes.
        if utils.valid_response(response.status_code):
            response_data = json.loads(response.text)
            self.name = response_data.get('name', None)
            self.description = response_data.get('description', None)
            self.genomes = response_data.get('genomes', None)
            # TODO: Gather genomes as genome objects.
            self.sync = True
        else:
            raise errors.InvalidResponseError(response)

    def fetch_genomes(self, api_base=DEV_BASE):
        # TODO: Link genomes.
        raise NotImplementedError


class Genome(object):
    """Genome Class"""

    def __init__(self, id=None, name=None, description=None, link=None, version=None, organism_id=None, sequence_type=None,
                 restricted=False, chromosome_count=None, organism=None, obj_type='local', fetch=False):
        self.id = id
        self.name = name
        self.description = description
        self.link = link
        self.version = version
        self.organism_id = organism_id
        self.sequence_type = sequence_type
        self.restricted = restricted
        self.chromosome_count = chromosome_count
        self.organism = Organism(id=organism["id"], name=organism["name"], description=organism["description"])

        self.obj_type = obj_type

        if fetch:
            self.fetch()

    #@auth.authenticated TODO: Authentication Wrapper
    # def fetch(self):
    #     if AUTH:
    #         response = requests.get(api_base + ENDPOINTS['organisms'] + str(self.id), params=PARAMS)
    #     else:
    #         response = requests.get(api_base + ENDPOINTS['organisms'] + str(self.id), params=PARAMS)

    def fetch_sequence(self):
        # TODO: Fetch Sequence
        raise NotImplementedError

    def export(self):
        # TODO: Export
        raise NotImplementedError

    def add(self):
        # TODO: Add genome
        raise NotImplementedError


class Experiment(object):
    """Experiment Class"""

    def __init__(self):
        self.id = None

    def fetch(self):
        raise NotImplementedError

    def add(self):
        raise NotImplementedError


# CoGe Module Imports
import organisms
import genomes
import experiments
