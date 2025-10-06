import processor
import memory

mem = memory.Memory()
cpu = processor.Processor(mem)
cpu.reset()
mem[0xFCE2] = 0xEA
mem[0xFCE3] = 0x18
cpu.execute(3)
print(cpu.flag_c)

