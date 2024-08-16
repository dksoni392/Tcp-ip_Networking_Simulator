import random

class Device:
    def __init__(self, name):
        self.name = name
        self.mac_address = self.generate_mac_address()
    
    def generate_mac_address(self):
        mac = [0x00, 0x16, 0x3e,
               random.randint(0x00, 0x7f),
               random.randint(0x00, 0xff),
               random.randint(0x00, 0xff)]
        return ':'.join(map(lambda x: "%02x" % x, mac))


class NetworkLayer:
    def __init__(self):
        self.ipAddressTable = {}
        self.routingTable = {}

    def assignIPAddress(self, device, ip_address):
        self.ipAddressTable[device] = ip_address

    def getIPAddress(self, device):
        return self.ipAddressTable.get(device, None)
    
    def addRoutingEntry(self, network, mask, next_hop):
        self.routingTable[(network, mask)] = next_hop

    def getRoutingTable(self):
        return self.routingTable


class DHCP:
    def __init__(self, network_layer):
        self.networkLayer = network_layer
        self.availableIPs = ["192.168.0.1", "192.168.0.2", "192.168.0.3", "192.168.0.4", "192.168.0.5"]

    def requestIP(self, device):
        if device in self.networkLayer.ipAddressTable:
            return

        if len(self.availableIPs) > 0:
            ip_address = self.availableIPs.pop(0)
            self.networkLayer.assignIPAddress(device, ip_address)
            print(f"Assigned IP address {ip_address} to {device.name}")
        else:
            print(f"No available IP addresses for {device.name}")


class ARP:
    def __init__(self, network_layer):
        self.networkLayer = network_layer
        self.arp_table = {}

    def resolve(self, ip_address):
        for device, ip in self.networkLayer.ipAddressTable.items():
            if ip == ip_address:
                self.arp_table[ip_address] = device.mac_address
                return device.mac_address
        return None


class StaticRouting:
    def __init__(self, network_layer):
        self.networkLayer = network_layer

    def addStaticRoute(self, network, mask, next_hop):
        self.networkLayer.addRoutingEntry(network, mask, next_hop)

    def getStaticRoutes(self):
        return self.networkLayer.getRoutingTable()


class RIPProtocol:
    def __init__(self, network_layer):
        self.networkLayer = network_layer
        self.routingTable = {}

    def updateRoutingTable(self, device, routes):
        self.routingTable[device] = routes

    def getRoutingTable(self):
        return self.routingTable

    def advertiseRoutes(self, device):
        routes = self.routingTable.get(device, {})
        print(f"Routing table advertisement for {device.name}:")
        for destination, nexthop in routes.items():
            print(f"Destination: {destination}, Next Hop: {nexthop}")

    def addRoute(self, device, destination, next_hop):
        if device not in self.routingTable:
            self.routingTable[device] = {}
        self.routingTable[device][destination] = next_hop


# Test Cases
# Create network layer and devices
network_layer = NetworkLayer()
router1 = Device("Router1")
router2 = Device("Router2")
host1 = Device("Host1")
host2 = Device("Host2")

# Create and configure DHCP
dhcp = DHCP(network_layer)
dhcp.requestIP(host1)
dhcp.requestIP(host2)

# Create and configure ARP
arp = ARP(network_layer)
mac1 = arp.resolve("192.168.0.1")
mac2 = arp.resolve("192.168.0.2")

# Create and configure Static Routing
static_routing = StaticRouting(network_layer)
static_routing.addStaticRoute("192.168.1.0", "255.255.255.0", "192.168.0.1")
static_routing.addStaticRoute("192.168.2.0", "255.255.255.0", "192.168.0.2")

# Create and configure RIP Protocol
rip = RIPProtocol(network_layer)
rip.addRoute(router1, "192.168.1.0", "192.168.0.1")
rip.addRoute(router2, "192.168.2.0", "192.168.0.2")
rip.advertiseRoutes(router1)
rip.advertiseRoutes(router2)

# Print routing tables
print("Static Routing Table:", static_routing.getStaticRoutes())
print("RIP Routing Table:", rip.getRoutingTable())
