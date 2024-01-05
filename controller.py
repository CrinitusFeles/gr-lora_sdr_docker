
from sdr_zmq_client.pmt import PMT
# from threading import Thread
# from sdr_zmq_client.socket_client import SocketClient
import zmq
from zmq import Socket
from ast import literal_eval



def config_server(addr: str = '0.0.0.0:5502'):
    context = zmq.Context()

    #  Socket to talk to server
    print("Start server…")
    socket: Socket = context.socket(zmq.PUSH)
    socket.bind(f"tcp://{addr}")

    #  Do 10 requests, waiting each time for a response
    try:
        while True:
            in_data: str = input('> ')
            config = PMT.DICT({
                                #   PMT.STRING('center_freq'): PMT.INT32(int(437e6)),
                                #   PMT.STRING('cr'): PMT.INT32(1),
                                #   PMT.STRING('bw'): PMT.INT32(125000),
                                #   PMT.STRING('sf'): PMT.INT32(10),
                                  PMT.STRING('input_index'): PMT.INT32(0),
                                  PMT.STRING('output_index'): PMT.INT32(0),
                                  }).to_bytes()
            # socket.send(msg(in_data.encode()))
            socket.send(config)
    except KeyboardInterrupt:
        pass

def send_msg_server(addr: str = '0.0.0.0:5503'):
    context = zmq.Context()
    print("Start server…")
    socket: Socket = context.socket(zmq.PUSH)
    socket.bind(f"tcp://{addr}")
    try:
        while True:
            in_data: str = input('> ')
            try:
                list_data = literal_eval(in_data)
                if isinstance(list_data, list):
                    data = bytes(list_data)
                    # socket.send((data.hex() + ',').encode('utf-8'))
                    socket.send(PMT.STRING(data.decode('utf-8')).to_bytes())
            except ValueError:
                socket.send(PMT.STRING(in_data).to_bytes())
    except KeyboardInterrupt:
        pass

def client(addr: str = '172.31.2.119:5502'):
    context = zmq.Context()

    print("Connecting to server")
    socket = context.socket(zmq.PULL)
    socket.connect(f"tcp://{addr}")
    try:
        while True:
            msg = socket.recv()
            print(f'got_msg {len(msg)}: ', msg)
            print(msg.hex(' ').upper())
    except KeyboardInterrupt:
        pass

# s_client = SocketClient('172.31.2.119', 5503)
# if(s_client.connect()):
#     s_client.send(pair('packet_len', 1))
#     s_client.disconnect()
client()
# send_msg_server()

# client()
# th = Thread(target=client, daemon=True)
# th.start()
# client()
# def routine(top_block):
#     import zmq
#     context = zmq.Context()

# #  Socket to talk to server
#     print("Connecting to hello world server…")
#     socket = context.socket(zmq.PULL)
#     socket.connect("tcp://192.168.0.105:5500")
#     while True:
#         msg = socket.recv()
#         print('got_msg: ', msg)
#         print(dir(top_block.lora_sdr_whitening_0))
#         top_block.lora_sdr_whitening_0.msg_handler(msg)