import struct

# This class is used for easy writing to and reading from a byte array containing different data types
#       It can be used to create a byte array. E.g buff=ByteBuffer().from_string("hello")
#       It can also be used to read data from a byte array. E.g buff=ByteBuffer(bytes); hello=buff.read_string()
# This class is not designed for one object to be used for reading and writing
class ByteBuffer:

    # b: an option byte array to read from
    def __init__(self, b=b''):
        self._bytes = b
        self._index = 0

        # This holds the length if a byte array was specified
        # otherwise it cannot be counted on
        self._size = len(b)

        # Verify that b is a byte array
        if not isinstance(b, bytes):
            raise AssertionError("Argument must be type `bytes`")

    # Gets the length of the buffer
    def __len__(self):
        return max(self._size, self._index)

    # Returns true we haven't reached the end of the data
    def has_left(self):
        return self._size > self._index

    # Writes a byte to the buffer
    # b: the data to write. This can be a list of bytes, a bytes object, or a single byte
    # signed: whether the byte should be written as signed
    # Returns the byte array that has been written
    def write(self, b, signed=False):

        # Format data given
        fmt = "b" if signed else "B"
        if (isinstance(b, list)):
            length = len(b)
            _bytes = struct.pack(fmt * len(b), b)
        elif (isinstance(b, bytes)):
            length = len(b)
            _bytes = b
        else:
            length = 1
            _bytes = struct.pack(fmt, b)

        # Add the data to the buffer
        self._bytes += _bytes
        self._index += length

        return _bytes

    # Writes a bool the the buffer
    # b: the bool to write (True/False)
    # Returns the byte written
    def write_bool(self, b):
        return self.write(1 if b else 0)

    # Writes a 32-bit integer to the buffer
    # i: the integer to write
    # signed: if true, the integer will be written as signed
    # Returns the byte array that has been writter
    def write_int(self, i, signed=True):

        # Format the data
        fmt = "i" if signed else "I"
        b = struct.pack(fmt, i)

        # Add the data to the buffer
        self._bytes += b
        self._index += 4

        return b

    # Writes a string to the buffer
    # Adds a trailing string terminator ('\0')
    # s: the string to write
    # Returns the bytes written
    def write_string(self, s):

        # Add null terminator
        s += '\0'

        # Format data
        b = s.encode('utf-8')

        # Add data to the buffer
        self._bytes += b
        self._index += len(b)

        return b

    # Reads a byte from the buffer
    # signed: If true, the byte is read as signed
    # Returns the byte read
    def read(self, signed=False):

        # We've reached the end of the buffer prematurely
        if (self._index >= len(self._bytes)): #TODO throw error
            return None

        # Format data
        fmt = "b" if signed else "B"
        b = struct.unpack_from(fmt, self._bytes, self._index)

        # Move to next data in buffer
        self._index += 1

        return b[0]

    # Reads a bool from the buffer
    # Returns the bool read
    def read_bool(self):
        return self.read() == 1

    # Reads a 32-bit integer from the buffer
    # signed: If true, the integer is read as signed
    def read_int(self, signed=True):

        # We've reached the end of the stream prematurely
        if (self._index >= len(self._bytes)): #TODO throw error
            return None

        i = struct.unpack_from("i" if signed else "I", self._bytes, self._index)
        self._index += 4

        #print("Read int: {}".format(i[0]))
        return i[0]

    # Reads a string from the buffer
    # Return the string read, not including the null terminator
    def read_string(self):

        # Build string
        # Keep reading characters until we find a null terminator "\0"
        b = b""
        c = self.read(True)
        while c != 0:
            b += bytes(chr(c), 'utf-8')
            c = self.read(True)

        # Turn the bytes into a string
        return b.decode('utf-8')

    # Converts the ByteBuffer to a byte array
    def bytes(self):
        return bytes(self._bytes)

    # Creates a ByteBuffer with one bool written
    # For convenience
    @staticmethod
    def from_bool(b):
        buff = ByteBuffer()
        buff.write_bool(b)
        return buff

    # Creates a ByteBuffer with one int written
    # For convenience
    @staticmethod
    def from_int(i):
        buff = ByteBuffer()
        buff.write_int(i)
        return buff

    # Creates a ByteBuffer with one string written
    # For convenience
    @staticmethod
    def from_string(s):
        buff = ByteBuffer()
        buff.write_string(s)
        return buff