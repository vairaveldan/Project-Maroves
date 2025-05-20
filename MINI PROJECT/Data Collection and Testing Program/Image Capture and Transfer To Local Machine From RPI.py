import paramiko
import subprocess
# Read the count in a file "var.txt" and increment it by 1
f=open("var.txt",'r')
var=int(f.read())
f.close()
f=open("var.txt",'w')
var+=1
f.write(f"{var}")
f.close()
# Define SSH credentials and commands
hostname = "raspberrypi.local"
username = "maroves"
password = "1234"  # Replace with your actual password
remote_image = f"sample-{var}.jpg"
local_path = r"DataSets"

try:
    # Step 1: SSH into Raspberry Pi and take a picture
    print("Connecting to Raspberry Pi...")
    
    # Create SSH client
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    # Connect to the Raspberry Pi
    client.connect(hostname, username=username, password=password)
    
    # Step 2: Run raspistill command
    print("Taking picture...")
    command = f"raspistill -o {remote_image}"
    stdin, stdout, stderr = client.exec_command(command)
    stdout.channel.recv_exit_status()  # Wait for command to finish
    
    # Check for errors
    error = stderr.read().decode()
    if error:
        print("Error taking picture:", error)
    else:
        print("Picture taken successfully.")

    # Step 3: Exit the SSH session
    print("Exiting Raspberry Pi...")
    client.close()

    # Step 4: Use pscp to copy the image to the local machine
    print("Transferring image to local machine...")
    pscp_command = ["pscp", "-pw", password, f"{username}@{hostname}:{remote_image}", local_path]
    
    # Run the pscp command
    subprocess.run(pscp_command, check=True)
    print("Image transferred successfully.")

except Exception as e:
    print(f"An error occurred: {e}")
    f=open("var.txt",'w')
    var-=1
    f.write(f"{var}")
    f.close()

finally:
    # Ensure client is closed in case of error
    try:
        client.close()
    except:
        pass