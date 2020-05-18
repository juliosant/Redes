from network.packet import Packet
from network.unreliable import UnreliableDataTransfer
from transport import checksum
import time
import random

ACK = False
Count = 0
ID = 0

class ReliableDataTransfer:

    def __init__(self, udt):
        if not isinstance(udt, UnreliableDataTransfer):
            raise Exception("udt parameter must be an instance of UnreliableDataTransfer")
        self.udt = udt

    def send(self, payload):
        global ACK,Count, ID
        packet = Packet({'payload': payload})
        packet.set_field("Pacote", ID)
        checksum.calculate_checksum(packet)
        self.udt.send(packet)
        # should wait for ACK before returning
        
        while(ACK == False):    
                       
            if(Count == 10):
                print("Tempo esgotado")
                self.udt.send(packet)
                Count = 0
            Count += 1 
            time.sleep(1)
        
        if(ACK == True):
            print("ACK Recebido")

        ACK = False
        ID = ID + 1    
        Count = 0     
        # if some time has passed while waiting for ACK, then it should retransmit the packet

    def receive(self):
        global ACK
        packet = self.udt.receive(timeout=100)
        #while packet is None:
        #   packet = self.udt.receive(timeout=100)
        valid = checksum.validate_checksum(packet)
        while valid is not True:
            if valid is False:
                print("Checksum inválido")
            if packet is None:
                print("Pacote Vazio")
            packet = self.udt.receive(timeout=100)
            valid = checksum.validate_checksum(packet)

        if packet is not None:
            # ID do Pacote Recebido
            print(packet.get_field("Pacote"))
            
        # should wait until there's data coming from bottom layer
            #valid = checksum.validate_checksum(packet)
            if valid:
                ACK = True
                # should acknowledge sender
                return packet.get_field('payload')