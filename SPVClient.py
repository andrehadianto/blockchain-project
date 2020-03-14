# get all the block header
# verify transaction exists/ added to the blockchain
# send a transaction
from Users import user_db

class SPVClient:
  def __init__(self, pub_key, priv_key):
    self.pub_key = pub_key
    self.priv_key = priv_key

  def createTransaction(self, blockchain, receiver_vk, amount, comment):
    new_transaction = Transaction(self.pub_key, receiver_vk, amount, comment)
    blockchain.add_transaction_to_pool([new_transaction])
    return new_transaction.sign(self.priv_key)

  def checkBalance(self):
    return ("User does not exists. Please register.") if self.pub_key not in user_db else user_db[self.pub_key]["balance"]