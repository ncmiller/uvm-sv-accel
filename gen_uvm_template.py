#!/usr/bin/python3

import os
import sys

transaction_template = \
"""\
`include "uvm_macros.svh"

class {dut_name}_transaction extends uvm_sequence_item;

  `uvm_object_utils({dut_name}_transaction)

  // Insert fields within each transaction
  // rand bit cmd;
  // rand bit addr;
  // rand int data;

  function new (string name = "");
    super.new(name);
  endfunction

  function string convert2string;
    // Insert code to print transaction here
    // return $sformatf("cmd=%b, addr=%0d, data=%0d", cmd, addr, data);
  endfunction

  function void do_copy(uvm_object rhs);
    {dut_name}_transaction t;
    $cast(t, rhs);

    // Insert code to copy transactions (e.g. copy fields one by one)
    // cmd  = t.cmd;
    // addr = t.addr;
    // data = t.data;
  endfunction

  function bit do_compare(uvm_object rhs, uvm_comparer comparer);
    {dut_name}_transaction t;
    bit status = 1;
    $cast(t, rhs);

    // Insert code to compare transactions
    // status &= (cmd  == t.cmd);
    // status &= (addr == t.addr);
    // status &= (data == t.data);

    return status;
  endfunction

endclass: {dut_name}_transaction
"""

sequencer_template = \
"""\
`include "uvm_macros.svh

class {dut_name}_sequence extends uvm_sequence #({dut_name}_transaction);

  `uvm_object_utils({dut_name}_sequence)

  function new (string name = "");
    super.new(name);
  endfunction

  task body;
    if (starting_phase != null)
      starting_phase.raise_objection(this);

    // Insert code to generate sequences
    // repeat(8)
    //   begin
    //   req = {dut_name}_transaction::type_id::create("req");
    //   start_item(req);
    //   if( !req.randomize() )
    //     `uvm_error("", "Randomize failed")
    //   finish_item(req);
    // end

    if (starting_phase != null)
      starting_phase.drop_objection(this);
  endtask: body

endclass: my_sequence

typedef uvm_sequencer #({dut_name}_transaction) {dut_name}_sequencer;
"""

Makefile_template = \
"""\
UVM_VERBOSITY = UVM_MEDIUM
TEST = {dut_name}_test

all: sim

sim:

"""


def generate_file_from_template(file_to_write, template_string, template_vars):
    filled_in_template = template_string.format(**template_vars)
    with open(file_to_write, 'w') as f:
        f.write(filled_in_template)

def main():
    # Create a dictionary of variables to insert into template strings
    template_vars = {}
    template_vars['dut_name'] = "test"

    files_to_gen = ['Makefile', 'transaction', 'sequencer'] #, 'if', 'driver', 'tb_top', 'test', 'env', 'agent', 'scoreboard', 'monitor', 'sequencer']

    # Create tb directory to store files and cd. If directory exists, warn user and exit.
    tb_dir = template_vars['dut_name'] + '_tb'
    if os.path.exists(tb_dir):
        print("ERROR: Testbench directory \"" + tb_dir + "\" already exists. "
              "Remove or rename the directory and run this script again.")
        sys.exit(-1)
    os.makedirs(tb_dir)
    os.chdir(tb_dir)

    # Generate files
    for f in files_to_gen:
        filename = f
        if f != 'Makefile':
            filename = template_vars['dut_name'] + '_' + f + '.sv'
        generate_file_from_template(filename, eval(f + '_template'), template_vars)

if __name__ == "__main__":
    main()
