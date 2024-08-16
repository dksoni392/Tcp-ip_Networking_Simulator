import time
class TransportLayer:
    def __init__(self):
        self.portTable = {}
        self.sequence_number = 0  # Initialize sequence number for frames
        self.acknowledgments = {}  # Dictionary to store ACKs for sent frames

    def openPort(self, device, port):
        self.portTable[device] = port

    def getPort(self, device):
        return self.portTable.get(device, None)

    def sendFrame(self, source_device, destination_device, frame_data):
        source_port = self.getPort(source_device)
        destination_port = self.getPort(destination_device)

        if source_port is None or destination_port is None:
            print("Source or destination device does not have an assigned port.")
            return

        print(f"Sending frame from {source_device.name}:{source_port} "
              f"to {destination_device.name}:{destination_port} - Data: {frame_data}")

        # Simulate network delay or other processing time
        time.sleep(1)

        # Store the frame with sequence number
        self.acknowledgments[self.sequence_number] = False

        # Increment sequence number for the next frame
        self.sequence_number += 1

        return self.sequence_number - 1  # Return sequence number of the sent frame

    def receiveACK(self, ack_number):
        if ack_number in self.acknowledgments:
            self.acknowledgments[ack_number] = True
            print(f"Received ACK for frame number: {ack_number}")
        else:
            print(f"Invalid ACK received for frame number: {ack_number}")

    def checkACK(self, frame_number):
        return self.acknowledgments.get(frame_number, False)
class TCP:
    def __init__(self, transport_layer):
        self.transportLayer = transport_layer

    def establishConnection(self, source_device, destination_device):
        source_port = self.transportLayer.getPort(source_device)
        destination_port = self.transportLayer.getPort(destination_device)

        if source_port is None or destination_port is None:
            print("Source or destination device does not have an assigned port.")
            return

        print(f"Establishing TCP connection from {source_device.name}:{source_port} "
              f"to {destination_device.name}:{destination_port}")

    def closeConnection(self, source_device, destination_device):
        source_port = self.transportLayer.getPort(source_device)
        destination_port = self.transportLayer.getPort(destination_device)

        if source_port is None or destination_port is None:
            print("Source or destination device does not have an assigned port.")
            return

        print(f"Closing TCP connection from {source_device.name}:{source_port} "
              f"to {destination_device.name}:{destination_port}")

    def sendSelectiveRepeat(self, source_device, destination_device, data):
        window_size = 3  # Selective Repeat window size
        frame_index = 0
        total_frames = len(data)
        timeout = 5  # Timeout in seconds

        while frame_index < total_frames:
            current_window = []
            for i in range(window_size):
                if frame_index >= total_frames:
                    break
                frame_number = self.transportLayer.sendFrame(source_device, destination_device, data[frame_index])
                current_window.append((frame_number, data[frame_index]))
                frame_index += 1

            # Wait for ACKs or timeout
            start_time = time.time()
            while time.time() - start_time < timeout:
                for frame_number, frame_data in current_window:
                    if self.transportLayer.checkACK(frame_number):
                        print(f"ACK received for frame number: {frame_number}")
                    else:
                        print(f"Timeout: ACK not received for frame number: {frame_number}, retransmitting...")
                        self.transportLayer.sendFrame(source_device, destination_device, frame_data)

    def receiveSelectiveRepeat(self, source_device, destination_device, expected_frames):
        received_frames = []
        expected_sequence_number = 0

        while len(received_frames) < expected_frames:
            # Simulate receiving frames out of order
            frame_number = self.transportLayer.sendFrame(destination_device, source_device, f"Frame {expected_sequence_number}")
            print(f"Received frame with sequence number: {frame_number}")
            
            # Simulate network delay or other processing time
            time.sleep(1)

            # Send ACK for the received frame
            self.transportLayer.receiveACK(frame_number)
            received_frames.append(frame_number)
            expected_sequence_number += 1

        print(f"Received all {expected_frames} frames successfully")

