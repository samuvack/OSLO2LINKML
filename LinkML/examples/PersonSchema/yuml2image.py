import os
import requests
from PIL import Image
from io import BytesIO


def yuml_to_jpg(yuml_code, output_file):
    # Define the yUML API URL
    yuml_url = "https://yuml.me/diagram/scruffy/class/"

    # Encode the YUML code
    yuml_code = yuml_code.encode("utf-8")

    # Send a POST request to yUML API to generate the diagram
    response = requests.post(yuml_url, data={"dsl_text": yuml_code})

    if response.status_code == 200:
        # Read the response content as an image
        image_data = BytesIO(response.content)
        image = Image.open(image_data)

        # Save the image as a JPG file
        image.save(output_file, "JPEG")
        print(f"Image saved as {output_file}")
    else:
        print(
            f"Failed to generate the diagram. Status code: {response.status_code}")
        print(response.text)  # Print the response content for debugging


if __name__ == "__main__":
    yuml_code = """
    [Customer]<>1-orders 0..*>[Order]
    [Order]++1-items 0..*>[LineItem]
    [Order]-[note:Aggregate root of Order{bg:wheat}]
    [Order]-[note:Aggregate root of Order{bg:wheat}]
    [Order]++1-superorder 0..1>[Order]
    [Order]-[note:Root Order{bg:yellow}]
    """

    output_file = "yuml_diagram.jpg"

    yuml_to_jpg('personinfo.txt', output_file)
