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
                 analysis_parameters=None, auth=None):
        if id:
            self.id = id
            self.sync = False
            if name:
                print("[CoGe API] %s - WARNING - Experiment ID & name both specified, using ID to fetch. "
                      "Values may be overwritten." % datetime.now())
            self.fetch(auth=auth)

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

            # Add analysis_parameters
            self.analysis_parameters = {}
            if analysis_parameters:
                self.add_analysis_parameters(analysis_parameters)

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
        if self.analysis_parameters:
            payload.update(self.analysis_parameters)

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
            print("[CoGe API] %s - WARNING - Load for Experiment %s failed." % (datetime.now(), self.name))
            return False

    def update(self, update_properties=None, auth=None):
        if auth is None:
            print("[CoGe API] %s - ERROR - Experiment update requires authentication. Specify an AuthToken.")
            raise errors.AuthError("No AuthToken specified.")

        if type(update_properties) is None:
            print("[CoGe API] %s - WARNING - Update failed (no properties to update specified)." % datetime.now())

        if type(update_properties) is not list:
            print("[CoGe API] %s - WARNING - Update failed (properties to update should be specified in a list)."
                  % datetime.now())
        if self.id is None:
            print("[CoGe API] %s - WARNING - Experiment %s has no ID and cannot be updated."
                  % (datetime.now(), self.name))
            return False

        header = {'Content-Type': 'application/json'}
        params = {'username': auth.username, 'token': auth.token}
        payload = {}
        for field in update_properties:
            value = getattr(self, field, None)
            if value is not None:
                payload[field] = value
            else:
                print("[CoGe API] %s - WARNING - Property %s was None or does not exist and cannot be updated."
                      % datetime.now())
        # Submit request.
        post_response = requests.post(API_BASE + ENDPOINTS['experiments_update'] + str(self.id),
                                      params=params,
                                      headers=header,
                                      data=json.dumps(payload))

        # Check request response for validity.
        if not utils.valid_response(post_response.status_code):
            raise errors.InvalidResponseError(post_response)

        # Parse response
        load_info = json.loads(post_response.text)
        if load_info.get('success', False):
            return True
        else:
            print("[CoGe API] %s - WARNING - Update for Experiment %s failed." % (datetime.now(), self.name))
            return False

    def delete(self, auth=None):
        if auth is None:
            print("[CoGe API] %s - ERROR - Experiment delete requires authentication. Specify an AuthToken.")
            raise errors.AuthError("No AuthToken specified.")
        # Send delete request
        delete_response = requests.delete(API_BASE + ENDPOINTS['experiments_delete'] + str(self.id),
                                          params={'username': auth.username, 'token': auth.token})

        # Check request response for validity.
        if not utils.valid_response(delete_response.status_code):
            raise errors.InvalidResponseError(delete_response)

        # Parse response
        load_info = json.loads(delete_response.text)
        if load_info.get('success', False):
            return True
        else:
            print("[CoGe API] %s - WARNING - Delete Experiment id%s failed." % (datetime.now(), str(self.id)))
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

    def add_analysis_parameters(self, parameters):

        def validate_parameter(p):
            if len(p) != 1:
                print("[CoGe API] %s - WARNING - Parameter validation failed for %s. Too many values."
                      % (datetime.now(), p))
                return False

            k = p.keys()[0]
            v = p[k]

            if k == 'read_params': # Done
                supported_read_types = ['single', 'paired']
                supported_encoding = [33, 64]

                read_type = v.get('read_type', 'single')
                encoding = v.get('encoding', 33)

                if read_type not in supported_read_types or encoding not in supported_encoding:
                    print("[CoGe API] %s - WARNING - Failed to add read_params %s. Incorrect specification."
                          % (datetime.now(), p))
                    return False
                else:
                    return {'read_params': {'read_type': read_type, 'encoding': encoding}}

            elif k == 'trimming_params': # Done
                supported_trimmers = ['cutadapt', 'trim_galore']

                trimmer = v.get('trimmer', None)
                cutadapt = v.get('cutadapt', None)
                trimgalore = v.get('trim_galore', None)

                if trimmer not in supported_trimmers:
                    print("[CoGe API] %s - WARNING - Failed to add trimming_params. Trimmer '%s' not supported."
                          % (datetime.now(), trimmer))
                    return False

                elif cutadapt is None and trimgalore is None:
                    return {'trimming_params': {'trimmer': trimmer}}

                elif trimmer == 'cutadapt' and cutadapt is not None:
                    q = cutadapt.get('-q', 25)
                    m = cutadapt.get('-m', 17)
                    return {'trimming_params': {'trimmer': trimmer, 'cutadapt': {'-q': q, '-m': m}}}

                elif trimmer == 'trim_galore' and trimgalore is not None:
                    q = trimgalore.get('-m', 20)
                    l = trimgalore.get('--length', 20)
                    result = {'trimming_params': {'trimmer': trimmer, 'trim_galore': {'-q': q, '--length': l}}}

                    a = trimgalore.get('-a', None)
                    if a is not None:
                        result['trimming_params']['trim_galore']['-a'] = a

                    return result

                else:
                    print("[CoGe API] %s - WARNING - Failed to add trimming_params %s. Incorrect specification."
                          % (datetime.now(), p))
                    return False

            elif k == 'alignment_params': # Done.
                supported_tools = ['gsnap', 'bowtie2', 'tophat2', 'hisat2', 'bismark', 'bwameth']

                tool = v.get('tool', None)
                gsnap = v.get('gsnap', None)
                loadbam = v.get('loadbam', True)

                if tool not in supported_tools:
                    print("[CoGe API] %s - WARNING - Failed to add alignment_params. Tool '%s' not supported."
                          % (datetime.now(), tool))
                    return False
                elif gsnap is None:
                    return {'alignment_params': {'tool': tool,
                                                 'load_bam': loadbam}}
                elif tool == 'gsnap' and gsnap is not None:
                    N = gsnap.get('-N', 1)
                    n = gsnap.get('-n', 5)
                    q = gsnap.get('-Q', True)
                    gapmode = gsnap.get('--gap-mode', 'none')
                    nofails = gsnap.get('--nofails', True)
                    maxmismatches = gsnap.get('--max-mismatches', 2)
                    return {'alignment_params': {'tool': tool,
                                                 'gsnap': {
                                                     '-N': N,
                                                     '-n': n,
                                                     '-Q': q,
                                                     '--gap-mode': gapmode,
                                                     '--nofails': nofails,
                                                     '--max-mismatches': maxmismatches},
                                                 'load_bam': loadbam}}
                else:
                    print("[CoGe API] %s - WARNING - Failed to add alignment_params %s. Incorrect specification."
                          % (datetime.now(), p))
                    return False

            elif k == 'expression_params': # Done
                q = v.get('-Q', None)
                if q is not None:
                    return {'expression_params': {'-Q': q}}
                else:
                    print("[CoGe API] %s - WARNING - Failed to add expression_params %s. Incorrect specification."
                          % (datetime.now(), p))
                    return False

            elif k == 'snp_params': # Done
                supported_methods = ['coge', 'samtools', 'platypus', 'gatk']

                method = v.get('method', None)
                coge = v.get('coge', None)
                samtools = v.get('samtools', None)
                gatk = v.get('gatk', None)

                if method not in supported_methods:
                    print("[CoGe API] %s - WARNING - Failed to add snp_params. Method '%s' not supported."
                          % (datetime.now(), method))
                    return False
                elif coge is None and samtools is None and gatk is None:
                    return {'snp_params': {'method': method}}
                elif method == 'coge' and coge is not None:
                    return {'snp_params': {'method': method,
                                           'coge': {'min-read-depth': coge.get('min-read-depth', 10),
                                                    'min-base-quality': coge.get('min-base-quality', 20),
                                                    'min-allele-count': coge.get('min-allele-count', 4),
                                                    'min-allele-freq': coge.get('min-allele-freq', 0.1),
                                                    'scale': coge.get('scale', 32)}}}
                elif method == 'samtools' and samtools is not None:
                    return {'snp_params': {'method': method,
                                           'samtools': {'min-read-depth': samtools.get('min-read-depth', 6),
                                                        'max-read-depth': samtools.get('max-read-depth', 10)}}}
                elif method == 'gatk' and gatk is not None:
                    return {'snp_params': {'method': method,
                                           'gatk': {'-stand_call_conf': gatk.get('-stand_call_conf', 30),
                                                    '-stand_emit_conf': gatk.get('-stand_emit_conf', 10)}}}
                else:
                    print("[CoGe API] %s - WARNING - Failed to add snp_params %s. Incorrect specification."
                          % (datetime.now(), p))
                    return False

            else:
                print("[CoGe API] %s - WARNING - Failed to add analysis parameter for group %s. Group not supported."
                      % (datetime.now(), k))
                return False

        if type(parameters) == dict:
            ks = parameters.keys()
            for k in ks:
                r = validate_parameter({k: parameters[k]})
                if r:
                    self.analysis_parameters.update(r)

        elif type(parameters) == list:
            for p in parameters:
                ks = p.keys()
                for k in ks:
                    r = validate_parameter({k: p[k]})
                    if r:
                        self.analysis_parameters.update(r)
        else:
            print("[CoGe API] %s - WARNING - add_analysis_parameters failed (unrecognized source format %s).\n"
                  "... A single source can be specified as a dict, multiple should be specified either by dict or list."
                  % (datetime.now(), parameters))

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
