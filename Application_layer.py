import socket

class ApplicationLayer:
    def __init__(self, device):
        self.device = device

    def sendHTTPRequest(self, destination, path):
        print("Entering sendHTTPRequest function")

        try:
            # Create a socket for communication
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Connect to the destination device using its IP address and port
            destination_ip = "192.168.0.10"  # Hardcoded IP address of the destination
            destination_port = 80  # Hardcoded port of the destination
            sock.connect((destination_ip, destination_port))

            # Send the HTTP request
            request = f"GET {path} HTTP/1.1\r\nHost: {destination_ip}\r\n\r\n"
            sock.sendall(request.encode())

            # Receive the response from the destination device
            response = sock.recv(1024).decode()

            # Print the response
            print(f"Received response from {destination.getName()}: {response}")

        except ConnectionRefusedError:
            print(f"Connection refused: Unable to connect to {destination.getName()}")

        except Exception as e:
            print(f"An error occurred while sending the HTTP request to {destination.getName()}: {str(e)}")

        finally:
            # Close the socket
            sock.close()

        print("Exiting sendHTTPRequest function")

    def sendDNSRequest(self, dns_server, hostname):
        print("Entering sendDNSRequest function")

        try:
            # Create a socket for communication
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            # Send the DNS request to the DNS server
            dns_server_ip = "192.168.0.20"  # Hardcoded IP address of the DNS server
            dns_server_port = 53  # Hardcoded port of the DNS server
            request = f"{hostname}"
            sock.sendto(request.encode(), (dns_server_ip, dns_server_port))

            # Receive the DNS response from the DNS server
            response, _ = sock.recvfrom(1024)
            response = response.decode()

            # Print the DNS response
            print(f"Received DNS response from {dns_server.getName()}: {response}")

        except Exception as e:
            print(f"An error occurred while sending the DNS request to {dns_server.getName()}: {str(e)}")

        finally:
            # Close the socket
            sock.close()

        print("Exiting sendDNSRequest function")
