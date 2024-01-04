#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: RX_TX
# Author: CrinitusFeles
# GNU Radio version: 3.10.3.0
import os
import time
from gnuradio import blocks
from gnuradio import gr
import sys
import signal
from gnuradio import soapy
from gnuradio import zeromq
import RX_TX_epy_block_0 as epy_block_0  # embedded python block
import gnuradio.lora_sdr as lora_sdr
from dotenv import load_dotenv


load_dotenv()


class RX_TX(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "RX_TX", catch_exceptions=True)

        ##################################################
        # Variables
        ##################################################
        self.sync_word = sync_word = int(os.environ['SYNC_WORD'])
        self.soft_decoding = True
        self.sf = sf = int(os.environ['SF'])
        self.samp_rate = samp_rate = int(os.environ['SAMP_RATE'])
        self.pay_len = pay_len = 3
        self.output_index = output_index = 0
        self.ldro = ldro = False
        self.input_index = input_index = 0
        self.impl_head = impl_head = False
        self.has_crc = has_crc = True
        self.cr = cr = int(os.environ['CR'])
        self.center_freq = center_freq = int(os.environ['FREQ'])
        self.bw = bw = int(os.environ['BW'])

        ##################################################
        # Blocks
        ##################################################
        self.zeromq_push_sink_0 = zeromq.push_sink(gr.sizeof_char, 1, os.environ['ZMQ_RCV_MESSAGES_SERVER'], 100, True, (-1))
        self.zeromq_pull_msg_source_0_0 = zeromq.pull_msg_source(os.environ['ZMQ_SEND_MESSAGES_CLIENT'], 100, False)
        self.zeromq_pull_msg_source_0 = zeromq.pull_msg_source(os.environ['ZMQ_CONFIG_CLIENT'], 100, False)
        self.soapy_hackrf_source_0 = None
        dev = 'driver=hackrf'
        stream_args = ''
        tune_args = ['']
        settings = ['']

        self.soapy_hackrf_source_0 = soapy.source(dev, "fc32", 1, os.environ.get('HACKRF_SERIAL', ''),
                                  stream_args, tune_args, settings)
        self.soapy_hackrf_source_0.set_sample_rate(0, samp_rate)
        self.soapy_hackrf_source_0.set_bandwidth(0, 0)
        self.soapy_hackrf_source_0.set_frequency(0, int(os.environ['FREQ']))
        self.soapy_hackrf_source_0.set_gain(0, 'AMP', True)
        self.soapy_hackrf_source_0.set_gain(0, 'LNA', min(max(24, 0.0), 40.0))
        self.soapy_hackrf_source_0.set_gain(0, 'VGA', min(max(24, 0.0), 62.0))
        self.soapy_hackrf_sink_0 = None
        dev = 'driver=hackrf'
        stream_args = ''
        tune_args = ['']
        settings = ['']

        self.soapy_hackrf_sink_0 = soapy.sink(dev, "fc32", 1, os.environ.get('HACKRF_SERIAL', ''),
                                  stream_args, tune_args, settings)
        self.soapy_hackrf_sink_0.set_sample_rate(0, samp_rate)
        self.soapy_hackrf_sink_0.set_bandwidth(0, 0)
        self.soapy_hackrf_sink_0.set_frequency(0, int(os.environ['FREQ']))
        self.soapy_hackrf_sink_0.set_gain(0, 'AMP', False)
        self.soapy_hackrf_sink_0.set_gain(0, 'VGA', min(max(16, 0.0), 47.0))
        self.lora_sdr_whitening_0 = lora_sdr.whitening(True,True,',','pay_len')
        self.lora_sdr_modulate_0 = lora_sdr.modulate(sf, samp_rate, bw, [sync_word], (int(20*2**sf*int(samp_rate/bw))),8)
        self.lora_sdr_interleaver_0 = lora_sdr.interleaver(cr, sf, ldro, bw)
        self.lora_sdr_header_decoder_0 = lora_sdr.header_decoder(False, cr, pay_len, has_crc, ldro, True)
        self.lora_sdr_header_0 = lora_sdr.header(impl_head, has_crc, cr)
        self.lora_sdr_hamming_enc_0 = lora_sdr.hamming_enc(cr, sf)
        self.lora_sdr_hamming_dec_0 = lora_sdr.hamming_dec(True)
        self.lora_sdr_gray_mapping_0 = lora_sdr.gray_mapping( True)
        self.lora_sdr_gray_demap_0 = lora_sdr.gray_demap(sf)
        self.lora_sdr_frame_sync_0 = lora_sdr.frame_sync(int(center_freq), bw, sf, False, [sync_word], (int(samp_rate/bw)),8)
        self.lora_sdr_fft_demod_0 = lora_sdr.fft_demod( True, True)
        self.lora_sdr_dewhitening_0 = lora_sdr.dewhitening()
        self.lora_sdr_deinterleaver_0 = lora_sdr.deinterleaver( True)
        self.lora_sdr_crc_verif_0 = lora_sdr.crc_verif( 1, False)
        self.lora_sdr_add_crc_0 = lora_sdr.add_crc(has_crc)
        self.epy_block_0 = epy_block_0.blk(out0_key='output_index', out1_key='input_index', out2_key='sf', out3_key='center_freq', out4_key='cr', out5_key='bw', out6_key='has_crc')
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_throttle_0.set_min_output_buffer(65536)
        self.blocks_tag_debug_0 = blocks.tag_debug(gr.sizeof_char*1, '', "")
        self.blocks_tag_debug_0.set_display(True)
        self.blocks_selector_0_0 = blocks.selector(gr.sizeof_gr_complex*1,input_index,0)
        self.blocks_selector_0_0.set_enabled(True)
        self.blocks_selector_0 = blocks.selector(gr.sizeof_gr_complex*1,input_index,output_index)
        self.blocks_selector_0.set_enabled(True)
        self.blocks_null_source_0 = blocks.null_source(gr.sizeof_gr_complex*1)
        self.blocks_msgpair_to_var_1 = blocks.msg_pair_to_var(self.set_cr)
        self.blocks_msgpair_to_var_0_1_0_0 = blocks.msg_pair_to_var(self.set_output_index)
        self.blocks_msgpair_to_var_0_1_0 = blocks.msg_pair_to_var(self.set_input_index)
        self.blocks_msgpair_to_var_0_1 = blocks.msg_pair_to_var(self.set_sf)
        self.blocks_msgpair_to_var_0_0_0 = blocks.msg_pair_to_var(self.set_has_crc)
        self.blocks_msgpair_to_var_0_0 = blocks.msg_pair_to_var(self.set_bw)
        self.blocks_msgpair_to_var_0 = blocks.msg_pair_to_var(self.set_center_freq)
        self.blocks_message_debug_0_0 = blocks.message_debug(True)
        self.blocks_message_debug_0 = blocks.message_debug(True)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.epy_block_0, 'out3'), (self.blocks_msgpair_to_var_0, 'inpair'))
        self.msg_connect((self.epy_block_0, 'out5'), (self.blocks_msgpair_to_var_0_0, 'inpair'))
        self.msg_connect((self.epy_block_0, 'out6'), (self.blocks_msgpair_to_var_0_0_0, 'inpair'))
        self.msg_connect((self.epy_block_0, 'out2'), (self.blocks_msgpair_to_var_0_1, 'inpair'))
        self.msg_connect((self.epy_block_0, 'out1'), (self.blocks_msgpair_to_var_0_1_0, 'inpair'))
        self.msg_connect((self.epy_block_0, 'out0'), (self.blocks_msgpair_to_var_0_1_0_0, 'inpair'))
        self.msg_connect((self.epy_block_0, 'out4'), (self.blocks_msgpair_to_var_1, 'inpair'))
        self.msg_connect((self.lora_sdr_crc_verif_0, 'msg'), (self.blocks_message_debug_0, 'print'))
        self.msg_connect((self.lora_sdr_header_decoder_0, 'frame_info'), (self.lora_sdr_frame_sync_0, 'frame_info'))
        self.msg_connect((self.zeromq_pull_msg_source_0, 'out'), (self.blocks_message_debug_0_0, 'print'))
        self.msg_connect((self.zeromq_pull_msg_source_0, 'out'), (self.epy_block_0, 'msg_in'))
        self.msg_connect((self.zeromq_pull_msg_source_0_0, 'out'), (self.blocks_message_debug_0_0, 'print'))
        self.msg_connect((self.zeromq_pull_msg_source_0_0, 'out'), (self.lora_sdr_whitening_0, 'msg'))
        self.connect((self.blocks_null_source_0, 0), (self.blocks_selector_0_0, 1))
        self.connect((self.blocks_selector_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_selector_0, 1), (self.soapy_hackrf_sink_0, 0))
        self.connect((self.blocks_selector_0_0, 0), (self.blocks_selector_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.lora_sdr_frame_sync_0, 0))
        self.connect((self.lora_sdr_add_crc_0, 0), (self.lora_sdr_hamming_enc_0, 0))
        self.connect((self.lora_sdr_crc_verif_0, 0), (self.blocks_tag_debug_0, 0))
        self.connect((self.lora_sdr_crc_verif_0, 0), (self.zeromq_push_sink_0, 0))
        self.connect((self.lora_sdr_deinterleaver_0, 0), (self.lora_sdr_hamming_dec_0, 0))
        self.connect((self.lora_sdr_dewhitening_0, 0), (self.lora_sdr_crc_verif_0, 0))
        self.connect((self.lora_sdr_fft_demod_0, 0), (self.lora_sdr_gray_mapping_0, 0))
        self.connect((self.lora_sdr_frame_sync_0, 0), (self.lora_sdr_fft_demod_0, 0))
        self.connect((self.lora_sdr_gray_demap_0, 0), (self.lora_sdr_modulate_0, 0))
        self.connect((self.lora_sdr_gray_mapping_0, 0), (self.lora_sdr_deinterleaver_0, 0))
        self.connect((self.lora_sdr_hamming_dec_0, 0), (self.lora_sdr_header_decoder_0, 0))
        self.connect((self.lora_sdr_hamming_enc_0, 0), (self.lora_sdr_interleaver_0, 0))
        self.connect((self.lora_sdr_header_0, 0), (self.lora_sdr_add_crc_0, 0))
        self.connect((self.lora_sdr_header_decoder_0, 0), (self.lora_sdr_dewhitening_0, 0))
        self.connect((self.lora_sdr_interleaver_0, 0), (self.lora_sdr_gray_demap_0, 0))
        self.connect((self.lora_sdr_modulate_0, 0), (self.blocks_selector_0, 1))
        self.connect((self.lora_sdr_whitening_0, 0), (self.lora_sdr_header_0, 0))
        self.connect((self.soapy_hackrf_source_0, 0), (self.blocks_selector_0_0, 0))


    def get_sync_word(self):
        return self.sync_word

    def set_sync_word(self, sync_word):
        self.sync_word = sync_word

    def get_soft_decoding(self):
        return self.soft_decoding

    def set_soft_decoding(self, soft_decoding):
        self.soft_decoding = soft_decoding

    def get_sf(self):
        return self.sf

    def set_sf(self, sf):
        self.sf = sf
        self.lora_sdr_gray_demap_0.set_sf(self.sf)
        self.lora_sdr_hamming_enc_0.set_sf(self.sf)
        self.lora_sdr_interleaver_0.set_sf(self.sf)
        self.lora_sdr_modulate_0.set_sf(self.sf)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.soapy_hackrf_sink_0.set_sample_rate(0, self.samp_rate)
        self.soapy_hackrf_source_0.set_sample_rate(0, self.samp_rate)

    def get_pay_len(self):
        return self.pay_len

    def set_pay_len(self, pay_len):
        self.pay_len = pay_len

    def get_output_index(self):
        return self.output_index

    def set_output_index(self, output_index):
        self.output_index = output_index
        self.blocks_selector_0.set_output_index(self.output_index)

    def get_ldro(self):
        return self.ldro

    def set_ldro(self, ldro):
        self.ldro = ldro

    def get_input_index(self):
        return self.input_index

    def set_input_index(self, input_index):
        self.input_index = input_index
        self.blocks_selector_0.set_input_index(self.input_index)
        self.blocks_selector_0_0.set_input_index(self.input_index)

    def get_impl_head(self):
        return self.impl_head

    def set_impl_head(self, impl_head):
        self.impl_head = impl_head

    def get_has_crc(self):
        return self.has_crc

    def set_has_crc(self, has_crc):
        self.has_crc = has_crc

    def get_cr(self):
        return self.cr

    def set_cr(self, cr):
        self.cr = cr
        self.lora_sdr_hamming_enc_0.set_cr(self.cr)
        self.lora_sdr_header_0.set_cr(self.cr)
        self.lora_sdr_interleaver_0.set_cr(self.cr)

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.soapy_hackrf_sink_0.set_frequency(0, self.center_freq)
        self.soapy_hackrf_source_0.set_frequency(0, self.center_freq)

    def get_bw(self):
        return self.bw

    def set_bw(self, bw):
        self.bw = bw




def main(top_block_cls=RX_TX, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()
    while True:
        time.sleep(1)
    # try:  # when running in interactive mode
    #     in_data =  input('Press Enter to quit: ')
    # except EOFError as err:
    #     time.sleep(0.1)
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
