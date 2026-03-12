# 🗺️ SIC Emulator — Implementation Roadmap

This document tracks the planned and completed work for the SIC (Simplified Instructional Computer) Emulator project, built with Python, TDD, and Object-Oriented Design.

---

## ✅ Milestone 0 — Foundation (Complete)

Core emulator infrastructure is in place and fully tested.

| Component | Status | Notes |
|---|---|---|
| `Memory` (32 KB byte-addressable) | ✅ Done | Read/write byte & word, boundary checks |
| `Registers` (A, X, L, PC, SW) | ✅ Done | 24-bit truncation via property setters |
| `Instruction` decoder | ✅ Done | Supports Format 2 (16-bit) & Format 3 (24-bit) |
| `CPU` fetch-decode-execute cycle | ✅ Done | Opcode dispatch table, PC management |
| Instructions: `LDA`, `STA`, `ADD`, `SUB`, `COMP`, `J`, `JEQ` | ✅ Done | Core arithmetic, load/store, and jump |
| Instructions: `RD`, `WD`, `TD` | ✅ Done | I/O device read/write/test |
| Instructions: `SVC`, `LPS` | ✅ Done | Supervisor call & load program status |
| Memory protection & privileged instruction checks | ✅ Done | User/Supervisor mode, interrupt vectors |
| I/O Device simulation (`DeviceManager`, `IODevice`) | ✅ Done | Console, Tape, and Disk devices |
| `Loader` (H, T, M, E records) | ✅ Done | Relocation via Modification records |
| `SICMachine` integration | ✅ Done | Top-level API wiring all components |
| Assembler Pass 1 (Parser, SymbolTable, OpcodeTable, Directives) | ✅ Done | `START`, `END`, `WORD`, `BYTE`, `RESW`, `RESB` |
| SIC/XE register stubs (B, S, T, F) | ✅ Done | Defined in `Registers`; not yet wired to CPU |

---

## 🚧 Phase 1 — Remaining SIC Instructions

**Goal:** Complete the full SIC instruction set so any conforming SIC assembly program can be executed.

| Task | Priority | Notes |
|---|---|---|
| `LDX` (Load Index Register, opcode `0x04`) | High | Load memory word into X register |
| `STX` (Store Index Register, opcode `0x10`) | High | Store X into memory |
| `JSUB` (Jump to Subroutine, opcode `0x48`) | High | Save PC to L, jump to address |
| `RSUB` (Return from Subroutine, opcode `0x4C`) | High | Set PC ← L |
| `TIX` (Test and Increment Index, opcode `0xB8`) | High | Increment X, compare to memory, set SW |
| `JLT` (Jump if Less Than, opcode `0x38`) | Medium | Jump if SW == `'<'` |
| `JGT` (Jump if Greater Than, opcode `0x34`) | Medium | Jump if SW == `'>'` |
| `MUL` (Multiply, opcode `0x20`) | Medium | A ← A × memory |
| `DIV` (Divide, opcode `0x24`) | Medium | A ← A ÷ memory |
| `AND` (Bitwise AND, opcode `0x40`) | Medium | A ← A AND memory |
| `OR` (Bitwise OR, opcode `0x44`) | Medium | A ← A OR memory |
| Unit tests for all new instructions | High | Follow existing TDD patterns in `tests/test_cpu.py` |

---

## 🚧 Phase 2 — Assembler Pass 2 & Object Code Generation

**Goal:** Complete the two-pass assembler so that SIC assembly source can be translated into loadable object code.

| Task | Priority | Notes |
|---|---|---|
| `pass_two.py` module skeleton | High | Mirror structure of `pass_one.py` |
| Instruction object code generation | High | Use SymbolTable from Pass 1 to resolve addresses |
| Forward reference resolution | High | All symbols must be defined by end of Pass 1 |
| Header (H) record generation | High | Program name, start address, length |
| Text (T) record generation | High | Packed hex object bytes, max 30 bytes/record |
| End (E) record generation | High | Execution start address |
| Modification (M) record generation | Medium | Needed for future relocatable output |
| `BYTE` operand encoding (`C'...'` and `X'...'`) | Medium | Character and hex literal support |
| Error reporting (undefined symbols, duplicate labels) | Medium | Clear messages with line numbers |
| Unit tests for Pass 2 output | High | Verify generated H/T/E records byte-for-byte |
| Integration test: assemble → load → run | Medium | Small self-contained SIC program end-to-end |

