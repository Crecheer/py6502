import processor
import memory

mem = memory.Memory()
cpu = processor.Processor(mem)
cpu.reset()

with open("test.hex") as f:
    # go through every bit and add it in the memory at the correct address
    for l in f:
        # first in line is usually <address>:, for example 0600:
        line = l.split()
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
try:
    cpu.execute_until_stop()
except Exception as e:
    print(e)
# print all flags
print(cpu.flag_b, cpu.flag_d, cpu.flag_i, cpu.flag_c,
      cpu.flag_z, cpu.flag_v, cpu.flag_n, cpu.flag_b, cpu.flag_d)
# print registers
print(cpu.reg_x, cpu.reg_y)
# print accumulator
print(cpu.reg_accumulator)
