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
from Threading import MiningWorker, TransactionWorker

if __name__ == "__main__":
    sutdcoin = BlockChain()
    users = list(user_db.keys())
    # Create transactions
    trans_gen = TransactionWorker(sutdcoin, users)
    trans_gen.start()

    time.sleep(2)

    # Converting users into workers
    worker_0 = MiningWorker(sutdcoin, users[0])
    worker_1 = MiningWorker(sutdcoin, users[1])
    worker_0.start()
    worker_1.start()
    worker_0.join()
    worker_1.join()
    
    print("\nsutdcoin blockchain graph:", sutdcoin.graph)
    print("\nsutdcoin user_db:", user_db)



""" Things to do: 
- Fork demo
- Make sure coin cant be double spent, check wallet
- Simulate miners competition
"""