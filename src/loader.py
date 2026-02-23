class Loader:
    """
    Implements an Object Code Loader for the SIC Emulator.
    Supports Header (H), Text (T), End (E), and Modification (M) records.
    """

    def __init__(self, machine):
        """
        Initializes the loader with a reference to the SIC machine.

        Args:
            machine: An instance of SICMachine.
        """
        self.machine = machine

    def load(self, object_code: str, load_address: int = None):
        """
        Parses and loads SIC object code into the machine's memory.

        Args:
            object_code: A string containing the object code lines.
            load_address: Optional address to load the program at. If provided,
                         relocation will be performed using this as the base address.
        """
        lines = object_code.strip().split('\n')
        program_base_address = 0
        actual_base_address = 0
        relocation_offset = 0

        for line in lines:
            line = line.strip()
            if not line:
                continue

            record_type = line[0]

            if record_type == 'H':
                # H^progname^startaddr^length
                # H: 1, Name: 2-7, Start: 8-13, Length: 14-19
                # program_name = line[1:7].strip()
                program_base_address = int(line[7:13], 16)
                # program_length = int(line[13:19], 16)

                if load_address is not None:
                    actual_base_address = load_address
                    relocation_offset = actual_base_address - program_base_address
                else:
                    actual_base_address = program_base_address
                    relocation_offset = 0

            elif record_type == 'T':
                # T^startaddr^length^objcode
                # T: 1, Start: 2-7, Length: 8-9, Code: 10-69
                start_addr = int(line[1:7], 16)
                length = int(line[7:9], 16)
                obj_code_hex = line[9:]

                target_address = start_addr + relocation_offset

                for i in range(0, length * 2, 2):
                    byte_val = int(obj_code_hex[i:i+2], 16)
                    self.machine.memory.write_byte(target_address + (i // 2), byte_val)

            elif record_type == 'M':
                # M^startaddr^length^flag^symbol
                # M: 1, Start: 2-7, Length: 8-9, Flag: 10, Symbol: 11-16
                if load_address is not None:
                    start_addr = int(line[1:7], 16)
                    length_half_bytes = int(line[7:9], 16)
                    modification_flag = line[9]

                    target_address = start_addr + relocation_offset

                    if length_half_bytes == 6:
                        current_val = self.machine.memory.read_word(target_address)
                        if modification_flag == '+':
                            new_val = (current_val + relocation_offset) & 0xFFFFFF
                        elif modification_flag == '-':
                            new_val = (current_val - relocation_offset) & 0xFFFFFF
                        else:
                            new_val = current_val
                        self.machine.memory.write_word(target_address, new_val)
                    elif length_half_bytes == 5:
                        # Handle 20-bit address modification
                        b1 = self.machine.memory.read_byte(target_address)
                        b2 = self.machine.memory.read_byte(target_address + 1)
                        b3 = self.machine.memory.read_byte(target_address + 2)

                        val = (b1 << 16) | (b2 << 8) | b3
                        addr_part = val & 0xFFFFF

                        if modification_flag == '+':
                            addr_part = (addr_part + relocation_offset) & 0xFFFFF
                        elif modification_flag == '-':
                            addr_part = (addr_part - relocation_offset) & 0xFFFFF

                        val = (val & 0xF00000) | addr_part

                        self.machine.memory.write_byte(target_address, (val >> 16) & 0xFF)
                        self.machine.memory.write_byte(target_address + 1, (val >> 8) & 0xFF)
                        self.machine.memory.write_byte(target_address + 2, val & 0xFF)

            elif record_type == 'E':
                # E^startaddr
                # E: 1, Start: 2-7
                if len(line) >= 7:
                    exec_start_addr = int(line[1:7], 16)
                    self.machine.registers.PC = exec_start_addr + relocation_offset
                else:
                    self.machine.registers.PC = actual_base_address
