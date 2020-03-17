from Block import Block
import time
import hashlib
import cbor
import random

prefix = b'\x00'
midfix = b'\x9f'
suffix = b'\xbb'


class BlockChain:

    def __init__(self):
        self.target_prefix = prefix * 2
        self.midfix = midfix
        self.target = (self.target_prefix + self.midfix*2 + suffix*252).hex()
        self.longest_header = None
        self.graph = {}
        self.genesis()
        self.existing_transaction = {}
        self.transactions_pool = []
        self.rejected_transaction = []

    def add_transaction_to_pool(self, transactions):
        self.transactions_pool.extend(transactions)

    def remove_transaction_from_pool(self, transaction):
        try:
            self.transactions_pool.remove(transaction)
            print('transaction ', transaction, ' is removed')
            self.rejected_transaction.append(transaction)
        except:
            print('transaction ', transaction, ' is already removed')

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
            if counter % 100000 == 0:
                print("genesis attempt: ", counter)
            generate_nonce = str(random.randint(0, 300000))
            genesis_header['nonce'] = generate_nonce
            to_hash = cbor.dumps(genesis_header)
            digest = hashlib.sha256(to_hash).hexdigest()
            if digest < self.target:
                break
            counter += 1
        print("genesis block created! Time taken:", time.time()-start)
        self.graph[digest] = {"children": [], "level_n": 0,
                              "body": None, "timestamp": genesis_header["timestamp"]}
        self.longest_header = digest

    def validate(self, block):  # check if incoming block is legit
        header = block.get_header()
        if self.verify_pow(block) is not True:
            return False
        elif header["timestamp"] < self.graph[self.longest_header]["timestamp"]:
            return False
        for txn in block.merkle_tree.past_transactions:
            if txn.serialize() in self.existing_transaction:
                return False
        print('validated: ', header)
        return True

    def verify_pow(self, block):
        to_hash = block.serialize()
        digest = hashlib.sha256(to_hash).hexdigest()
        if digest < self.target:
            return True
        return False

    def add(self, block):
        if self.validate(block):
            digest = block.hash_header()
            prev_level = self.graph[block.get_header()[
                "prev_header"]]["level_n"]
            self.graph[block.get_header()["prev_header"]
                       ]["children"].append(digest)
            self.graph[digest] = {"children": [], "level_n": prev_level + 1,
                                  "body": block, "timestamp": block.get_header()["timestamp"]}
            for txn in block.merkle_tree.past_transactions:
                self.existing_transaction[txn.serialize()] = self.existing_transaction.get(
                    txn.serialize(), 0) + 1
                self.remove_transaction_from_pool(txn)
            # Updating difficulty
            if time.time() - self.graph[block.get_header()["prev_header"]]["timestamp"] > 5:
                self.midfix = int.to_bytes(int.from_bytes(
                    self.midfix, 'little') + 256, 2, 'little')
                self.target = (self.target_prefix + self.midfix*2 + suffix*252).hex()
                print("reducing target difficulty")
            if time.time() - self.graph[block.get_header()["prev_header"]]["timestamp"] < 2:
                self.midfix = int.to_bytes(int.from_bytes(
                    self.midfix, 'little') - 256, 2, 'little')
                self.target = (self.target_prefix + self.midfix*2 + suffix*252).hex()
                print("increasing target difficulty")
            self.resolve_longest_header()

    # finds the longest header and updates it
    def resolve_longest_header(self):
        highest_level_n = 0
        highest_level_n_digest = []
        for digest, node in self.graph.items():  # finding the highest level_n
            # if len(node["children"]) > 1:
            #     print('Fork is found...')
            # check transaction
            if node["level_n"] > highest_level_n:
                highest_level_n_digest = []  # getting nodes with highest level_n
                highest_level_n_digest.append(digest)
                highest_level_n += 1
            elif node["level_n"] == highest_level_n:
                highest_level_n_digest.append(digest)
            else:
                continue
        random_index = random.randint(0, len(highest_level_n_digest) - 1)
        self.longest_header = highest_level_n_digest[random_index]  # return a random header
        print("The longest header is now ", self.longest_header)
        # go to the shorter chaing
        # and give refund to all the previous transactions
        level_n_fork = highest_level_n - 1
        fork_digest = 0
        current_digest = self.longest_header
        while True: #iterating to find the parents, stop until a fork is found
            for digest, node in self.graph.items():
                if node["level_n"] == level_n_fork and current_digest in node["children"]:
                    if len(node["children"]) > 1:
                        fork_digest = digest
                    else:
                        level_n_fork += 1
                        current_digest = digest
                    break
            if fork_digest != 0: #fork is found
                break
        print("The fork is found at ", fork_digest)
        
        #issuing refund
        to_refund = []
        for children in self.graph[fork_digest]["children"]:
            current_child = children
            if children != current_digest:
                while True:
                    to_refund.append(elf.graph[current_child]["body"]["root"]) #appends the root of all blocks of the shortest chain
                    if len(self.graph[current_child]["children"]) == 0:
                        break
                    else:
                        current_child = self.graph[current_child]["children"][0] #assume theres only 1 child please
        
        #to_refund does something




                
                    
                

            

