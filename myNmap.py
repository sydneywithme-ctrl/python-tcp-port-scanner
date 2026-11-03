#Imports Python's socket module so the program can create network connections and test TCP ports.
import socket
#Imports sys so the program can read the IP address entered on the command line.
import sys
#Imports subprocess so Python can run the Windows ping command.
import subprocess

#Checks if a TCP port is open on the target host. It creates a socket, sets a timeout, and attempts to connect to the specified port. If the connection is successful (returns 0), the port is considered open; otherwise, it is closed.
def check_port(host, port):
    scanner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    scanner.settimeout(0.05)

    connection = scanner.connect_ex((host, port))
    scanner.close()

    return connection == 0
#checks if the provided IP address is valid. It uses socket.inet_aton to validate the IP address format. If the IP address is valid, it returns True; otherwise, it returns False.
def valid_ip(ip_address):
    try:
        socket.inet_aton(ip_address)
        return True
    except socket.error:
        return False
#checks if the target IP address is reachable by sending a single ping request. It uses subprocess.run to execute the ping command and suppresses the output. If the ping command returns a success code (0), the IP address is considered reachable; otherwise, it is not.
def is_reachable(ip_address):
    result = subprocess.run(
        ["ping", "-n", "1", "-w", "1000", ip_address],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return result.returncode == 0
#Makes sure the user provided an IP address as a command line argument. If not, it prints an error message and exits the program. It also validates the provided IP address and checks if it is reachable before proceeding with the port scanning.
if len(sys.argv) < 2:
    print("Provide an IP address as a command line argument.")
    print("Example: python3 myNmap.py 127.0.0.1")
    sys.exit()

target_ip = sys.argv[1]
#gets and checks the IP address provided as a command line argument. It validates the IP address format and checks if the target IP address is reachable before proceeding with the TCP port scanning.
if not valid_ip(target_ip):
    print("Error: Invalid IP address provided.")
    sys.exit(1)

if not is_reachable(target_ip):
    print("Error: The IP address is not reachable.")
    sys.exit(1)

print("TCP Port Scanner")
print("Target:", target_ip)
print("---------------------------")

open_ports = []
#scans TCP ports from 1 to 3400 on the target IP address. For each port, it calls the check_port function to determine if the port is open. If a port is open, it adds it to the open_ports list and prints a message indicating that the port is open.
for port in range(1, 3401):
    if check_port(target_ip, port):
        open_ports.append(port)
        print("Port", port, "is open.")
#displays a summary of the scanning results. It prints a separator line and then checks if any open TCP ports were found. If no open ports were found, it prints a message indicating that no open TCP ports were found. Otherwise, it prints the total number of open TCP ports found.
print("---------------------------")

if len(open_ports) == 0:
    print("No open TCP ports found.")
else:
    print('Total open TCP ports found:', len(open_ports))
