from scapy.layers.inet import TCP, IP
from scapy.layers.l2 import Ether

x = b"aabbccddee035405db8e8303080045000034d60c400040060000c0a80065c0a80066c5ffbfcddcfac945000000008002faf082420000020405b40103030801010402"


TCP(x).show()