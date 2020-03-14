from Block import Block
import time
import hashlib
import cbor
import random


class BlockChain:
    
    def __init__(self):
        self.target_prefix = b'\x0f' * 2
        self.target = self.target_prefix + b'\xff'*254
        self.longest_block = None
        self.longest_header = None
        self.graph = {}
        self.genesis()
        self.existing_transaction = {}
        self.transactions_pool = []

    def add_transaction_to_pool(self, transactions):
        self.transactions_pool.extend(transactions)
        
    def remove_transaction_from_pool(self, transaction):
        self.transactions_pool.remove(transaction)

    def genesis(self):
        start = time.time()
        print("generating genesis block...")
        genesis_header = {
            "timestamp": int(time.time()),
            "root": None,
            "prev_header": None,
            "nonce": None,
        }
        counter = 0
        while True:
            if counter % 1000 == 0:
                print("genesis attempt: ",counter)
            genNonce = str(random.randint(0, 300000))
            genesis_header['nonce'] = genNonce
            to_hash = cbor.dumps(genesis_header)
            digest = hashlib.sha256(to_hash).digest()
            if digest < self.target:
                break
            counter+= 1
        print("genesis block created! Time taken:", time.time()-start)
        self.graph[digest] = {"children": [], "level_n": 0,"body":None, "timestamp": genesis_header["timestamp"]}
        self.longest_block = genesis_header
        self.longest_header = digest
        
    def validate(self, block): #check if incoming block is legit
        header = block.get_header()
        print('validating...', header)
        if self.verify_pow(block) is not True:
            print(1)
            return False
        elif header["timestamp"] < self.graph[self.longest_header]["timestamp"]: #TODO: IMPLEMENT FIND_BLOCK FROM HASHED_HEADER IN THE GRAPH
            print(2)
            return False
        for txn in block.merkle_tree.past_transactions:
            if txn.serialize() in self.existing_transaction:
                print(3)
                return False
        return True

    def verify_pow(self, block):
        to_hash = block.serialize()
        digest = hashlib.sha256(to_hash).digest()
        if digest < self.target:
            return True
        return False

    def add(self, block):
        print('blockchain.add: ')
        if self.validate(block):
            digest = block.hash_header()
            prev_level = self.graph[block.get_header()["prev_header"]]["level_n"]
            self.graph[block.get_header()["prev_header"]]["children"].append(digest)
            self.graph[digest] = {"children": [], "level_n": prev_level + 1, "body": block, "timestamp": block.get_header()["timestamp"]}
            for txn in block.merkle_tree.past_transactions:
                self.existing_transaction[txn.serialize()] = 1
                self.remove_transaction_from_pool(txn)
                
            if time.time() - self.graph[block.get_header()["prev_header"]]["timestamp"] > 5:
                # adjust target ( increase )
                self.target_prefix = int.to_bytes(int.from_bytes(self.target_prefix, 'little') * 2, 2, 'little')
                self.target = self.target_prefix + b'\xff'*254
                print("getting easier:", self.target_prefix)

            if time.time() - self.graph[block.get_header()["prev_header"]]["timestamp"] < 2: 
                # adjust target ( lower )
                self.target_prefix = int.to_bytes(int.from_bytes(self.target_prefix, 'little') // 2, 2, 'little')
                self.target = self.target_prefix + b'\xff'*254
                print("getting harder:", self.target_prefix)

    def resolve(self): #finds the longest header and updates it 
        highest_level_n = 0
        highest_level_n_digest = []
        for digest, node in self.graph.items(): #finding the highest level_n
            if node["level_n"] > highest_level_n:
                highest_level_n_digest = [] #getting nodes with highest level_n
                highest_level_n_digest.append(digest)
                highest_level_n += 1
            elif node["level_n"] == highest_level_n:
                highest_level_n_digest.append(digest)
            else: 
                continue

        self.longest_header = highest_level_n_digest[random.randint(0, len(highest_level_n_digest) - 1)] #return a random header
        print("The longest header is now " + self.longest_header)