# SIC Emulator Design Document

## 1. Architectural Overview

The SIC (Simplified Instructional Computer) Emulator is designed as a software simulation of the architecture described in Leland L. Beck's *System Software: An Introduction to System Programming*.

The architecture of the emulator strictly adheres to Object-Oriented Design (OOD) principles. The system is highly modularized, with the physical hardware components of the SIC machine modeled as distinct Python classes. This separation of concerns ensures that the emulator is maintainable, testable, and prepared for future extension to the SIC/XE architecture.

The core of the emulation is orchestrated by the `SICMachine` class, which integrates the CPU, Memory, Registers, and I/O Devices, executing the fetch-decode-execute cycle.

## 2. Core Components

### 2.1 Memory (`src/memory.py`)
- **Responsibility:** Simulates the 32,768-byte byte-addressable memory of the SIC machine.
- **Design Details:**
  - Implemented using a mutable `bytearray` to efficiently manage raw byte storage.
  - Exposes methods for byte-level (`read_byte`, `write_byte`) and word-level (3-byte) access (`read_word`, `write_word`).
  - Implements strict boundary checking. Word accesses spanning beyond the memory boundary raise errors.
  - Ensures values written are strictly 24-bit representations (truncated if larger) and are stored in big-endian format.
  - Employs `memoryview` for optimized word-level access via slice assignments.

### 2.2 Registers (`src/registers.py`)
- **Responsibility:** Manages the CPU registers defined by the SIC architecture (A, X, L, PC, SW) and placeholders for SIC/XE registers (B, S, T, F).
- **Design Details:**
  - Uses a Python descriptor class (`Register`) to enforce bitwise truncation transparently on assignment. Standard registers are restricted to 24 bits, while the Floating-point register (F) is 48 bits.
  - The Status Word (SW) register handles condition codes (ASCII representation), mode bits (Supervisor/User), and interrupt codes via bitwise operations.
  - Enables intuitive syntax for register access and modification (e.g., `cpu.registers.A = value`).

### 2.3 CPU (`src/cpu.py`)
- **Responsibility:** Orchestrates the fetch-decode-execute cycle.
- **Design Details:**
  - Fetches instructions from memory using the address currently stored in the Program Counter (PC).
  - Uses an `opcodes` mapping dictionary to translate 8-bit opcodes into specific handler methods (e.g., `_lda`, `_add`, `_j`).
  - Implements hardware-level protections, such as raising exceptions for unimplemented instructions, restricted operations in User mode, and illegal memory access.

### 2.4 Instruction (`src/instruction.py`)
- **Responsibility:** Encapsulates a single machine instruction word and provides utility methods for decoding its fields.
- **Design Details:**
  - Validates that the raw instruction is within the 24-bit integer limit upon instantiation.
  - Uses `__slots__ = ("_word",)` to minimize memory footprint and optimize attribute access speed.
  - Extracts the opcode, flag bits (X bit for indexed addressing), and the 15-bit address field.
  - Prepares the groundwork for parsing Format 2 (16-bit) and Format 3/4 (24/32-bit) instructions required for SIC/XE.

### 2.5 I/O Devices (`src/devices.py`)
- **Responsibility:** Manages external interactions through simulated hardware devices mapping 8-bit device IDs to implementations.
- **Design Details:**
  - Utilizes a `DeviceManager` to maintain the registry of devices.
  - Defines an `IODevice` base class to specify the interface for operations: `test`, `read`, `write`, and `reset`.
  - Concrete device classes like Console, Tape, and Disk are modeled. Storage devices are implemented with a `FileBackedDevice` using `io.BytesIO` buffers, mimicking raw byte streams.

### 2.6 Loader (`src/loader.py`)
- **Responsibility:** Reads assembled object code formats and loads them into memory.
- **Design Details:**
  - Capable of parsing standard SIC/XE object code records (Header, Text, Modification, End).
  - Handles the relocation of code utilizing Modification (M) records.
  - Exposes robust error handling for malformed object structures.

### 2.7 Assembler (`src/assembler/`)
- **Responsibility:** Converts SIC assembly language source code into intermediate states (Pass One) and ultimately into executable object code (Pass Two, pending).
- **Design Details:**
  - **PassOne:** Scans the assembly file to build the `SymbolTable` and calculates the total program length via the Location Counter (`locctr`).
  - **Parser:** A robust `LineParser` interprets source text to distinguish between labels, mnemonics, operands, and comments.
  - **OpcodeTable:** Provides mnemonic-to-opcode resolution.
  - **DirectiveHandlers:** Employs the Strategy Pattern to decouple parsing logic for specific assembler directives (`START`, `END`, `WORD`, `BYTE`, `RESW`, `RESB`) from the main `PassOne` engine.

### 2.8 Machine Integration (`src/machine.py`)
- **Responsibility:** Serves as the top-level container that wires up the Memory, Registers, CPU, and Device Manager.
- **Design Details:**
  - Acts as the primary API for running tests or external interfaces against the emulator.
  - Implements a generic `step()` method to advance the CPU state and helper functions to bulk-load programs directly into memory or parse complete object codes.

## 3. Key Design Patterns & Principles Applied

1. **Single Responsibility Principle (SRP):** Each class encapsulates a specific functional domain. For example, `Memory` handles only data storage and boundaries, while `CPU` strictly coordinates instruction execution.
2. **Descriptor Pattern:** The `Register` class is a custom Python descriptor, automatically applying 24-bit bounds checking without cluttering the `Registers` class with boiler-plate getter/setter logic.
3. **Strategy Pattern:** `DirectiveHandler` sub-classes define specific behaviors for parsing different assembly directives, making the assembler highly extensible for new pseudo-ops.
4. **Facade Pattern:** `SICMachine` hides the complexities of bootstrapping individual emulator components, presenting a unified interface for operation.

## 4. Extensibility to SIC/XE

The architecture was intentionally built with the upcoming transition to SIC/XE in mind:
- **Expanded Memory & Registers:** The `Memory` module can logically be expanded from 32KB to 1MB. Placeholder properties for extended registers (B, S, T, F) already exist in the `Registers` file.
- **Instruction Decoding:** The `Instruction` object is prepared to handle different length instructions (Format 1 to 4) dynamically. A `FORMAT_MAP` logic hook exists in `CPU.fetch` to adjust the PC based on varying instruction sizes.
- **Addressing Modes:** The decoder is modularized to compute effective addresses, enabling the seamless integration of immediate, indirect, base-relative, and PC-relative addressing.
- **Relocation support:** The `Loader` already supports parsing Modification (M) records, which are fundamental to SIC/XE's dynamically loadable programs.
