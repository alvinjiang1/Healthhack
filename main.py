import os

passkey = "/Users/alvin/Desktop/Healthhack/team-fath-f9cf4023f0e5.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = passkey

def detect_text(path):
    """Detects text in the file."""
    from google.cloud import vision

    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print("Texts:")

    for text in texts:
        print(f'\n"{text.description}"')

        vertices = [
            f"({vertex.x},{vertex.y})" for vertex in text.bounding_poly.vertices
        ]

        # print("bounds: {}".format(",".join(vertices)))

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )
    return texts

    
# print(detect_text("/Users/alvin/Desktop/Healthhack/2024-01-24 08.18.58.jpg"))

filepath = "output.txt"
with open(filepath, "w") as file:
    # Call detect_text and extract the text from the protobuf message
    result = detect_text("/Users/alvin/Desktop/Healthhack/2024-01-24 08.18.58.jpg")

    text = ""
    for line in result:
        text += f'\n"{line.description}"'
    
    file.write(text)