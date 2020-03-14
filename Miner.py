from Block import Block
import Blockchain
import hashlib
from Users import user_db
import random
import cbor
import time

COINS_PER_BLOCK = 100
MAX_TRANS_PER_BLOCK = 4

class Miner():
    
    def __init__(self, miner_id, blockchain):
        self.miner_id = miner_id
        self.blockchain = blockchain
    
    def mine(self):
        pool = []
        if len(self.blockchain.transactions_pool)<4:
            pool.extend(self.blockchain.transactions_pool)
        else:
            random_unique_index = random.sample(range(0, len(self.blockchain.transactions_pool)), 4)
            for i in random_unique_index:
                pool.append(self.blockchain.transactions_pool[i])
        trans = []
        temp_balance = {} # key = user value = balance
        for transaction in pool:
            trans.append(transaction)
            if transaction.sender not in temp_balance:
                # to do : function to get balance get_balance(transaction.sender)
                temp_balance[transaction.sender] = user_db[transaction.sender].get("balance")
            if transaction.receiver not in temp_balance:
                temp_balance[transaction.receiver] = user_db[transaction.receiver].get("balance")

        for transaction in trans:
            if temp_balance[transaction.sender] - transaction.amount < 0:
                print("Transaction invalid: insufficient balance...")
                trans.remove(transaction)
                self.blockchain.remove_transaction_from_pool(transaction)
                continue
            temp_balance[transaction.sender] -= transaction.amount
            temp_balance[transaction.receiver] += transaction.amount
            print("Transaction can be processed: sufficient balance...")
            #get sender and amount
        # Init block and build tree
        prev_header = self.blockchain.longest_header
        if len(trans) == 0:
            return "All transactions invalid"
        
        block = Block(trans, prev_header)
        #get pow
        counter = 0
        start = time.time()
        while True:
            if counter % 10000 == 0:
                print("Mine attempt:", counter, " by: ", self.miner_id[0:5])
            #drop block if someone else has added to the chain
            if prev_header != self.blockchain.longest_header:
                print("Longest header has changed. Other miner finished first...")
                break
            generate_nonce = str(random.randint(0, 300000))
            block.header['nonce'] = generate_nonce
            to_hash = cbor.dumps(block.header)
            digest = hashlib.sha256(to_hash).digest()
            if digest < self.blockchain.target:
                try:
                    self.blockchain.add(block)
                    for transaction in trans:
                        user_db[transaction.sender]["balance"] -= transaction.amount
                        user_db[transaction.receiver]["balance"] += transaction.amount
                    # get miner balance
                    user_db[self.miner_id]["balance"] = user_db[self.miner_id].get("balance", 0) + COINS_PER_BLOCK #reward
                    print('Mining successful. Time taken: ', time.time()-start)
                    # announce to everyone 
                except Exception as e:
                    print("Mining failed, blockchain reject submitted block:", e, 'time taken: ',time.time()-start)
                break
            counter+= 1

    def check_balance(self, public_key):
        chain = self.blockchain
        transactions_list = []
        balance = 0
        for v in chain.past_transactions:
            if v.sender == public_key:
                balance -= v.amount
                transactions_list.append(v)
            if v.receiver == public_key:
                balance += v.amount
                transactions_list.append(v)
        return balance
        