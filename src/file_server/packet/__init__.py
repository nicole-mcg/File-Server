from os.path import dirname, basename, isfile
import glob

from .packet_manager import handle_incoming_packet, register_packet
from .packet import Packet