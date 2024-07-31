import socket
import re
import logging
from typing import Optional

# Configuration
TCP_PORT = 55555
WOL_PORT = 9
BROADCAST_IP = '255.255.255.255'  # Use the broadcast IP address for Wake-on-LAN

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def validate_mac_address(mac_address: str) -> Optional[str]:
    """Validate and format the MAC address."""
    mac_address = mac_address.replace(':', '').upper()
    if len(mac_address) != 12 or not re.match(r'^[0-9A-F]{12}$', mac_address):
        logging.error(f"Invalid MAC address: {mac_address}")
        return None
    return mac_address

def send_wol_packet(mac_address: str) -> None:
    """Send a Wake-on-LAN packet to the specified MAC address."""
    validated_mac = validate_mac_address(mac_address)
    if not validated_mac:
        return

    # Magic Packet consists of 6 bytes of 0xFF followed by the MAC address repeated 16 times
    packet = b'\xFF' * 6 + (bytes.fromhex(validated_mac) * 16)

    try:
        # Create a UDP socket and send the packet
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            s.sendto(packet, (BROADCAST_IP, WOL_PORT))
            logging.info(f"Sent Wake-on-LAN packet to {validated_mac}")
    except Exception as e:
        logging.error(f"Failed to send Wake-on-LAN packet: {e}")

def listen_for_tcp_packets():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Add this line
        s.bind(('0.0.0.0', TCP_PORT))  # Ensure it's binding to all interfaces
        s.listen()
        logging.info(f"Listening for TCP packets on port {TCP_PORT}")
        
        while True:
            try:
                conn, addr = s.accept()
                with conn:
                    logging.info(f"Connected by {addr}")
                    data = conn.recv(1024).decode().strip()
                    if data:
                        mac_address = re.sub(r'[^a-fA-F0-9:]', '', data)
                        send_wol_packet(mac_address)
            except Exception as e:
                logging.error(f"Error while processing connection: {e}")

if __name__ == "__main__":
    listen_for_tcp_packets()