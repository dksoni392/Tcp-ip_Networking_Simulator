from switch_2 import *
from switch_2 import Device
from CRC import *
from Physical_Layer import physicalLayer
from Data_link_layer import Data_link_layer
from Network_layer import *
from transportLayer import *
from Application_layer import *

def main():
    count="1"
    while(count):
        SD_Data, SourceDevice = physicalLayer()
        print()
        print()
        print("*******************************************************")
        print("Entering into Data Link Layer part\n")
        SD_Data = Data_link_layer(SD_Data, SourceDevice)

        print("*******************************************************")
        print("Entering into Network Layer part\n")
        networkLayer = NetworkLayer()

        ripProtocol = RIPProtocol(networkLayer)

        # Create an instance of the DHCP class and pass the networkLayer instance
        dhcp = DHCP(networkLayer)

        # Assign IP addresses to devices using DHCP
        dhcp.requestIP(A)
        dhcp.requestIP(B)
        dhcp.requestIP(C)
        dhcp.requestIP(D)
        dhcp.requestIP(E)
        ripProtocol.updateRoutingTable(A, {"192.168.0.0": "192.168.0.1"})
        ripProtocol.updateRoutingTable(B, {"192.168.0.0": "192.168.0.2"})

        # Advertise routes
        ripProtocol.advertiseRoutes(A)
        ripProtocol.advertiseRoutes(B)
        # Retrieve IP addresses from the network layer
        ip_address_A = networkLayer.getIPAddress(A)
        ip_address_B = networkLayer.getIPAddress(B)
        ip_address_C = networkLayer.getIPAddress(C)
        ip_address_D = networkLayer.getIPAddress(D)
        ip_address_E = networkLayer.getIPAddress(E)

        print("*******************************************************")
        print("Printing IP Address Table\n")
        
        print("IP Address for Device A:", ip_address_A)
        print("IP Address for Device B:", ip_address_B)
        print("IP Address for Device C:", ip_address_C)
        print("IP Address for Device D:", ip_address_D)
        print("IP Address for Device E:", ip_address_E)

        print("*******************************************************")
        print("Entering into Transport Layer part\n")
        
        transportLayer = TransportLayer()

        # Assign ports to devices
        transportLayer.openPort(A, 8000)
        transportLayer.openPort(B, 9000)
        transportLayer.openPort(C, 7000)
        transportLayer.openPort(D, 6000)
        transportLayer.openPort(E, 5000)

        # Create an instance of the TCP class and pass the transportLayer instance
        tcp = TCP(transportLayer)

        # Establish TCP connections
        tcp.establishConnection(A, B)
        tcp.establishConnection(C, D)
        tcp.establishConnection(D, E)

        # Use Selective Repeat to send data
        data_to_send = ["Frame 1", "Frame 2", "Frame 3", "Frame 4", "Frame 5"]
        print("*******************************************************")
        print("Sending data using Selective Repeat protocol\n")
        tcp.sendSelectiveRepeat(A, B, data_to_send)

        # Simulate receiving data with Selective Repeat
        print("*******************************************************")
        print("Receiving data using Selective Repeat protocol\n")
        tcp.receiveSelectiveRepeat(B, A, len(data_to_send))

        # Close TCP connections
        tcp.closeConnection(A, B)
        tcp.closeConnection(C, D)
        tcp.closeConnection(D, E)

        print("*******************************************************")
        print("Entering into Application Layer part\n")

        # Set the information for Device A
        deviceA = Device("Device A")
        deviceA.setMACaddress("00:00:00:00:00:01")
        deviceA.setData("Hello, World!")
        deviceA.setIPAddress("192.168.0.1")
        deviceA.setPort(5000)

        # Set the information for the destination device (WebServer)
        destination = Device("WebServer")
        destination.setIPAddress("192.168.0.10")
        destination.setPort(80)

        # Set the information for the DNS server
        dns_server = Device("DNS Server")
        dns_server.setIPAddress("192.168.0.20")
        dns_server.setPort(53)

        # Create an application layer
        appLayer = ApplicationLayer(deviceA)

        # Send an HTTP request
        request_type = input("Enter 'http' to send an HTTP request or 'dns' to send a DNS request: ")
        if request_type == 'http':
            appLayer.sendHTTPRequest(destination, "/index.html")
        elif request_type == 'dns':
            # Send a DNS request
            appLayer.sendDNSRequest(dns_server, "www.google.com")
        else:
            print("Invalid Choice")

if __name__ == "__main__":
    main()
