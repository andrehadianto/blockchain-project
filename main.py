import hashlib
import random
import time
import math
import json
import KeyGen
from Miner import Miner
from Users import user_db
from Blockchain import BlockChain
from Transaction import Transaction

if __name__ == "__main__":
    sutdcoin = BlockChain()
    users = list(user_db.keys())
    t1 = Transaction(users[0], users[2], 80, "user0 -(80)-> user2")
    t2 = Transaction(users[0], users[1], 30, "user0 -(30)-> user1")
    sutdcoin.add_transaction_to_pool([t1,t2])

    user3 = Miner(users[3], sutdcoin)
    user3.mine()
    
    print("\nsutdcoin blockchain graph:", sutdcoin.graph)
    print("\nsutdcoin user_db:", user_db)