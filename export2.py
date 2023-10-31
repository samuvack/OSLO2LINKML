import json
import yaml


def convert_uml_json_to_linkml(json_filename, yaml_filename):
    with open(json_filename, 'r') as json_file:
        data = json.load(json_file)
        
        text = """id: https://w3id.org/linkml/examples/personinfo
name: personinfo
description: |-
  Information about people, based on [schema.org](http://schema.org)
license: https://creativecommons.org/publicdomain/zero/1.0/
default_curi_maps:
  - semweb_context
imports:
  - linkml:types
prefixes:
  personinfo: https://w3id.org/linkml/examples/personinfo/
  linkml: https://w3id.org/linkml/
  schema: http://schema.org/
  rdfs: http://www.w3.org/2000/01/rdf-schema#
  prov: http://www.w3.org/ns/prov#
  GSSO: http://purl.obolibrary.org/obo/GSSO_
  famrel: https://example.org/FamilialRelations#
  skos: http://www.w3.org/2004/02/skos/core#
  # DATA PREFIXES
  P: http://example.org/P/
  ROR: http://example.org/ror/
  CODE: http://example.org/code/
  GEO: http://example.org/geoloc/
default_prefix: personinfo
default_range: string

emit_prefixes:
  - rdf
  - rdfs
  - xsd
  - skos

"""
        
        intro = {
            'id': 'https://w3id.org/linkml/examples/personinfo',
            'name': 'personinfo',
            'description': 'Converted from UML JSON',
            'prefixes': {
                'schema': 'http://example.org/schema/',
                'linkml': 'https://w3id.org/linkml/',
                'personinfo': 'https://w3id.org/linkml/examples/personinfo',
                'rdfs': 'http://www.w3.org/2000/01/rdf-schema',
                'prov': 'http://www.w3.org/ns/prov',
                'GSSO': 'http://purl.obolibrary.org/obo/GSSO_',
                'famrel': 'https://example.org/FamilialRelations',
                'skos': 'http://www.w3.org/2004/02/skos/core',
            },
            'imports': {
                'linkml': 'types'
            },
            'default_range': 'string',
            'default_prefix': 'personinfo',
        }

        # Create the basic structure for LinkML
        linkml = {
            'classes': {},
            'slots': {}
        }

        # Extract the packagedElement
        packaged_elements = data["xmi:XMI"]["uml:Model"]["packagedElement"]["packagedElement"]

        # Ensure that packaged_elements is a list
        if isinstance(packaged_elements, dict):
            packaged_elements = [packaged_elements]

        # Iterate through the packagedElements and identify UML Classes
        for element in packaged_elements:
            element_type = element.get("@xmi:type")
            if element_type == "uml:Class" or "uml:AssociationClass":
                    test = element.get("packagedElement")
                    if test is None:
                        class_name = element.get("@name")
                        #print(class_name)
                        linkml['classes'][class_name] = {
                            'description': class_name,
                            'slots': []
                        }

                        # If there are owned attributes, add them as slots
                        if "ownedAttribute" in element:
                            attributes = element["ownedAttribute"]
                            # Ensure that attributes is a list
                            if isinstance(attributes, dict):
                                attributes = [attributes]

                            for attr in attributes:
                                if isinstance(attr, dict) and "@name" in attr:
                                    attr_name = attr["@name"]
                                    linkml['classes'][class_name]['slots'].append(
                                        attr_name)

                                    # Add to the slots section
                                    linkml['slots'][attr_name] = {
                                        'description': ''
                                    }
            
        elements = data["xmi:XMI"]["xmi:Extension"]["elements"]["element"]
        for element in elements:
            element_type = element.get("@xmi:type")
            #extra

        # Extract connectors for relationships
        connectors = data["xmi:XMI"]["xmi:Extension"]["connectors"]["connector"]
        for conn in connectors:
            try:
                #print(conn["source"]["model"]["@name"],'-->', conn["target"]["model"]["@name"])
                source_class = conn["source"]["model"]["@name"]
                target_class = conn["target"]["model"]["@name"]
                isNavigable = conn["target"]["modifiers"]["@isNavigable"]
                role = conn["target"]["role"]
                test = role.get("@name")
                if isNavigable == "true":
                    if test is None:
                        # Add to the slots section as a relationship
                        linkml['classes'][source_class] = {
                            'description': source_class, #conn["documentation"]["@value"] if "documentation" in conn and "@value" in conn["documentation"] else '',
                            'is_a': target_class,
                            'slots' : []
                            #'domain': source_class,
                            #'range': target_class
                        }
                        print(target_class)
                        if linkml['classes'].get(target_class) is None:
                            linkml['classes'][target_class] = {
                                # conn["documentation"]["@value"] if "documentation" in conn and "@value" in conn["documentation"] else '',
                                'description': target_class,
                                'slots': []
                                # 'domain': source_class,
                                # 'range': target_class
                            }
                    else:
                        continue
            except KeyError:
                # Handle the case where the key doesn't exist
                continue
                    
                    
        with open(yaml_filename, 'w') as yaml_file:
            yaml_file.write(text)

        with open(yaml_filename, 'a') as yaml_file:
            yaml_file.write(yaml.dump(linkml, default_flow_style=False))


if __name__ == '__main__':
    json_filename = 'persoon.json'  # Replace with your JSON filename
    yaml_filename = 'output.yaml'  # Replace with desired YAML filename
    convert_uml_json_to_linkml(json_filename, yaml_filename)
