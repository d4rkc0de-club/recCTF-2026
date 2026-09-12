#include <iostream>
#include <vector>
#include <string>
#include <cstdint>

// --- Opcode Definitions ---
enum Opcode : uint8_t {
    HALT       = 0x00, // Halts execution of the virtual machine.
    LOAD_IMM   = 0x01, // Format: [Opcode, Reg, Imm] -> Loads an 8-bit immediate value into a register.
    LOAD_INPUT = 0x02, // Format: [Opcode, Reg]      -> Loads the next byte from the user input into a register.
    XOR_IMM    = 0x03, // Format: [Opcode, Reg, Imm] -> Performs bitwise XOR on a register with an immediate value.
    ADD_IMM    = 0x04, // Format: [Opcode, Reg, Imm] -> Adds an 8-bit immediate value to a register.
    CMP_IMM    = 0x05, // Format: [Opcode, Reg, Imm] -> Compares a register value with an immediate. Sets Zero Flag if equal.
    JMP        = 0x06, // Format: [Opcode, Addr]     -> Unconditionally jumps to the target instruction address.
    JZ         = 0x07, // Format: [Opcode, Addr]     -> Jumps to the target address if the Zero Flag is set (true).
    JNZ        = 0x08, // Format: [Opcode, Addr]     -> Jumps to the target address if the Zero Flag is clear (false).
    INC        = 0x09, // Format: [Opcode, Reg]      -> Increments the specified register by 1.
    LOAD_MEM   = 0x0A, // Format: [Opcode, Dst, Adr] -> Loads a byte from VM memory[Reg(Adr)] into Reg(Dst).
    CMP_REG    = 0x0B  // Format: [Opcode, R1, R2]   -> Compares Reg(R1) with Reg(R2). Sets Zero Flag if equal.
};

// --- Virtual Machine Class Architecture ---
class VM {
private:
    std::vector<uint8_t> bytecode;
    uint8_t memory[256] = {0};    // 256 bytes of internal data memory
    uint8_t registers[8] = {0};   // 8 General-purpose registers (R0 to R7)
    uint8_t stack[256] = {0};     // Internal stack storage
    uint8_t sp = 0;               // Stack pointer
    size_t pc = 0;                // Program Counter
    bool zero_flag = false;       // Zero status flag for branching
    size_t input_ptr = 0;         // Tracks the current position in the user input string
    std::string input_str;
    bool running = false;

public:
    VM(const std::vector<uint8_t>& code, const std::string& input) 
        : bytecode(code), input_str(input) {}

    // Configures the VM's internal memory space
    void set_memory(size_t addr, uint8_t val) {
        if (addr < 256) {
            memory[addr] = val;
        }
    }

    // Fetches the next byte from bytecode and increments the Program Counter
    uint8_t fetch() {
        if (pc < bytecode.size()) {
            return bytecode[pc++];
        }
        return HALT;
    }

    // Decodes and executes the individual instruction components
    void execute(uint8_t opcode) {
        switch (opcode) {
            case HALT: {
                running = false;
                break;
            }
            case LOAD_IMM: {
                uint8_t reg = fetch();
                uint8_t imm = fetch();
                if (reg < 8) registers[reg] = imm;
                break;
            }
            case LOAD_INPUT: {
                uint8_t reg = fetch();
                uint8_t val = 0;
                if (input_ptr < input_str.length()) {
                    val = static_cast<uint8_t>(input_str[input_ptr++]);
                } else {
                    val = 0; // Null terminator padding if string buffer ends
                    input_ptr++;
                }
                if (reg < 8) registers[reg] = val;
                break;
            }
            case XOR_IMM: {
                uint8_t reg = fetch();
                uint8_t imm = fetch();
                if (reg < 8) registers[reg] ^= imm;
                break;
            }
            case ADD_IMM: {
                uint8_t reg = fetch();
                uint8_t imm = fetch();
                if (reg < 8) registers[reg] += imm;
                break;
            }
            case CMP_IMM: {
                uint8_t reg = fetch();
                uint8_t imm = fetch();
                if (reg < 8) {
                    zero_flag = (registers[reg] == imm);
                }
                break;
            }
            case JMP: {
                uint8_t addr = fetch();
                pc = addr;
                break;
            }
            case JZ: {
                uint8_t addr = fetch();
                if (zero_flag) pc = addr;
                break;
            }
            case JNZ: {
                uint8_t addr = fetch();
                if (!zero_flag) pc = addr;
                break;
            }
            case INC: {
                uint8_t reg = fetch();
                if (reg < 8) registers[reg]++;
                break;
            }
            case LOAD_MEM: {
                uint8_t reg_dest = fetch();
                uint8_t reg_addr = fetch();
                if (reg_dest < 8 && reg_addr < 8) {
                    registers[reg_dest] = memory[registers[reg_addr]];
                }
                break;
            }
            case CMP_REG: {
                uint8_t reg1 = fetch();
                uint8_t reg2 = fetch();
                if (reg1 < 8 && reg2 < 8) {
                    zero_flag = (registers[reg1] == registers[reg2]);
                }
                break;
            }
            default: {
                running = false; // Unknown instruction safeguards execution
                break;
            }
        }
    }

