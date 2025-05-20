import paramiko
import subprocess
import cv2
import numpy as np
from keras.models import load_model


# ----------- Step 1: Capture image from Raspberry Pi camera -----------
def capture_image(hostname, username, password, remote_image_path):
    print("[1] Capturing image from Raspberry Pi camera...")

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, username=username, password=password)

    capture_command = f"raspistill -o {remote_image_path}"
    stdin, stdout, stderr = client.exec_command(capture_command)
    stdout.channel.recv_exit_status()

    error = stderr.read().decode()
    client.close()

    if error:
        print("Error capturing image:", error)
        return False
    print("Image captured successfully.")
    return True


# ----------- Step 2: Transfer image from Pi to local machine -----------
def transfer_image(hostname, username, password, remote_image_path, local_image_path):
    print("[2] Transferring image to local machine...")

    pscp_command = [
        "pscp", "-pw", password,
        f"{username}@{hostname}:{remote_image_path}", local_image_path
    ]

    try:
        subprocess.run(pscp_command, check=True)
        print("Image transferred successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print("Image transfer failed:", e)
        return False


# ----------- Step 3: Predict image using local model -----------
def predict_image(local_image_path, model_path, labels_path):
    print("[3] Predicting image...")

    model = load_model(model_path, compile=False)

    with open(labels_path, "r") as f:
        class_names = f.readlines()

    image = cv2.imread(local_image_path)
    if image is None:
        print("Error loading image.")
        return False

    image_resized = cv2.resize(image, (224, 224))
    image_array = np.asarray(image_resized, dtype=np.float32).reshape(1, 224, 224, 3)
    image_array = (image_array / 127.5) - 1

    prediction = model.predict(image_array)
    index = np.argmax(prediction)
    class_name = class_names[index].strip()
    confidence = prediction[0][index]

    print(f"Predicted Class: {class_name}")
    print(f"Confidence: {confidence * 100:.2f}%")

    if class_name == "0 stone":
        print("✅ Stone detected.")
        return True
    else:
        print("❌ Stone not detected.")
        return False


# ----------- Main Function -----------
def main():
    hostname = "raspberrypi.local"
    username = "maroves"
    password = "1234"
    remote_image_path = "Image.jpg"  # Image stored temporarily on Pi
    local_image_path = r"Captured_Image_RPI\Image.jpg"
    model_path = r"Model\keras_model.h5"
    labels_path = r"Model\labels.txt"
    input("Press Enter to start the image capture and prediction process...")
    if capture_image(hostname, username, password, remote_image_path):
        if transfer_image(hostname, username, password, remote_image_path, local_image_path):
            predict_image(local_image_path, model_path, labels_path)
if __name__ == "__main__":
    main()
