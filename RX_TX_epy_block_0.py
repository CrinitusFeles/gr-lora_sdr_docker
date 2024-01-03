"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, out0_key='', out1_key='', out2_key='', out3_key='', out4_key='', out5_key='', out6_key=''):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='MSG_HANDLER',   # will show up in GRC
            in_sig=None,
            out_sig=None
        )
        self.keys = [out0_key, out1_key, out2_key, out3_key, out4_key, out5_key, out6_key]
        self.message_port_register_in(pmt.intern('msg_in'))
        self.set_msg_handler(pmt.intern('msg_in'), self.handle_msg)
        for i in range(7):
            self.message_port_register_out(pmt.intern(f'out{i}'))
            print(f'registered variable: {self.keys[i]}')

    def handle_msg(self, msg):
        value = pmt.to_python(msg)
        if isinstance(value, dict):
            print(f'Got config msg: {value}')
            for key, val in value.items():
                if key in self.keys:
                    print(f'got msg for port{self.keys.index(key)}.')
                    self.message_port_pub(pmt.intern(f'out{self.keys.index(key)}'), pmt.cons(pmt.intern(key), pmt.to_pmt(val)))
        else:
            print('msg is not dict!')


    def work(self, input_items, output_items):
        """example: multiply with constant"""
        output_items[0][:] = input_items[0] # * self.example_param
        return len(output_items[0])
