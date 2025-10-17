import processor
import memory

mem = memory.Memory()
cpu = processor.Processor(mem)
cpu.reset()
mem[0xFCE2] = 0xA9
mem[0xFCE3] = 0x2A
cpu.execute(2)
print(cpu.reg_accumulator)
print(cpu.reg_y)