---

## 🚧 Phase 3 — Integration Testing

**Goal:** Validate the entire pipeline (assemble → load → execute) with realistic SIC programs.

| Task | Priority | Notes |
|---|---|---|
| End-to-end test harness in `tests/test_integration.py` | High | Assemble source, load object code, run, assert output |
| Sample SIC program: sum of array | High | Tests LDA, ADD, STA, TIX, JLT loop |
| Sample SIC program: I/O copy loop | Medium | Tests RD/WD/TD with simulated devices |
| Sample SIC program: subroutine call | Medium | Tests JSUB/RSUB/L register |
| Edge case: program exactly fills memory | Low | Boundary condition test |
| Edge case: assembled code loaded at non-zero address | Medium | Relocation via M records |

---

## 🔮 Phase 4 — SIC/XE Extension

**Goal:** Extend the emulator to support the full SIC/XE architecture.

| Task | Priority | Notes |
|---|---|---|
| Expand memory to 1 MB (20-bit addresses) | High | Update `Memory` and `CPU` address calculations |
| Wire B, S, T registers to CPU | High | Already present in `Registers` |
| Format 1 instructions (1 byte, no operand) | High | e.g., `FIX`, `FLOAT`, `NORM`, `HIO`, `SIO`, `TIO` |
| Format 2 register-to-register instructions | High | e.g., `ADDR`, `SUBR`, `MULR`, `DIVR`, `COMPR`, `TIXR`, `CLEAR`, `RMO`, `SHIFTL`, `SHIFTR` |
| PC-relative addressing (Format 3, `p` bit) | High | Effective address = PC + displacement |
| Base-relative addressing (Format 3, `b` bit) | High | Effective address = B + displacement |
| Indirect addressing (Format 3, `n=1,i=0`) | High | nixbpe flag: computed address is dereferenced — the final EA = memory[computed address] |
| Immediate addressing (Format 3, `n=0,i=1`) | High | nixbpe flag: address field is the operand value itself, no memory access for the operand |
| Format 4 extended addressing (32-bit, `e` bit) | High | 20-bit address field |
| Floating-point register F (48-bit) | Medium | Already defined in `Registers` |
| Floating-point instructions (`ADDF`, `SUBF`, `MULF`, `DIVF`, `COMPF`, `LDF`, `STF`) | Medium | IEEE-754-like 48-bit operations |
| Update Assembler for SIC/XE formats | High | Detect `+` prefix for Format 4, n/i/x/b/p/e flag encoding |
| Update Loader for SIC/XE relocatable programs | Medium | M records already partially supported |
| Unit and integration tests for SIC/XE | High | All new instructions and addressing modes |

---

## 🔮 Phase 5 — Debugger & CLI Interface

**Goal:** Provide a usable interactive interface for running and inspecting SIC/XE programs.

| Task | Priority | Notes |
|---|---|---|
| Command-line runner: `python -m src.machine <object_file>` | High | Load and run a program from a file |
| Step-by-step debugger (`step`, `run`, `break`, `regs`, `mem`) | Medium | Interactive REPL for inspecting machine state |
| Breakpoint support | Medium | Pause execution at a given address |
| Memory dump command | Medium | Hex + ASCII view of a memory range |
| Register display | Medium | Formatted view of all registers and flags |
| Disassembler | Low | Reverse-translate object bytes to mnemonics |
| Symbol map loading for debugger | Low | Show labels alongside addresses during stepping |

---

## 📅 Suggested Delivery Order

```
Phase 1  →  Phase 2  →  Phase 3  →  Phase 4  →  Phase 5
 (SIC        (Pass 2     (E2E          (SIC/XE     (Debugger /
  instrs)     + tests)    tests)        ext.)        CLI)
```

Each phase builds on the previous one. Phases 1–3 complete the standard SIC architecture; Phases 4–5 extend toward a full SIC/XE development environment.
