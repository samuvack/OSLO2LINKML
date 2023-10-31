import json
import yaml


def convert_uml_json_to_linkml(json_filename, yaml_filename):
    with open(json_filename, 'r') as json_file:
        data = json.load(json_file)

        # Create the basic structure for LinkML
        linkml = {
            'id': 'http://example.org/schema/MySchema',
            'name': 'MySchema',
            'description': 'Converted from UML JSON',
            'prefixes': {
                'schema': 'http://example.org/schema/'
            },
            'classes': {}
        }

        # Extract the packagedElement
        packaged_elements = data["xmi:XMI"]["uml:Model"]["packagedElement"]["packagedElement"]

        # Ensure that packaged_elements is a list
        if isinstance(packaged_elements, dict):
            packaged_elements = [packaged_elements]

        # Iterate through the packagedElements and identify UML Classes
        for element in packaged_elements:
            element_type = element.get("@xmi:type")
            if element_type == "uml:Class":
                class_name = element.get("@name")
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
                            linkml['classes'][class_name]['slots'].append(
                                attr["@name"])

        with open(yaml_filename, 'w') as yaml_file:
            yaml_file.write(yaml.dump(linkml, default_flow_style=False))


if __name__ == '__main__':
    json_filename = 'persoon.json'  # Replace with your JSON filename
    yaml_filename = 'output.yaml'  # Replace with desired YAML filename
    convert_uml_json_to_linkml(json_filename, yaml_filename)
