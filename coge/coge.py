import requests
import json
from datetime import datetime

from pprint import pprint

# CoGe API Imports
from constants import *
import utils
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
        fetch_url = API_BASE + ENDPOINTS["organisms_fetch"]

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

    def fetch_genomes(self, api_base=API_BASE):
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

    def __init__(self, id=None, name=None, description=None, version=1, source='CoGePy', restricted=True,
                 genome_id=None, notebook_id=None, tags=None, additional_metadata=None, source_data=None,
                 analysis_parameters=None, authtoken=None):
        if id:
            self.id = id
            self.sync = False
            if name:
                print("[CoGe API] %s - WARNING - Experiment ID & name both specified, using ID to fetch. "
                      "Values may be overwritten." % datetime.now())
            self.fetch(auth=authtoken)

        elif name and genome_id:
            # Add basic info.
            self.id = None
            self.types = None
            self.sync = False
            self.name = name
            self.description = description
            self.version = version
            self.source = source
            self.restricted = restricted

            self.genome_id = genome_id
            self.notebook_id = notebook_id

            # Add tags.
            self.tags = []
            if tags:
                self.add_tags(tags)

            # Add additional metadata.
            self.additional_metadata = []
            if additional_metadata:
                self.add_metadata(additional_metadata)

            # Add source_data
            self.source_data = []
            if source_data:
                self.add_source_data(source_data)

            # # Add analysis_parameters
            # self.analysis_parameters = {}
            # if analysis_parameters:
            #     self.add_analysis_parameters(analysis_parameters)

            # Properties for checking status of add.
            self.added = False
            self.addid = None
        else:
            print("[CoGe API] %s - ERROR - Invalid experiment specification.\n"
                  "... To fetch an experiment from CoGe: specify id ( i.e. Experiment(id=1) ).\n"
                  "... To create a new experiment: specify name, genome_id, and source data.\n"
                  "... ... optional: description, version, source, restricted, notebook_id, tags, additional_metadata "
                  "and analysis_parameters.")
            raise errors.InvalidCogeObject(msg="Experiment creation failed.")

    def __repr__(self):
        if self.sync:
            return "< EXPERIMENT | %s | id%s | synced >" % (self.name, str(self.id))
        else:
            return "< EXPERIMENT | %s | id%s | local >" % (self.name, str(self.id))

    def __str__(self):
        if self.sync:
            return "Synced Experiment '%s' (CoGe id%s)" % (self.name, str(self.id))
        else:
            return "Local Experiment '%s' (CoGe id%s)" % (self.name, str(self.id))

    def fetch(self, auth):
        # Define Fetch URL.
        fetch_url = API_BASE + ENDPOINTS["experiments_fetch"]

        # Fetch organism, with authentication if provided.
        if auth:
            response = requests.get(fetch_url + str(self.id), params={'username': auth.username, 'token': auth.token})
        else:
            response = requests.get(fetch_url + str(self.id))

        # Check response, populate experiment information.
        if utils.valid_response(response.status_code):
            response_data = json.loads(response.text)

            self.name = response_data.get('name', None)
            self.description = response_data.get('description', None)
            self.version = response_data.get('version', None)
            self.source = response_data.get('source', None)
            self.restricted = response_data.get('restricted', None)
            self.genome_id = response_data.get('genome_id', None)
            self.notebook_id = response_data.get('notebook_id', None)
            self.tags = response_data.get('tags', None)
            self.additional_metadata = response_data.get('additional_metadata', None)
            self.types = response_data.get('types', None)

            self.sync = True
        else:
            raise errors.InvalidResponseError(response)

    def add(self, auth=None):
        if auth is None:
            print("[CoGe API] %s - ERROR - Experiment add requires authentication. Specify an AuthToken.")
            raise errors.AuthError("No AuthToken specified.")

        if self.sync:
            print("[CoGe API] %s - WARNING - Experiment %s is synced with the server and cannot be added."
                  % (datetime.now(), self.name))
            return False

        if self.id:
            print("[CoGe API] %s - WARNING - Experiment already has an assigned ID (%s) and cannot be added."
                  % (datetime.now(), self.id))
            return False

        if len(self.source_data) < 1:
            print("[CoGe API] %s - WARNING - Experiment %s has no source data and cannot be added."
                  % (datetime.now(), self.name))
            return False

        header = {'Content-Type': 'application/json'}
        params = {'username': auth.username, 'token': auth.token}
        payload = {'genome_id': self.genome_id,
                   'metadata': {
                       'name': self.name,
                       'version': self.version,
                       'source': self.source,
                       'restricted': self.restricted,
                   },
                   'source_data': self.source_data}

        # Add optional parameters to payload
        if self.notebook_id:
            payload['notebook_id'] = self.notebook_id
        if self.description:
            payload['metadata']['description'] = self.description
        if self.tags:
            payload['metadata']['tags'] = self.tags
        if self.additional_metadata:
            payload['additional_metadata'] = self.additional_metadata
        # TODO: Add analysis parameters
        # if self.analysis_parameters:
        #     for param in self.analysis_parameters:
        #         payload[param] = self.analysis_parameters[param]

        # Submit request.
        put_response = requests.put(API_BASE + ENDPOINTS['experiments_add'],
                                    params=params,
                                    headers=header,
                                    data=json.dumps(payload))

        # Check request response for validity.
        if not utils.valid_response(put_response.status_code):
            raise errors.InvalidResponseError(put_response)

        # Parse response
        load_info = json.loads(put_response.text)
        if load_info['success']:
            self.added = True
            self.addid = load_info['id']
            return load_info
        else:
            print("[CoGe API] %s - WARNING" % datetime.now())
            return False

    def add_tags(self, tags):
        if type(tags) == str:
            self.tags.append(tags)
        elif type(tags) == list:
            self.tags += [str(t) for t in tags]
        else:
            print("[CoGe API] %s - WARNING - add_tag failed (unrecognized tag argument %s).\n"
                  "... A single tag can be specified as a string, multiple tags should be specified in a list."
                  % (datetime.now(), tag))

    def add_metadata(self, metadata):
        req = ["type", "text"]
        opt = ["type_group", "link"]

        if type(metadata) == dict:
            if not set(req).issubset(metadata.keys()):
                print("[CoGe API] %s - WARNING - Both 'type' and 'text' must be specified for additional "
                      "metadata. Skipping %s." % (datetime.now(), str(metadata)))
            else:
                for k, v in metadata.iteritems():
                    if k not in req and k not in opt:
                        m.pop(k, None)
                        print("[CoGe API] %s - WARNING - Unknown additional_metadata key (%s) was removed.\n"
                              "... Only 'type', 'text', 'type_group', and 'link' are currently supported."
                              % (datetime.now(), k))
                    self.additional_metadata.append(metadata)

        elif type(metadata) == list:
            md = []
            for m in metadata:
                if type(m) is not dict:
                    print("[CoGe API] %s - WARNING - Additional metadata must be specified in dictionary form. "
                          "Skipping %s." % (datetime.now(), str(m)))
                elif not set(req).issubset(m.keys()):
                    print("[CoGe API] %s - WARNING - Both 'type' and 'text' must be specified for additional "
                          "metadata. Skipping %s." % (datetime.now(), str(m)))
                else:
                    for k, v in m.iteritems():
                        if k not in req and k not in opt:
                            m.pop(k, None)
                            print("[CoGe API] %s - WARNING - Unknown additional_metadata key (%s) was removed.\n"
                                  "... Only 'type', 'text', 'type_group', and 'link' are currently supported."
                                  % (datetime.now(), k))
                        md.append(m)

            self.additional_metadata += md

        else:
            print("[CoGe API] %s - WARNING - add_metadata failed (unrecognized metadata format %s).\n"
                  "... A single metadata entry can be specified as a dict, multiple should be specified by list."
                  % (datetime.now(), metadata))

    def add_source_data(self, sources):
        source_types = ['irods', 'ftp', 'http', 'sra']

        def validate_source(source):
            source_type = source.get('type', None)
            source_path = source.get('path', None)
            if source_type and source_path:
                if source_type not in source_types:
                    print("[CoGe API] %s - WARNING - Invalid source type (%s). Skipping...\n"
                          "... supported types: %s." % (datetime.now(), str(source_type), ', '.join(source_types)))
                    return False
                else:
                    return {'type': source_type, 'path': source_path}
            else:
                print("[CoGe API] %s - WARNING - Source missing type or path (%s). Skipping..."
                      % (datetime.now(), str(source)))
                return False

        if type(sources) == dict:
            r = validate_source(sources)
            if r:
                self.source_data.append(r)

        elif type(sources) == list:
            for s in sources:
                r = validate_source(s)
                if r:
                    self.source_data.append(r)
        else:
            print("[CoGe API] %s - WARNING - add_source_data failed (unrecognized source format %s).\n"
                  "... A single source can be specified as a dict, multiple should be specified by list."
                  % (datetime.now(), sources))

    def check_add(self):
        if self.added and self.addid:
            task = Job(id=self.addid)
            task.update_status()
            stat = task.status
            print("[CoGe API] %s - INFO - Experiment add status: %s" % (datetime.now(), stat))
            # TODO: If completed, update experiment ID.
            # if stat == "Completed":
            #     self.id = ''
            return task.status
        else:
            print("[CoGe API] %s - WARNING - Experiment %s not added, or missing add_id. Unable to check status."
                  % (datetime.now(), self.name))
            return False

class Job(object):
    def __init__(self, id=None, auth=None):
        self.id = id
        self.auth = auth
        self.status = self.update_status()

    def query(self):
        url = API_BASE + ENDPOINTS['jobs_fetch']
        if self.auth:
            response = requests.get(url + str(self.id),
                                    params={'username': self.auth.username, 'token': self.auth.token})
        else:
            response = requests.get(url + str(self.id))

        if not utils.valid_response(response.status_code):
            raise errors.InvalidResponseError(response)

        response_data = json.loads(response.text)
        pprint(response_data)
        return response_data

    def update_status(self):
        response = self.query()
        return response['status']


# CoGe Module Imports
import auth
import organisms
import genomes
import experiments
