import paramiko
import threading
import sys

def run_remote_python_script():
    hostname = "raspberrypi.local"
    username = "maroves"
    password = "1234"

    print("[INFO] Connecting to Raspberry Pi at", hostname, "with username:", username)

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(hostname, username=username, password=password)
        print("[INFO] Successfully connected to Raspberry Pi.")

        # Create a shell channel
        channel = client.invoke_shell()
        print("[INFO] Shell session started.")

        # Navigate to the desired directory and run the Python script
        print("[CMD] cd ~")
        channel.send("cd ~\n")

        print("[CMD] clear")
        channel.send("clear\n")

        print("[CMD] python3 program.py")
        channel.send("python3 program.py\n")

        # Function to continuously read output from the Raspberry Pi
        def read_output():
            while True:
                if channel.recv_ready():
                    output = channel.recv(1024).decode()
                    print(output, end="")

        output_thread = threading.Thread(target=read_output, daemon=True)
        output_thread.start()

        print("[INFO] Press Enter to send Ctrl+C and stop the program.")
        while True:
            key = input()
            if key == "":
                print("[CMD] Sending Ctrl+C to stop the script.")
                channel.send("\x03")  # Send Ctrl+C to stop the script

    except Exception as e:
        print(f"[ERROR] {e}")

    finally:
        print("[INFO] Closing SSH connection.")
        channel.close()
        client.close()
        print("[INFO] Disconnected.")

# Run the script
run_remote_python_script()
