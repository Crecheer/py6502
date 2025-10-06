class Memory:
    def __init__(self, size: int = 65536):
        self.size = size
        # make memory array
        self.memory = [0] * size
        print(len(self.memory))
    def __getitem__(self, address: int) -> int:
        # get value at the address
        return self.memory[address]

    def __setitem__(self, address: int, value: int) -> int:
        # sets value at address
        if value.bit_length() > 8:
            raise ValueError("value is too big, needs to be 8 bits max")
        self.memory[address] = value
        return self.memory[address]
    