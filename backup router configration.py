import paramiko
import time

def cisco_copy_running_config(hostname, username, password, enable_password):
    # Hardcoded TFTP server and filename
    tftp_server = "10.10.0.2"
    tftp_filename = "backup_router1"

    # Create an SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the router using provided credentials
        ssh.connect(hostname, username=username, password=password, allow_agent=False, look_for_keys=False)

        # Create a shell channel for interaction
        channel = ssh.invoke_shell()

        # Wait for the prompt after connecting
        time.sleep(1)
        output = channel.recv(65535).decode('utf-8')
        print(output)

        # Check if login was successful by looking for '#' or '>'
        if '#' in output or '>' in output:
            # Send the 'enable' command to enter privileged mode
            channel.send("enable\n")
            time.sleep(1)

            # Send the enable password
            channel.send(enable_password + "\n")
            time.sleep(1)

            # Check if the prompt indicates successful enable mode
            enable_output = channel.recv(65535).decode('utf-8')
            print(enable_output)

            # Check if '#' is present in enable mode prompt
            if '#' in enable_output:
                print("Login successful! Entered privilege mode.")

                # Copy running config to TFTP server
                channel.send(f"copy running-config tftp://{tftp_server}/{tftp_filename}\n")
                time.sleep(1)  # Adjust the sleep time as needed

                channel.send(f"\n")
                time.sleep(1)  # Adjust the sleep time as needed                

                channel.send(f"\n")
                time.sleep(1)  # Adjust the sleep time as needed                

                # Check if the copy was successful
                copy_output = channel.recv(65535).decode('utf-8')
                print(copy_output)

            else:
                print("Enable mode failed!")
                print("Login failed!")

        else:
            print("Login failed!")

        # Close the SSH connection
        ssh.close()

    except Exception as e:
        # Handle exceptions and print an error message
        print(f"Error: {e}")
        print("Copy failed!")

# Entry point of the script
if __name__ == "__main__":
    # Replace these values with your router's information
    router_hostname =input("pleaser enter router ip :"+" ")
    router_username =input("please enter username:"+" ")
    router_enable_password =input("please enter router password:"+" ")
    router_password =input("please enter privilage password:"+" ")
    

    # Call the function to copy running config to TFTP server
    cisco_copy_running_config(router_hostname, router_username, router_password, router_enable_password)