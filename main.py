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
    
    print("\nsutdcoin blockchain graph")
    for k, v in sutdcoin.graph.items():
        print("BLOCK: ",k)
        print("CHILDREN: ",v["children"])
        print("HEIGHT: ",v["level_n"])
        print("TIMESTAMP: ",v["timestamp"],"\n")

    print("\nsutdcoin user_db")
    for k, v in user_db.items():
        print("USER_ID: ",k)
        print("BALANCE: ",v["balance"], "\n")
