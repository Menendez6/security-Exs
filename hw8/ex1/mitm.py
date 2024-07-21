from netfilterqueue import NetfilterQueue
import scapy.all as scapy

def print_and_accept(pkt):
    print(pkt)
    scapy_packet = scapy.IP(pkt.get_payload())
    if scapy_packet.haslayer(scapy.http.HTTPRequest):
        # Extract the raw data
        data = scapy_packet[scapy.http.HTTPRequest].fields['Unknown_Headers']['secret'.encode()].decode()

        print(data)
    #print(pkt.get_payload())
    pkt.accept()

nfqueue = NetfilterQueue()
nfqueue.bind(1, print_and_accept)
try:
    nfqueue.run()
except KeyboardInterrupt:
    print('')

nfqueue.unbind()

'''

    # Check if the packet has a data payload (e.g., TCP or UDP)
    if scapy_packet.haslayer(scapy.Raw):
        # Extract the raw data
        payload = scapy_packet[scapy.Raw].load

        # Convert the binary data to plaintext (you may need to specify the encoding)
        plaintext_data = payload.decode('utf-8')

        # Print or manipulate the plaintext data as needed
        print("Plaintext data:", plaintext_data)

        # You can modify the payload if desired
        # For example, modify the plaintext data and re-encode it
        modified_data = "Modified: " + plaintext_data
        scapy_packet[scapy.Raw].load = modified_data

        # Set the packet payload to the modified data
        packet.set_payload(bytes(scapy_packet))

    # Accept the packet (forward it)
    packet.accept()

# Create a NetfilterQueue object
nfqueue = NetfilterQueue()

# Bind the queue number and the callback function
nfqueue.bind(1, process_packet)

try:
    # Run the queue
    nfqueue.run()
except KeyboardInterrupt:
    print("Exiting...")
'''