import cv2  
import numpy as np
from keras.models import load_model

# Function to predict if the image contains a stone
def predict_image(image_path, model_path, labels_path):
    # Load the model
    model = load_model(model_path, compile=False)

    # Load the labels
    with open(labels_path, "r") as f:
        class_names = f.readlines()

    # Load and preprocess the image
    image = cv2.imread(image_path)
    image_resized = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
    image_array = np.asarray(image_resized  , dtype=np.float32).reshape(1, 224, 224, 3)
    image_array = (image_array / 127.5) - 1  # Normalize

    # Predict using the model
    prediction = model.predict(image_array)

    # Get the index of the class with the highest score
    index = np.argmax(prediction)
    confidence_score = prediction[0][index]

    # Get the class name
    class_name = class_names[index].strip()

    # Print prediction
    if class_name == "0 empty":
        print("Stone not detected.")
    else:
        print("Stone detected!")
        print("Class Name:", class_name[2:])
        print("Confidence Score:", str(np.round(confidence_score * 100, 2)) + "%")

# Main Function
def main():
    predict_image("Captured_Image_RPI/Image.jpg", "Model/keras_model.h5", "Model/labels.txt")

if __name__ == "__main__":
    main()
