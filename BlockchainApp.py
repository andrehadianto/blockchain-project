from flask import Flask, request, redirect
from Blockchain import BlockChain
import json
import os

PORT = 5001

app = Flask(__name__)

sutdcoin = BlockChain()
user_db = {}


@app.route('/add_user', methods=["POST"])
def add_user():
    if request.method == "POST":
        try:
            pub_key = request.form['pub_key']
            priv_key = request.form['priv_key']
            balance = request.form['balance']
        except:
            return "missing parameters", 400
        user_db[pub_key] = {"priv_key": priv_key, "balance": balance}
        return "user successfully added", 200


@app.route('/add_transaction', methods=["POST"])
def add_transactions():
    if request.method == "POST":
        try:
            transaction = request.form["transaction"]
        except:
            return ('', 400)
        try:
            sutdcoin.add_transaction_to_pool([transaction])
        except Exception as e:
            return('something wrong ' + e, 500)
        return ("transaction successfully added", 200)


@app.route('/get_headers')
def get_headers():
    res = []
    for hashed_headers in sutdcoin.graph.keys():
        res.append(hashed_headers['body'].get_header())
    res = json.dumps(res)
    return res, 200


@app.route('/get_users')
def get_users():
    return json.dumps(user_db)


@app.route('/graph')
def get_graph():
    return json.dumps(sutdcoin.graph)


@app.route('/find_transactions', methods=["POST"])
def find_transactions():
    if request.method == "POST":
        try:
            txn_list = request.form['transaction_list']
        except:
            return "missing parameters", 400
        res = {}
        for txn in txn_list:
            for val in sutdcoin.graph.values():
                if txn in val['body'].merkle_tree.past_transactions:
                    nodes, neighbour, _ = val['body'].merkle_tree.get_min_nodes(
                        txn)
                    root = val['body'].merkle_tree.get_root()
                    res[txn] = {"nodes": nodes,
                                "neighbour": neighbour, "root": root}
        res = json.dumps(res)
        return res, 200


@app.route('/get_all_user_transactions', methods=["POST"])
def get_all_user_transactions():
    if request.method == "POST":
        try:
            user = request.form['user']
        except:
            return "missing parameters", 400
        res = []
        for txn in sutdcoin.existing_transaction:
            if user == txn.sender or user == txn.receiver:
                res.append(txn)
        res = json.dumps(res)
        return res, 200


if __name__ == '__main__':
    app.run("0.0.0.0", port=PORT, debug=True)
