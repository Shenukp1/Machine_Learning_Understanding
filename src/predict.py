"""
Original Author: Jonathan Hudson
CPSC 433 F26

This files is used in the case that interactive.py does not work. It also does
enforce reproducibility in the sense we have to use grabimage.py to make an image.
then that image can be used to predict.

IMPORTANT(shenukp1) Nov 13, 2026: The first argument (i.e., MNIST or notMNIST ) determines the classname and data
that is fetched. In our case, we only care about the notMNIST.

TODO(shenukp1) Nov 13, 2026: Displaying all the images in the image directory, then choosing based on input number

Usage:
     ```bash
     $ python predict.py <MNIST,notMNIST>
     ```

Example Usage:
     ```bash
     $ python predict.py notMNIST
     ```
NOTE(shenukp1) Nov 13, 2026: You will be prompted to choose the model, image, and capital letter (A-J), which is mapped to 0-9.

"""


import os
import sys
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import pyscreenshot as ImageGrab
from constant import MODEL_DIR, IMAGE_DIR

def main():
     class_names = check_args()
     print(f"--Load Model {sys.argv[2]}--")
     # Load the model that should be in sys.argv[2]
     # see<https://www.tensorflow.org/api_docs/python/tf/keras/models/load_model>
     model = tf.keras.models.load_model(sys.argv[2])
     print(f"--Load Image {sys.argv[3]}--")
     img = plt.imread(sys.argv[3])
     if np.amax(img.flatten()) > 1:
          img = img/255
     img = 1 - img
     print(f"--Predict as Class {sys.argv[4]}--")
     predict(model, class_names, img, int(sys.argv[4]))

def predict(model, class_names, img, true_label):
    img = np.array([img])
    # TODO(shenukp1) Nov 13, 2026: Replace these two lines with code to make a prediction
  
    prediction = [1/10,1/10,1/10,1/10,1/10,1/10,1/10,1/10,1/10,1/10]
    # TODO(shenukp1) Nov 13, 2026: Determine what the predicted label is
    predicted_label = 0
    plot(class_names, prediction, true_label, predicted_label, img[0])
    plt.show()

VALID_LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]

def select_model():
     """A function to make it easier for us to choose a model.
     """
     if not os.path.exists(MODEL_DIR):
          print(f"Model directory '{MODEL_DIR}' does not exist!")
          sys.exit(1)

     models = sorted([f for f in os.listdir(MODEL_DIR) if f.endswith(".keras")])
     if not models:
          print(f"No .keras models found in '{MODEL_DIR}'!")
          sys.exit(1)

     print("--Available Models--")
     for idx, name in enumerate(models, start=1):
          print(f"{idx}: {name}")

     choice = input("Select a model (number): ").strip()
     if not choice.isdigit() or not (1 <= int(choice) <= len(models)):
          print(f"Invalid selection: must be a number between 1 and {len(models)}")
          sys.exit(1)

     return os.path.join(MODEL_DIR, models[int(choice) - 1])

def select_image():
     """A function to make it easier for us to choose an image.
     """
     if not os.path.exists(IMAGE_DIR):
          print(f"Image directory '{IMAGE_DIR}' does not exist!")
          sys.exit(1)

     # Only grab .png files named <A-J>.png
     images = sorted([
          f for f in os.listdir(IMAGE_DIR)
          if f.endswith(".png") and f.split(".")[0] in VALID_LETTERS
     ])
     if not images:
          print(f"No .png images found in '{IMAGE_DIR}'!")
          sys.exit(1)

     print("--Available Images--")
     for idx, name in enumerate(images, start=1):
          print(f"{idx}: {name}")

     choice = input("Select an image (number): ").strip()
     if not choice.isdigit() or not (1 <= int(choice) <= len(images)):
          print(f"Invalid selection: must be a number between 1 and {len(images)}")
          sys.exit(1)

     return os.path.join(IMAGE_DIR, images[int(choice) - 1])

def letter_to_index(image_path):
     """Parses the [A-J] prefix from the image filename and converts it to 0-9.
     """
     filename = os.path.basename(image_path)
     letter = filename.split(".")[0]

     if letter not in VALID_LETTERS:
          print(f"Invalid letter '{letter}': must be a capital letter from A to J")
          sys.exit(1)

     # Convert 'A' -> '0', ..., 'J' -> '9' as a string for sys.argv[4]
     return str(VALID_LETTERS.index(letter))

def check_args():
     if(len(sys.argv) == 1): # Seems like by default we look at the MNIST, changed to notMNIST
         print("No arguments so using defaults to `notMNIST`.")
         model_path = select_model()
         img_path = select_image()
         sys.argv = ["predict.py", "notMNIST", model_path, img_path, letter_to_index(img_path)]
     elif(len(sys.argv) == 2): # Inserting model, image, and letter index so we do not have to type them in CLI
         # These will exit if we dont get a model or an image
         model_path = select_model()
         img_path = select_image()
         sys.argv.extend([model_path, img_path, letter_to_index(img_path)])
     if(len(sys.argv) != 5):
          print("Usage python predict.py <MNIST,notMNIST>")
          sys.exit(1)
     if sys.argv[1] == "MNIST":
          print("--Dataset MNIST--")
          class_names = list(range(10))
     elif sys.argv[1] == "notMNIST":
          print("--Dataset notMNIST--")
          class_names = ["A","B","C","D","E","F","G","H","I","J"]
     else:
          print(f"Choose MNIST or notMNIST, not {sys.argv[1]}")
          sys.exit(2)
     if sys.argv[2][-6:] != ".keras":
          print(f"{sys.argv[2]} is not a keras extension")
          sys.exit(1)
     if sys.argv[3][-4:] != ".png":
          print(f"{sys.argv[3]} is not a png extension")
          sys.exit(1)
     img = plt.imread(sys.argv[3])
     if len(img.shape) != 2:
          print("Image is not grey scale!")
          sys.exit(4)
     if img.shape != (28,28):
          print("Image is not 28 by 28!")
          sys.exit(4)
     if not sys.argv[4].isdigit():
          print(f"{sys.argv[4]} is not an integer (0-9)")
          sys.exit(1)
     if int(sys.argv[4]) < 0 or int(sys.argv[4]) > 9 :
          print(f"{sys.argv[4]} is not an integer (0-9)")
          sys.exit(1)
     return class_names

def plot(class_names, prediction, true_label, predicted_label, img):
    plt.figure(figsize=(6,3))
    plt.subplot(1,2,1)
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])
    plt.imshow(img, cmap=plt.cm.binary)
    predicted_label = np.argmax(prediction)
    if predicted_label == true_label:
        color = 'blue'
    else:
        color = 'red'
    plt.xlabel("{} {:2.0f}% ({})".format(class_names[predicted_label],100*np.max(prediction),class_names[true_label]),color=color)
    plt.subplot(1,2,2)
    plt.grid(False)
    plt.xticks(range(10))
    plt.yticks([])
    thisplot = plt.bar(class_names, prediction, color="#777777")
    plt.ylim([0, 1])
    thisplot[predicted_label].set_color('red')
    thisplot[true_label].set_color('blue')

if __name__ == "__main__":
    main()