    // Main CPU loop dispatcher
    bool run() {
        running = true;
        pc = 0;
        size_t cycles = 0;
        
        // Loop safety bounds to avoid infinite loop locks
        while (running && pc < bytecode.size() && cycles < 5000) {
            uint8_t op = fetch();
            execute(op);
            cycles++;
        }
        
        // Return verification status stored in R7 (1 = Correct, 0 = Wrong)
        return registers[7] == 1;
    }
};

int main() {
    std::cout << "Enter the flag: ";
    std::string user_input;
    if (!std::getline(std::cin, user_input)) {
        std::cout << "Wrong!\n";
        return 0;
    }

    // --- Obfuscated Bytecode Sequence ---
    // The flag is checked iteratively through a small loops structure.
    std::vector<uint8_t> vm_bytecode = {
        // [Offset 0] Setup the loop character offset counter (R1 = 0)
        LOAD_IMM, 1, 0,
        
        // [Offset 3] Verification Loop Core
        LOAD_INPUT, 0,       // R0 = next input byte
        XOR_IMM, 0, 0x5A,    // Transform Step 1: Input XOR 0x5A
        ADD_IMM, 0, 0x23,    // Transform Step 2: Input ADD 0x23
        LOAD_MEM, 2, 1,      // R2 = memory[R1] (Loads correct transformed byte)
        CMP_REG, 0, 2,       // Evaluates transformation against memory target
        JNZ, 37,             // Mismatch detected -> Jump straight to failure routine
        INC, 1,              // Increment tracking loop variable index
        CMP_IMM, 1, 21,      // Checks if all 21 flag characters are handled
        JNZ, 3,              // If R1 != 21, cycle back to the loop start address
        
        // [Offset 26] Post-loop verification (Prevents overly long input strings)
        LOAD_INPUT, 0,       // Checks for existence of trailing chars
        CMP_IMM, 0, 0,       // Should evaluate to 0 if text ends cleanly
        JNZ, 37,             // Found trailing content -> Jump to failure path
        
        // [Offset 33] Success Routine
        LOAD_IMM, 7, 1,      // Assign success outcome code to R7
        HALT,
        
        // [Offset 37] Failure Routine
        LOAD_IMM, 7, 0,      // Assign failure outcome code to R7
        HALT
    };

    // --- Preloaded Obfuscated Target Table ---
    // Derived from transforming the flag: d4rk{VMs_i_l0v3_th3m}
    // Equation used: target[i] = (flag[i] ^ 0x5A) + 0x23
    uint8_t transformed_flag[] = {
        0x61, 0x91, 0x4B, 0x54, 0x44, 0x2F, 0x3A, 0x4C, 0x28, 0x56, 
        0x28, 0x59, 0x8D, 0x4F, 0x8C, 0x28, 0x51, 0x55, 0x8C, 0x5A, 0x4A
    };

    VM vm(vm_bytecode, user_input);

    // Initialise the VM Data Memory Table
    for (size_t i = 0; i < sizeof(transformed_flag); ++i) {
        vm.set_memory(i, transformed_flag[i]);
    }

    // Process implementation sequence inside VM
    if (vm.run()) {
        std::cout << "Correct!\n";
    } else {
        std::cout << "Wrong!\n";
    }

    return 0;
}