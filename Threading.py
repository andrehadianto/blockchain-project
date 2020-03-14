from Miner import Miner
from Transaction import Transaction
import random
import threading
import time

class MiningWorker(threading.Thread):
  def __init__(self, blockchain, user_pk):
    threading.Thread.__init__(self)
    self.blockchain = blockchain
    self.user_pk = user_pk
    
  def run(self):
    miner = Miner(self.user_pk, self.blockchain)
    for _ in range(50):
      print(self.user_pk[0:5], "starts mining")
      miner.mine()
      print(self.user_pk[0:5], "stops mining")

class TransactionWorker(threading.Thread):
  def __init__(self, blockchain, users):
    threading.Thread.__init__(self)
    self.blockchain = blockchain
    self.users = users

  def run(self):
    random_transactions = random.randint(10, 14)
    transaction_list = []
    for _ in range(0, random_transactions):
      random_sender = random.randint(0,5)
      random_receiver = random.randint(0,5)
      random_amount = random.randint(0,50)
      trans = Transaction(self.users[random_sender], self.users[random_receiver], random_amount, "{} send to {}".format(self.users[random_sender][0:5], self.users[random_receiver][0:5]))
      transaction_list.append(trans)
    self.blockchain.add_transaction_to_pool(transaction_list)
    print('All', random_transactions, 'transactions added')