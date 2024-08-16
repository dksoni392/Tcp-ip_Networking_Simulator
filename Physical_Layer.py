from switch_2 import *
def physicalLayer():
        deviceInfo()
        print()
        print("*******************************************************")
        print("Devices we have: A, B, C, D, E")
        sourceDevice = input("Choose SourceDevice:\n")
        print()
        print("*******************************************************")
        if sourceDevice not in ["A", "B", "C", "D", "E"]:
            print("Invalid SourceDevice")
            return
        
        destinationDevice = input("Choose DestinationDevice:\n")
        print()
        print("*******************************************************")
        if destinationDevice not in ["A", "B", "C", "D", "E"]:
            print("Invalid DestinationDevice")
            return
        
        if sourceDevice == destinationDevice:
            print()
            print("*******************************************************")
            print("SourceDevice and DestinationDevice can't be same")
            return
        
        SD_Data = input("SourceDevice Data Input for transmission (In binary format):\n")
        for i in range(len(SD_Data)):
            if SD_Data[i] != '0' and SD_Data[i] != '1':
                print("Invalid Data Format(Please enter in binary format)")
                return

        if sourceDevice == "A":
            A.setData(SD_Data)
        elif sourceDevice == "B":
            B.setData(SD_Data)
        elif sourceDevice == "C":
            C.setData(SD_Data)
        elif sourceDevice == "D":
            D.setData(SD_Data)
        elif sourceDevice == "E":
            E.setData(SD_Data)
        print()
        print("*******************************************************")
        print("DevicesData before Transmission:")
        print("A data before Transmission:", A.data)
        print("B data before Transmission:", B.data)
        print("C data before Transmission:", C.data)
        print("D data before Transmission:", D.data)
        print("E data before Transmission:", E.data)

        c2 = int(input("Choose your Choice:\n1: StarTopologyConnection 2: DedicatedNetworkConnection\n"))
        if c2 == 1:
            if destinationDevice == "A":
                print("The Mac Address Of device is:",A.MACaddress)
                A.setData(SD_Data)
                hb1.store(SD_Data, sourceDevice, A.MACaddress)
            elif destinationDevice == "B":
                print("The Mac Address Of device is:",B.MACaddress)
                B.setData(SD_Data)
                hb1.store(SD_Data, sourceDevice, B.MACaddress)
            elif destinationDevice == "C":
                print("The Mac Address Of device is:",C.MACaddress)
                C.setData(SD_Data)
                hb1.store(SD_Data, sourceDevice, C.MACaddress)
            elif destinationDevice == "D":
                print("The Mac Address Of device is:",D.MACaddress)
                D.setData(SD_Data)
                hb1.store(SD_Data, sourceDevice, D.MACaddress)
            elif destinationDevice == "E":
                print("The Mac Address Of device is:",E.MACaddress)
                E.setData(SD_Data)
                hb1.store(SD_Data, sourceDevice, E.MACaddress)
            
            
        elif c2 == 2:
            if destinationDevice in ["A", "B", "C", "D", "E"]:
                if sourceDevice == "A":
                    A.setData("0")
                elif sourceDevice == "B":
                    B.setData("0")
                elif sourceDevice == "C":
                    C.setData("0")
                elif sourceDevice == "D":
                    D.setData("0")
                elif sourceDevice == "E":
                    E.setData("0")

                if destinationDevice == "A":
                    A.setData(SD_Data)
                elif destinationDevice == "B":
                    B.setData(SD_Data)
                elif destinationDevice == "C":
                    C.setData(SD_Data)
                elif destinationDevice == "D":
                    D.setData(SD_Data)
                elif destinationDevice == "E":
                    E.setData(SD_Data)
        print()
        print("*******************************************************")
        print("DevicesData after Transmission:")
        print("A data after Transmission:", A.data)
        print("B data after Transmission:", B.data)
        print("C data after Transmission:", C.data)
        print("D data after Transmission:", D.data)
        print("E data after Transmission:", E.data)
        
        print()
        print("*******************************************************")
        getMACTable()

        return SD_Data, sourceDevice