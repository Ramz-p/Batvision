

import requests
import cv2
import numpy as np
from io import BytesIO
import base64


def rgb_to_grayscale(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray_image


def colorize_image(image):
    url = "https://api.deepai.org/api/colorizer"
    headers = {'Api-Key': 'YOURAPIKEYHERE'}

    try:
        # Encode image to base64
        _, img_encoded = cv2.imencode('.jpg', image)
        image_data = BytesIO(img_encoded)
        image_base64 = base64.b64encode(image_data.getvalue()).decode('utf-8')

        # Make request to DeepAI API
        response = requests.post(url, data={'image': image_base64}, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes

        # Decode base64 response to image
        response_json = response.json()
        output_url = response_json['output_url']
        colored_image_data = requests.get(output_url).content
        colored_image = cv2.imdecode(np.frombuffer(colored_image_data, np.uint8), cv2.IMREAD_COLOR)

        # Check if the returned image is valid
        if colored_image is not None and colored_image.shape[0] > 0 and colored_image.shape[1] > 0:
            return colored_image
        else:
            print("Error: Unable to colorize the image. Returned image is invalid.")
            return None
    except (requests.exceptions.RequestException, KeyError) as e:
        print("Error: Unable to colorize the image.", e)
        return None



def main():
    choice = input("Enter '1' for RGB to grayscale or '2' for grayscale to RGB: ")

    if choice == '1':
        image_path = input("Enter the path to the RGB image: ")
        rgb_image = cv2.imread(image_path)
        grayscale_image = rgb_to_grayscale(rgb_image)
        cv2.imshow("Grayscale Image", grayscale_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    elif choice == '2':
        image_path = input("Enter the path to the grayscale image: ")
        grayscale_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        colored_image = colorize_image(grayscale_image)
        cv2.imshow("Colored Image", colored_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Invalid choice. Please enter either '1' or '2'.")


if __name__ == "__main__":
    main()
