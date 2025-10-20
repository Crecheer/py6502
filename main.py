import processor
import memory

mem = memory.Memory()
cpu = processor.Processor(mem)
cpu.reset()

with open("test.hex") as f:
    # go through every bit and add it in the memory at the correct address
    for l in f:
        line = l.split() # first in line is usually <address>:, for example 0600:
        address = 0x0000
        count = 0x0000
        for b in line:
            if b.endswith(":"):
                address = int(b[:-1], 16)
            else:
                ins = int(b, 16)
                loc = address + count
                mem[loc] = ins
                count += 1


print(mem[0])
cpu.pc = 0
cpu.execute_until_stop()
print(cpu.reg_accumulator)

