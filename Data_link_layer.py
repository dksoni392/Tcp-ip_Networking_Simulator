from switch_2 import *
from Switch import *
import time
from Broadcast import *
from selectiverepeat import *
from stopandwait import *
def Data_link_layer(data3,sourceDevice):
        c3 = int(input("What's your Choice?\n1: HubSwitchHub-Configuration 2: SwitchDevice-Configuration\n"))
        if c3 == 1:
            print()
            print("*******************************************************")
            print("HubSwitchHub-Configuration")

            # Create end devices and hubs
            A = Device("A")
            B = Device("B")
            C = Device("C")
            D = Device("D")
            E = Device("E")
            hub1 = switch_1("hub1")
            hub2 = switch_1("hub2")

            # Connect devices to hubs
            hub1.connect(A)
            hub1.connect(B)
            hub1.connect(C)
            hub2.connect(D)
            hub2.connect(E)

            # Set data for source device
            if sourceDevice not in ["A", "B", "C", "D", "E"]:
                print("Invalid SourceDevice")
                return
            if sourceDevice == "A":
                A.setData(data3)
            elif sourceDevice == "B":
                B.setData(data3)
            elif sourceDevice == "C":
                C.setData(data3)
            elif sourceDevice == "D":
                D.setData(data3)
            elif sourceDevice == "E":
                E.setData(data3)

            # Print devices' data before transmission
            print()
            print("*******************************************************")
            print("DevicesData before Transmission:")
            print("A data before Transmission:", A.data)
            print("B data before Transmission:", B.data)
            print("C data before Transmission:", C.data)
            print("D data before Transmission:", D.data)
            print("E data before Transmission:", E.data)

            # Perform broadcast transmission
            connected_devices = hub1.getConnectedDevices() + hub2.getConnectedDevices()
            broadcast_function(sourceDevice, data3, connected_devices)
            print()
            print("*******************************************************")

            # Determine which hub is transferring the data and which hub is sending the data
            transfer_hub = hub1 if sourceDevice in ["A", "B", "C"] else hub2
            sending_hub = hub1 if transfer_hub == hub2 else hub2

            # Calculate the broadcast domain
            broadcast_domain = len(connected_devices)

            # Calculate the collision domain
            collision_domain = len(hub1.getConnectedDevices()) + len(hub2.getConnectedDevices())

            # Print transfer and sending hub information
            print("Transfer Hub:", transfer_hub.name)
            print("Sending Hub:", sending_hub.name)

            # Print devices' data after transmission
            print("DevicesData after Transmission:")
            print("A data after Transmission:", A.data)
            print("B data after Transmission:", B.data)
            print("C data after Transmission:", C.data)
            print("D data after Transmission:", D.data)
            print("E data after Transmission:", E.data)

            # Calculate and print total time taken for transmission
            time_taken = time.process_time()
            print()
            print("*******************************************************")
            print("Total Time Taken for Transmission:", time_taken)
            print("Broadcast domain =", broadcast_domain, "and Collision domain =", collision_domain)

        elif c3 == 2:
            print("SwitchDevice-Configuration")
            TotDevices = int(input("Give total number of end devices:\n"))
            bridge_count = 0

            SourceDevice2 = int(input("Choose source from 1, 2, 3:\n"))
            print()
            print("*******************************************************")
            destinationDevice2 = int(input("Choose Destination from 1, 2, 3 (shouldn't be the same as Source):\n"))
            print()
            print("*******************************************************")
            print("Data to be transmitted will be", data3, ":\n")
            print()
            print("*******************************************************")
            bridge_count += 1

            if bridge_count == 1:
                # Create switch
                switch = Switch()

            # Create devices and connect them to the switch
                devices = [Device(f"Device {i+1}") for i in range(TotDevices)]
                for i in range(TotDevices):
                    switch.connect(devices[i])

                # Set data for the source device
                sourceDevice2 = devices[SourceDevice2 - 1]
                sourceDevice2.setData(data3)

                # Choose token passing or polling
                c4 = int(input("Choose Token Passing or Polling:\n1: Token Passing 2: Polling\n"))
                c5 = int(input("Choose ARQ Method:\n1: Stop-and-Wait ARQ 2: Selective Repeat ARQ\n"))

                if c4 == 1 and c5 == 1:
                    # Token Passing with Stop-and-Wait ARQ
                    token = None
                    for i in range(len(devices)):
                        if devices[i] == sourceDevice2:
                            token = devices[i]
                            break

                    if token is None:
                        print("Source device is not connected to the switch.")
                        return

                    # Perform token passing
                    start = time.process_time()
                    for i in range(len(data3)):
                        if devices[i % TotDevices] == token:
                            continue
                        devices[i % TotDevices].data += data3[i]
                        print(f"Received frame number: {i+1} at Device {i % TotDevices + 1}")

                    time_taken = time.process_time() - start
                    print()
                    print("*******************************************************")
                    print("Total Time Taken for Transmission:", time_taken)

                elif c4 == 1 and c5 == 2:
                    # Token Passing with Selective Repeat ARQ
                    window_size = int(input("Enter the window size for Selective Repeat ARQ:\n"))
                    selective_repeat_arq = SelectiveRepeatARQ(window_size)

                    # Perform token passing
                    selective_repeat_arq.send_data(data3, devices, sourceDevice2)

                elif c4 == 2 and c5 == 1:
                    # Polling with Stop-and-Wait ARQ
                    start = time.process_time()
                    stop_and_wait_arq = StopAndWaitARQ()

                    # Perform polling
                    for i in range(len(data3)):
                        stop_and_wait_arq.send_data(data3[i], devices, sourceDevice2)
                        print(f"Received frame number: {i+1} at Device {i % TotDevices + 1}")

                    time_taken = time.process_time() - start
                    print()
                    print("*******************************************************")
                    print("Total Time Taken for Transmission:", time_taken)

                elif c4 == 2 and c5 == 2:
                    # Polling with Selective Repeat ARQ
                    window_size = int(input("Enter the window size for Selective Repeat ARQ:\n"))
                    selective_repeat_arq = SelectiveRepeatARQ(window_size)

                    # Perform polling
                    start = time.process_time()
                    for i in range(len(data3)):
                        selective_repeat_arq.send_data(data3[i], devices, sourceDevice2)
                        print(f"Received frame number: {i+1} at Device {i % TotDevices + 1}")

                    time_taken = time.process_time() - start
                    print()
                    print("*******************************************************")
                    print("Total Time Taken for Transmission:", time_taken)

                else:
                    print("Invalid Choice")
                    return

            else:
                print("Invalid Choice")
                return

# Call the function with the appropriate arguments


        else:
            print("Invalid Choice")
            return
            
    