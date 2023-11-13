import requests

def convert_yuml_to_uml(file_path, output_path='uml_diagram.png'):
    # Lees de YUML-inhoud uit het bestand
    with open(file_path, 'r') as file:
        yuml_content = file.read()

    output_path = "test.svg"
    # Maak de volledige URL met de YUML-inhoud
    diagram_url = yuml_content

    # Verstuur het verzoek naar de yUML API
    response = requests.get(diagram_url)

    # Controleer of het verzoek succesvol was
    if response.status_code == 200:
        # Sla de afbeelding op
        with open(output_path, 'wb') as file:
            file.write(response.content)
        print(f"UML-diagram succesvol opgeslagen als {output_path}")
    else:
        print("Er is een fout opgetreden bij het aanmaken van het UML-diagram")

# Gebruik het script
convert_yuml_to_uml('yuml.yuml')


