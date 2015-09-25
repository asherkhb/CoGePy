import requests
# import pprint

__author__ = 'asherkhb'

# ~Base API URLs~ #
base = "https://genomevolution.org/coge/api/v1/"  # CoGe
# base = "http://geco.iplantc.org/coge/api/v1"    # GeCo

# TODO: Make a "lock" decorator that can lock classes and prevent users from adding inappropriate attributes
# def lock(cls):
#     attributes = cls.print_attributes()
#     print attributes

def help():
    current_services = ["search_organisms",
                        "get_organism_info",
                        "search_genomes",
                        "get_genome_info"]
    current_classes = ["Organism", "Genome"]

    print "Welcome to the CoGe Web Services API"
    print "\nCurrent supported services are: "
    for i, service in enumerate(current_services):
        print "    %d. %s" % ((i+1), service)
    print "\nCurrent supported classes are:"
    for i, cls in enumerate(current_classes):
        print "    %d. %s" % ((i+1), cls)
    print "    HINT: For a list of attributes in a class, use 'class_name.print_attributes()'"
    print "\nFor additional help, visit http://genomevolution.org"


def search_organisms(search_term):
    # TODO: Add check to ensure valid search term
    r = base + "organisms/search/%s" % str(search_term)
    g = requests.get(r)
    results = g.json()["organisms"]
    print 'Search for "%s" returned %d results.' % (str(search_term), len(results))
    for n, result in enumerate(results):
        print "> Search Result %d" % (n+1)
        print "\tName:%s\n\tid: %s\n\tDescription:%s" % (result["name"], str(result["id"]), result["description"])
    # return results


def get_organism_info(oid):
    r = base + "organisms/%s" % str(oid)
    g = requests.get(r)
    organism = Organism(g.json())
    return organism


def get_genome_info(gid):
    r = base + "genomes/%s" % str(gid)
    g = requests.get(r)
    genome = Genome(genomeObject=g.json())
    return genome


class Organism:
    def __init__(self, organismObject):
        self.name = organismObject["name"]
        self.id = organismObject["id"]
        self.description = organismObject["description"]
        # TODO: Add genomes once API supports it
        # self.genomes = organismObject["genomes"]

    def print_attributes(self):
        attributes = self.__dict__.keys()
        print attributes

# @lock
class Genome:
    def __init__(self, genomeObject=None):
        if genomeObject:
            self.id = genomeObject["id"]
            self.name = genomeObject["organism"]["name"]
            self.version = genomeObject["version"]
            self.restricted = genomeObject["restricted"]

            self.description = genomeObject["organism"]["description"]
            self.organism_id = genomeObject["organism"]["id"]

            self.chromosome_count = genomeObject["chromosome_count"]
            self.chromosomes = genomeObject["chromosomes"]

            self.sequence_type = genomeObject["sequence_type"]["name"]
            self.experiments = genomeObject["experiments"]
            self.additional_metadata = genomeObject["additional_metadata"]

    def print_attributes(self):
        attributes = self.__dict__.keys()
        print attributes


