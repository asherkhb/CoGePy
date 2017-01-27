__author__ = 'senorrift'

from coge import coge

## Example: help ##
#coge.help()

## Example: get_genome_info, print some info ##
#dog = coge.get_genome_info(7057)
## ... Print some attributes from genome object ##
#print dog.name
#print dog.id
#print dog.chromosome_count
## ... Print all available attributes of the genome object ##
#dog.print_attributes()

## Example: search_genomes ##
#coge.search_organisms("dog")

## Example: get_organism_info ##
#dog = coge.get_organism_info(25934)
#dog.print_attributes()
#print dog.name
#print dog.id
#print dog.description

dog = coge.Genome()
#dog.print_attributes()
#dog.name = "Doge"
#dog.collar = "pink"

#dog.print_attributes()