import struct

class ByteBuffer:
    def __init__(self, b=b''):
        self._bytes = b
        self._index = 0
        self._size = len(b)
        if not isinstance(b, bytes):
            raise AssertionError("Argument must be type `bytes`")

    #Gets the current size in bytes
    def __len__(self):
        return max(self._size, self._index)

    def has_left(self):
        return self._size > self._index

    # Writes a byte to the buffer
    # Writes an unsigned byte by default
    def write(self, b, signed=False):
        fmt = "b" if signed else "B"
        if (isinstance(b, list)):
            _bytes = struct.pack(fmt * len(b), b)
        elif (isinstance(b, bytes)):
            _bytes = b
        else:
            _bytes = struct.pack(fmt, b)
        self._bytes += _bytes
        self._index += 1
        return _bytes

    # Writes a bool the the buffer
    def write_bool(self, b):
        return self.write(1 if b else 0)

    # Writes a 32-bit integer to the buffer
    # Writes a signed integer by default
    def write_int(self, i, signed=True):
        fmt = "i" if signed else "I"
        bytes = struct.pack(fmt, i)
        self._bytes += bytes
        self._index += 4
        #print("Write int: {}".format(i))
        return bytes

    # Writes a string to the buffer
    def write_string(self, s):
        s += '\0'
        b = s.encode('utf-8')
        self._bytes += b
        self._index += len(b)
        #print("write string: {}".format(s))

    # Reads a byte from the buffer
    # Unsigned by default
    def read(self, signed=False):
        if (self._index >= len(self._bytes)): #TODO throw error
            return None
        fmt = "b" if signed else "B"
        b = struct.unpack_from(fmt, self._bytes, self._index)
        self._index += 1
        return b[0]

    # Reads a bool from the buffer
    def read_bool(self):
        return self.read() == 1

    # Reads a 32-bit integer from the buffer
    # Signed by default
    def read_int(self, signed=True):
        if (self._index >= len(self._bytes)): #TODO throw error
            return None
        i = struct.unpack_from("i" if signed else "I", self._bytes, self._index)
        self._index += 4

        #print("Read int: {}".format(i[0]))
        return i[0]

    # Reads a string from the buffer
    def read_string(self):
        b = b""
        c = self.read(True)
        while c != 0:
            b += bytes(chr(c), 'utf-8')
            c = self.read(True)

        #print("Read string: {}".format(b.decode('utf-8')))
        return b.decode('utf-8')

    # Converts to binary
    def bytes(self):
        return bytes(self._bytes)

    @staticmethod
    def from_bool(b):
        buff = ByteBuffer()
        buff.write_bool(b)
        return buff

    @staticmethod
    def from_int(i):
        buff = ByteBuffer()
        buff.write_int(i)
        return buff

    @staticmethod
    def from_string(s):
        buff = ByteBuffer()
        buff.write_string(s)
        return buff