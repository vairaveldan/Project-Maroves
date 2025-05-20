import paramiko
import threading
import subprocess
import sys
import cv2
import numpy as np
from keras.models import load_model

# ---------- Program 1: Interactive run on Pi with Ctrl+C on Enter ----------
def run_program_1_on_pi():
    hostname = "raspberrypi.local"
    username = "maroves"
    password = "1234"

    print("Running program.py interactively on Raspberry Pi...")

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, username=username, password=password)

    channel = client.invoke_shell()
    channel.send("python3 program.py\n")

    def read_output():
        while True:
            if channel.recv_ready():
                output = channel.recv(1024).decode()
                print(output, end="")

    output_thread = threading.Thread(target=read_output, daemon=True)
    output_thread.start()

    try:
        while True:
            key = input()
            if key == "":
                channel.send("\x03")  # Send Ctrl+C
    except KeyboardInterrupt:
        print("Interrupted by user.")
    finally:
        channel.close()
        client.close()


# ---------- Program 2: Image processing pipeline ----------
def capture_image_from_pi(hostname, username, password, remote_image):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, username=username, password=password)

    print("Taking picture...")
    command = f"raspistill -o {remote_image}"
    stdin, stdout, stderr = client.exec_command(command)
    stdout.channel.recv_exit_status()

    error = stderr.read().decode()
    client.close()

    if error:
        print("Error taking picture:", error)
        return False
    print("Picture taken successfully.")
    return True


def transfer_image(hostname, username, password, remote_image, local_path):
    print("Transferring image to local machine...")
    pscp_command = ["pscp", "-pw", password, f"{username}@{hostname}:{remote_image}", local_path]
    subprocess.run(pscp_command, check=True)
    print("Image transferred successfully.")


def predict_image(image_path, model_path, labels_path):
    model = load_model(model_path, compile=False)
    with open(labels_path, "r") as f:
        class_names = f.readlines()

    image = cv2.imread(image_path)
    image_resized = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
    image_array = np.asarray(image_resized, dtype=np.float32).reshape(1, 224, 224, 3)
    image_array = (image_array / 127.5) - 1

    prediction = model.predict(image_array)
    index = np.argmax(prediction)
    class_name = class_names[index].strip()
    confidence_score = prediction[0][index]

    if class_name == "0 stone":
        print(class_name)
        print("Stone detected!")
        print("Confidence Score:", str(np.round(confidence_score * 100, 2)) + "%")
        return True
    else:
        print("Stone not detected.")
        return False


def main():
    hostname = "raspberrypi.local"
    username = "maroves"
    password = "1234"
    remote_image = "image.jpg"
    local_path = r"Captured_Image_RPI\Image.jpg"
    model_path = r"Model\keras_model.h5"
    labels_path = r"Model\labels.txt"

    input("Press Enter to take a picture with the Raspberry Pi camera...")

    if capture_image_from_pi(hostname, username, password, remote_image):
        transfer_image(hostname, username, password, remote_image, local_path)

        if predict_image(local_path, model_path, labels_path):
            print("Calling Program 1 to run on Raspberry Pi...")
            run_program_1_on_pi()


if __name__ == "__main__":
    main()
