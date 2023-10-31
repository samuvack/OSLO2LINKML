import json
import xmltodict


def convert_xml_to_json(xml_filename, json_filename):
    with open(xml_filename, 'r') as xml_file:
        xml_content = xml_file.read()
        data_dict = xmltodict.parse(xml_content)
        json_data = json.dumps(data_dict, indent=4)

        with open(json_filename, 'w') as json_file:
            json_file.write(json_data)


if __name__ == '__main__':
    xml_filename = 'persoon.xml'  # Replace with your XML filename
    json_filename = 'output.json'  # Replace with desired JSON filename
    convert_xml_to_json(xml_filename, json_filename)
