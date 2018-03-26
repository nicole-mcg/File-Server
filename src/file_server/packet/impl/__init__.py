#This package contains implementations of the file_server.packet.Packet class

from file_server.packet import register_packet


from .idle import IdlePacket
from .file_change import FileChangePacket
from .file_add import FileAddPacket
from .file_delete import FileDeletePacket
from .file_move import FileMovePacket

register_packet(IdlePacket) # 0
register_packet(FileChangePacket) # 1
register_packet(FileAddPacket) # 2
register_packet(FileDeletePacket) # 3
register_packet(FileMovePacket) # 4
