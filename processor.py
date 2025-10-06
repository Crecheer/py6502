import memory
import sys

class Processor:

    ADDRESSING = [
        # 0      1      2      3      4     5      6      7      8       9     A      B       C      D     E      F
        "imp", "inx", "imp", "inx", "zp",  "zp",  "zp",  "zp",  "imp", "imm", "acc", "imm", "abs", "abs", "abs", "abs",  # 0
        "rel", "iny", "imp", "iny", "zpx", "zpx", "zpx", "zpx", "imp", "aby", "imp", "aby", "abx", "abx", "abx", "abx",  # 1
        "abs", "inx", "imp", "inx", "zp",  "zp",  "zp",  "zp",  "imp", "imm", "acc", "imm", "abs", "abs", "abs", "abs",  # 2
        "rel", "iny", "imp", "iny", "zpx", "zpx", "zpx", "zpx", "imp", "aby", "imp", "aby", "abx", "abx", "abx", "abx",  # 3
        "imp", "inx", "imp", "inx", "zp",  "zp",  "zp",  "zp",  "imp", "imm", "acc", "imm", "abs", "abs", "abs", "abs",  # 4
        "rel", "iny", "imp", "iny", "zpx", "zpx", "zpx", "zpx", "imp", "aby", "imp", "aby", "abx", "abx", "abx", "abx",  # 5
        "imp", "inx", "imp", "inx", "zp",  "zp",  "zp",  "zp",  "imp", "imm", "acc", "imm", "ind", "abs", "abs", "abs",  # 6
        "rel", "iny", "imp", "iny", "zpx", "zpx", "zpx", "zpx", "imp", "aby", "imp", "aby", "abx", "abx", "abx", "abx",  # 7
        "imm", "inx", "imm", "inx", "zp",  "zp",  "zp",  "zp",  "imp", "imm", "imp", "imm", "abs", "abs", "abs", "abs",  # 8
        "rel", "iny", "imp", "iny", "zpx", "zpx", "zpy", "zpy", "imp", "aby", "imp", "aby", "abx", "abx", "aby", "aby",  # 9
        "imm", "inx", "imm", "inx", "zp",  "zp",  "zp",  "zp",  "imp", "imm", "imp", "imm", "abs", "abs", "abs", "abs",  # A
        "rel", "iny", "imp", "iny", "zpx", "zpx", "zpy", "zpy", "imp", "aby", "imp", "aby", "abx", "abx", "aby", "aby",  # B
        "imm", "inx", "imm", "inx", "zp",  "zp",  "zp",  "zp",  "imp", "imm", "imp", "imm", "abs", "abs", "abs", "abs",  # C
        "rel", "iny", "imp", "iny", "zpx", "zpx", "zpx", "zpx", "imp", "aby", "imp", "aby", "abx", "abx", "abx", "abx",  # D
        "imm", "inx", "imm", "inx", "zp",  "zp",  "zp",  "zp",  "imp", "imm", "imp", "imm", "abs", "abs", "abs", "abs",  # E
        "rel", "iny", "imp", "iny", "zpx", "zpx", "zpx", "zpx", "imp", "aby", "imp", "aby", "abx", "abx", "abx", "abx",  # F
    ]

    OPCODES = [
        # 0      1      2     3      4       5     6       7      8      9     A       B      C     D       E      F
        "brk", "ora", "nop", "slo", "nop", "ora", "asl", "slo", "php", "ora", "asl", "nop", "nop", "ora", "asl", "slo",  # 0
        "bpl", "ora", "nop", "slo", "nop", "ora", "asl", "slo", "clc", "ora", "nop", "slo", "nop", "ora", "asl", "slo",  # 1
        "jsr", "and", "nop", "rla", "bit", "and", "rol", "rla", "plp", "and", "rol", "nop", "bit", "and", "rol", "rla",  # 2
        "bmi", "and", "nop", "rla", "nop", "and", "rol", "rla", "sec", "and", "nop", "rla", "nop", "and", "rol", "rla",  # 3
        "rti", "eor", "nop", "sre", "nop", "eor", "lsr", "sre", "pha", "eor", "lsr", "nop", "jmp", "eor", "lsr", "sre",  # 4
        "bvc", "eor", "nop", "sre", "nop", "eor", "lsr", "sre", "cli", "eor", "nop", "sre", "nop", "eor", "lsr", "sre",  # 5
        "rts", "adc", "nop", "rra", "nop", "adc", "ror", "rra", "pla", "adc", "ror", "nop", "jmp", "adc", "ror", "rra",  # 6
        "bvs", "adc", "nop", "rra", "nop", "adc", "ror", "rra", "sei", "adc", "nop", "rra", "nop", "adc", "ror", "rra",  # 7
        "nop", "sta", "nop", "sax", "sty", "sta", "stx", "sax", "dey", "nop", "txa", "nop", "sty", "sta", "stx", "sax",  # 8
        "bcc", "sta", "nop", "nop", "sty", "sta", "stx", "sax", "tya", "sta", "txs", "nop", "nop", "sta", "nop", "nop",  # 9
        "ldy", "lda", "ldx", "lax", "ldy", "lda", "ldx", "lax", "tay", "lda", "tax", "nop", "ldy", "lda", "ldx", "lax",  # A
        "bcs", "lda", "nop", "lax", "ldy", "lda", "ldx", "lax", "clv", "lda", "tsx", "lax", "ldy", "lda", "ldx", "lax",  # B
        "cpy", "cmp", "nop", "dcp", "cpy", "cmp", "dec", "dcp", "iny", "cmp", "dex", "nop", "cpy", "cmp", "dec", "dcp",  # C
        "bne", "cmp", "nop", "dcp", "nop", "cmp", "dec", "dcp", "cld", "cmp", "nop", "dcp", "nop", "cmp", "dec", "dcp",  # D
        "cpx", "sbc", "nop", "isb", "cpx", "sbc", "inc", "isb", "inx", "sbc", "nop", "sbc", "cpx", "sbc", "inc", "isb",  # E
        "beq", "sbc", "nop", "isb", "nop", "sbc", "inc", "isb", "sed", "sbc", "nop", "isb", "nop", "sbc", "inc", "isb",  # F
    ]

    def __init__(self, mem: memory.Memory) -> None:
        self.memory = mem
        self.reg_accumulator = 0
        self.reg_x = 0
        self.reg_y = 0

        self.pc = 0
        self.sp = 0
        self.cycles = 0

        # flags of status register
        self.flag_c = True # carry flag
        self.flag_z = True # zero flag
        self.flag_i = True # interrupt enable / disable flag
        self.flag_d = False # decimal mode flag,
        self.flag_b = True # break flag
        self.flag_unused = True # unused, always set true
        self.flag_v = True # overflow flag
        self.flag_n = True # negative flag

    def reset(self) -> None:
        # reset processor
        self.pc = 0xFCE2 # starting point of program counter
        self.sp = 0x01FD # starting point of stack pointer
        self.cycles = 0
        self.flag_i = True
        self.flag_d = False
        self.flag_b = True

    def read_byte(self, address: int) -> int:
        data = self.memory[address]
        self.cycles += 1 # reading byte takes 1 cycle in the real processor
        return data

    def write_byte(self, address: int, value: int) -> None:
        self.memory[address] = value
        self.cycles += 1 # writing also takes 1 cycle irl

    def read_word(self, address: int) -> int:
        if sys.byteorder == "little":
            data = self.read_byte(address) | (self.read_byte(address + 1) << 8)
        else:
            data = (self.read_byte(address) << 8) | self.read_byte(address + 1)
        return data

    def write_word(self, address: int, value: int) -> int:
        if sys.byteorder == "little":
            self.write_byte(address, value & 0xFF)
            self.write_byte(address + 1, (value >> 8) & 0xFF)
        else:
            self.write_byte(address, (value >> 8) & 0xFF)
            self.write_byte(address + 1, value & 0xFF)

    def fetch_byte(self) -> int:
        data = self.read_byte(self.pc)
        self.pc += 1
        return data

    def fetch_word(self) -> int:
        data = self.read_word(self.pc)
        self.pc += 2
        return data

    def read_register(self, register) -> int:
        self.cycles += 1
        match register:
            case "a":
                return self.reg_accumulator
            case "x":
                return self.reg_x
            case "y":
                return self.reg_y

    def push_stack(self, data: int) -> None:
        self.memory[self.sp] = data
        self.cycles += 1
        self.sp -= 1

    def pop_stack(self) -> int:
        self.cycles += 1
        dataTemp = self.memory[self.sp]
        self.sp += 1
        return dataTemp

    def eval_flag(self, data: int, flag) -> None:
        match flag:
            case "n":
                self.flag_n = (data & 0x80) != 0
            case "z":
                if data == 0:
                    self.flag_z = True
                else:
                    self.flag_z = False


    def execute(self, cycles: int = 0):
        while(self.cycles < cycles) or (cycles == 0):
            opcode = self.fetch_byte()
            try: eval("self.ins_" + self.OPCODES[opcode] + "_" + self.ADDRESSING[opcode] + "()")
            except AttributeError: print("non implemented instruction")
    def ins_nop_imp(self) -> None:
        # no operation
        self.cycles += 1

    def ins_clc_imp(self) -> None:
        # clear carry flag
        self.flag_c = False
        self.cycles += 1

    def ins_cld_imp(self) -> None:
        # clear decimal mode
        self.flag_d = False
        self.cycles += 1

    def ins_cli_imp(self) -> None:
        # clear interrupt disable
        self.flag_i = False
        self.cycles += 1

    def ins_dec_zp(self) -> None:
        # decrement memory zero page
        address = self.fetch_byte()
        self.write_byte(address, self.read_byte(address) - 1)
        self.eval_flag(self.memory[address], "n")
        self.eval_flag(self.memory[address], "z")
        self.cycles += 1

    def ins_dec_zpx(self) -> None:
        # decrement memory, zero page x
        address = (self.fetch_byte() + self.read_register("x")) & 0xFF
        self.write_byte(address, self.read_byte(address) - 1)
        self.eval_flag(self.memory[address], "n")
        self.eval_flag(self.memory[address], "z")
        self.cycles += 1

    def ins_dec_abs(self) -> None:
        # decrement memory absolute
        address = self.fetch_word()
        self.write_byte(address, self.read_byte(address) - 1)
        self.eval_flag(self.memory[address], "n")
        self.eval_flag(self.memory[address], "z")
        self.cycles += 1

    def ins_inc_zp(self) -> None:
        # increment memory zero page
        address = self.fetch_byte()
        self.write_byte(address, self.read_byte(address) + 1)
        self.eval_flag(self.memory[address], "n")
        self.eval_flag(self.memory[address], "z")
        self.cycles += 1

    def ins_inc_zpx(self) -> None:
        # increment memory, zero page x
        address = (self.fetch_byte() + self.read_register("x")) & 0xFF
        self.write_byte(address, self.read_byte(address) + 1)
        self.eval_flag(self.memory[address], "n")
        self.eval_flag(self.memory[address], "z")
        self.cycles += 1

    def ins_inc_abs(self) -> None:
        # increment memory absolute
        address = self.fetch_word()
        self.write_byte(address, self.read_byte(address) + 1)
        self.eval_flag(self.memory[address], "n")
        self.eval_flag(self.memory[address], "z")
        self.cycles += 1

    def ins_dex_imp(self) -> None:
        # decrement x register
        self.reg_x = self.read_register("x") - 1
        self.eval_flag(self.reg_x, "n")
        self.eval_flag(self.reg_x, "z")

    def ins_dey_imp(self) -> None:
        # decrement y register
        self.reg_y = self.read_register("y") - 1
        self.eval_flag(self.reg_y, "n")
        self.eval_flag(self.reg_y, "z")


    def ins_inx_imp(self) -> None:
        # increment x register
        self.reg_x = self.read_register("x") + 1
        self.eval_flag(self.reg_x, "n")
        self.eval_flag(self.reg_x, "z")

    def ins_iny_imp(self) -> None:
        # increment y register
        self.reg_y = self.read_register("y") - 1
        self.eval_flag(self.reg_y, "n")
        self.eval_flag(self.reg_y, "z")

    def ins_lda_imm(self) -> None:
        # load accumulator immediate
        self.reg_accumulator = self.fetch_byte()
        self.eval_flag(self.reg_accumulator, "n")
        self.eval_flag(self.reg_accumulator, "z")

    def ins_lda_zp(self) -> None:
        # load accumulator zero page
        self.reg_accumulator = self.read_byte(self.fetch_byte())
        self.eval_flag(self.reg_accumulator, "n")
        self.eval_flag(self.reg_accumulator, "z")

    def ins_lda_zpx(self) -> None:
        # load accumulator zero page x
        self.reg_accumulator = self.read_byte((self.fetch_byte() + self.read_register("x")) & 0xFF)
        self.eval_flag(self.reg_accumulator, "n")
        self.eval_flag(self.reg_accumulator, "z")

    def ins_lda_abs(self) -> None:
        # load accumulator absolute
        self.reg_accumulator = self.read_byte(self.fetch_word())
        self.eval_flag(self.reg_accumulator, "n")
        self.eval_flag(self.reg_accumulator, "z")

    def ins_lda_abx(self) -> None:
        # load accumulator absolute x
        self.reg_accumulator = self.read_byte(self.fetch_word() + self.reg_x)
        self.eval_flag(self.reg_accumulator, "n")
        self.eval_flag(self.reg_accumulator, "z")

    def ins_lda_aby(self) -> None:
        # load accumulator absolute y
        self.reg_accumulator = self.read_byte(self.fetch_word() + self.reg_y)
        self.eval_flag(self.reg_accumulator, "n")
        self.eval_flag(self.reg_accumulator, "z")

    def ins_lda_inx(self) -> None:
        # load accumulator indexed indirect
        self.reg_accumulator = self.read_byte(self.read_word(((self.fetch_byte() + self.reg_x) & 0xFF)))
        self.eval_flag(self.reg_accumulator, "n")
        self.eval_flag(self.reg_accumulator, "z")

    def ins_lda_iny(self) -> None:
        self.reg_accumulator = self.read_byte(self.read_word(self.fetch_byte()) + self.reg_y)
        self.eval_flag(self.reg_accumulator, "n")
        self.eval_flag(self.reg_accumulator, "z")

    def ins_ldx_imm(self) -> None:
        # load x reg immediate
        self.reg_x = self.fetch_byte()
        self.eval_flag(self.reg_x, "n")
        self.eval_flag(self.reg_x, "z")

    def ins_ldx_zp(self) -> None:
        # load x reg zero page
        self.reg_x = self.read_byte(self.fetch_byte())
        self.eval_flag(self.reg_x, "n")
        self.eval_flag(self.reg_x, "z")

    def ins_ldx_zpy(self) -> None:
        # load reg x zero page y
        self.reg_x = self.read_byte((self.fetch_byte() + self.read_register("x")) & 0xFF)
        self.eval_flag(self.reg_x, "n")
        self.eval_flag(self.reg_x, "z")

    def ins_ldx_abs(self) -> None:
        # load reg x absolute
        self.reg_x = self.read_byte(self.fetch_word())
        self.eval_flag(self.reg_x, "n")
        self.eval_flag(self.reg_x, "z")

    def ins_ldx_aby(self) -> None:
        # load reg x absolute y
        self.reg_x = self.read_byte(self.fetch_word() + self.reg_y)
        self.eval_flag(self.reg_x, "n")
        self.eval_flag(self.reg_x, "z")

    def ins_ldy_imm(self) -> None:
        # load y reg immediate
        self.reg_y = self.fetch_byte()
        self.eval_flag(self.reg_y, "n")
        self.eval_flag(self.reg_y, "z")

    def ins_ldy_zp(self) -> None:
        # load y reg zero page
        self.reg_y = self.read_byte(self.fetch_byte())
        self.eval_flag(self.reg_y, "n")
        self.eval_flag(self.reg_y, "z")

    def ins_ldy_zpx(self) -> None:
        # load reg y zero page x
        self.reg_y = self.read_byte((self.fetch_byte() + self.read_register("x")) & 0xFF)
        self.eval_flag(self.reg_y, "n")
        self.eval_flag(self.reg_y, "z")

    def ins_ldy_abs(self) -> None:
        # load reg y absolute
        self.reg_y = self.read_byte(self.fetch_word())
        self.eval_flag(self.reg_y, "n")
        self.eval_flag(self.reg_y, "z")

    def ins_ldy_abx(self) -> None:
        # load reg y absolute x
        self.reg_y = self.read_byte(self.fetch_word() + self.reg_x)
        self.eval_flag(self.reg_y, "n")
        self.eval_flag(self.reg_y, "z")

    def ins_sec_imp(self) -> None:
        # set carry flag
        self.flag_c = True
        self.cycles += 1

    def ins_sed_imp(self) -> None:
        # set decimal mode
        self.flag_d = True
        self.cycles += 1

    def ins_sei_imp(self) -> None:
        # set interrupt mode
        self.flag_i = True
        self.cycles += 1
