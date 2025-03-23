## RISC-V L1 Cache Configuration

# Single-core RISC-V system with L1 instruction and data caches
# The system uses a simple CPU model and a simple memory controller
# The CPU is connected to a DDR3 memory controller
# The system runs a simple "hello world" program
# The system is simulated with the timing memory mode

import os
import argparse
import m5
import m5.debug
from m5.objects import *

m5.util.addToPath("../")

from caches import *
from common import SimpleOpts

# Define the binary
thispath = os.path.dirname(os.path.realpath(__file__))

default_binary = os.path.join(
    thispath,
    "test/hello"
)

SimpleOpts.add_option("binary", nargs="?", default=default_binary)
# SimpleOpts.add_option("--input_file", nargs="?", default=None, help="Input file to replace the keyboard")
# SimpleOpts.add_option("--output_file", nargs="?", default=None, help="Output file")
# SimpleOpts.add_option("file_args", nargs=argparse.REMAINDER, default=None)
args = SimpleOpts.parse_args()

# Define the system
system = System()
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "1GHz"
system.clk_domain.voltage_domain = VoltageDomain()
system.mem_mode = "timing"  # Use timing accesses
system.mem_ranges = [AddrRange("512MiB")]  # Create an address range

# Set the CPU
# system.cpu = RiscvTimingSimpleCPU()
system.cpu = RiscvO3CPU()
system.cpu.ArchISA.riscv_type = "RV32"

# Create an L1 instruction and data cache
system.cpu.icache = L1ICache(args)
system.cpu.dcache = L1DCache(args)

# Connect the instruction and data caches to the CPU
system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)

# Create a memory bus
system.membus = SystemXBar()

# Connect the instruction and data caches to the memory bus
system.cpu.icache.connectBus(system.membus)
system.cpu.dcache.connectBus(system.membus)

# Create the interrupt controller for the CPU
system.cpu.createInterruptController()

# Connect the system up to the membus
system.system_port = system.membus.cpu_side_ports

# Create a DDR3 memory controller
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

system.workload = SEWorkload.init_compatible(args.binary)

# Create a process
process = Process()

# Handle the arguments
# if args.file_args:
#     process.cmd = [args.binary] + args.file_args
# else:
#     process.cmd = [args.binary]

# if args.input_file:
#     process.input = args.input_file

# if args.output_file:
#     output_dir = os.path.dirname(args.output_file)
#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)
#     process.output = args.output_file

process.cmd = [args.binary]

# Set the cpu to use the process as its workload and create thread contexts
system.cpu.workload = process
system.cpu.createThreads()

# set up the root SimObject and start the simulation
root = Root(full_system=False, system=system)
m5.instantiate()

print(f"Beginning simulation!")
exit_event = m5.simulate()
print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")
