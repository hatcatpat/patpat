import argparse
import global_variables

from pythonosc import dispatcher, osc_server, udp_client, osc_message_builder, osc_bundle_builder

from math import *


class OSCManager():
    def __init__(self):
        self.clients = []
        self.bundle = None
        #  self.setup_clients(9001, 12000)
        #  self.setup_clients(12000)
        self.setup_clients(57120)
        self.setup_server(5005)

    def setup_server(self, port):
        parser = argparse.ArgumentParser()
        parser.add_argument("--ip",
                            default="127.0.0.1",
                            help="The ip to listen on")
        parser.add_argument("--port",
                            type=int,
                            default=5005,
                            help="The port to listen on")
        args = parser.parse_args()

        disp = dispatcher.Dispatcher()
        disp.map("/update_commands", global_variables.trigger_update_flag)
        disp.map("/bang", global_variables.bang)
        disp.map("/init", global_variables.init_bang)

        self.server = osc_server.ThreadingOSCUDPServer((args.ip, args.port),
                                                       disp)
        print("Serving on {}".format(self.server.server_address))

    def serve_server(self):
        self.server.serve_forever()

    def setup_clients(self, *ports):

        for port in ports:
            parser = argparse.ArgumentParser()
            parser.add_argument("--ip",
                                default="127.0.0.1",
                                help="The ip of the OSC server")
            parser.add_argument("--port",
                                type=int,
                                default=port,
                                help="The port the OSC server is listening on")
            args = parser.parse_args()
            self.clients.append(udp_client.SimpleUDPClient(args.ip, args.port))

    ## sends the full bundle only to the "main" client, i.e the one making the audio
    def send_full_bundle(self):
        if not self.bundle == None:
            self.bundle = self.bundle.build()
            self.clients[0].send(self.bundle)
            self.reset_bundle()

    def reset_bundle(self):
        self.bundle = osc_bundle_builder.OscBundleBuilder(
            osc_bundle_builder.IMMEDIATELY)

    def send_osc_to_client(self, clientIndex, address, args):
        if 0 <= clientIndex < len(self.clients):
            self.clients[clientIndex].send_message(address, args)

    def add_osc_message(self, address, args):
        msg = osc_message_builder.OscMessageBuilder(address=address)

        msg.add_arg(global_variables.t)

        if type(args) == tuple or type(args) == list:
            for arg in args:
                msg.add_arg(arg)
        else:
            msg.add_arg(args)

        self.bundle.add_content(msg.build())

    def send_osc_bundle(self, address, args):
        bundle = osc_bundle_builder.OscBundleBuilder(
            osc_bundle_builder.IMMEDIATELY)
        msg = osc_message_builder.OscMessageBuilder(address="/array" + address)

        for arg in args:
            msg.add_arg(arg)
            bundle.add_content(msg.build())

        bundle = bundle.build()

        for client in self.clients:
            client.send(bundle)
