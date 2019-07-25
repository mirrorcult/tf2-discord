from config import *
from pypresence import Presence
import valve.source
import valve.source.a2s
import valve.source.master_server
import time
import random

RPC = Presence(client_id)
RPC.connect()

rand = ["111", "222", "333"]

# Main loop
while True:
    RPC.update(details="testing:", state=random.choice(rand))
    time.sleep(15)
