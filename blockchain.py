import datetime
import json
import hashlib
import random
from flask import Flask , jsonify

class Blockchain:
    def __init__(self):
        #store group of Block
        self.chain = [] #list to store Block
        self.transaction = 0
        #genesis block
        self.create_block(nonce = 1, previous_hash = "0")

    #create Block
    def create_block(self,nonce,previous_hash):
        #store component of each Block
        block = {
            "index" : len(self.chain)+1,
            "timestamp" : str(datetime.datetime.now()),
            "nonce" : nonce,
            "data" : self.transaction,
            "previous_hash" : previous_hash ,
        }

        self.chain.append(block)
        return block

    #get previous block
    def get_previous_block(self):
        return self.chain[-1]

    #hashing
    def hash(self, block):
        #convert python object(dict) => json object
        encode_block = json.dumps(block, sort_keys = True).encode()

        #sha - 256
        

        return hashlib.sha256(encode_block).hexdigest()

    #pow
    def proof_of_work(self, previous_nonce):
        #require nonce => target hash => 00fxxxxxxxx
        new_nonce = 1 #wanted nonce
        check_proof = False #target require

        #solve
        while check_proof is False:
            #hexadecimal
            hash_operation = hashlib.sha256(str(new_nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hash_operation[:2] == "00":
                check_proof = True
            else:
                new_nonce+=1
        return new_nonce

    #valid block
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index] # verify block
            if block["previous_hash"] != self.hash(previous_block):
                return False
            previous_nonce = previous_block["nonce"] # nonce of previous block
            nonce = block["nonce"] # nonce of verify block
            hashoperation = hashlib.sha256(str(nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hashoperation[:2] != "00":
                return False
            previous_block = block
            block_index += 1
        return True

#web Sever

app = Flask(__name__)

#block

blockchain = Blockchain()

#routing
@app.route('/')
def hello():
    return "<h1>Hello Blockchain</h1>"

@app.route('/get_chain', methods=["GET"])
def get_chain():
    response={
        "chain":blockchain.chain,
        "length":len(blockchain.chain)
    }
    return jsonify(response),200

@app.route('/mining', methods=["GET"])
def mining_block():

    amount = 1000000
    blockchain.transaction = blockchain.transaction + amount

    #pow
    previous_block = blockchain.get_previous_block()
    previous_nonce = previous_block["nonce"]

    #nonce
    nonce = blockchain.proof_of_work(previous_nonce)

    #hash previous block
    previous_hash = blockchain.hash(previous_block)

    #update new block
    block = blockchain.create_block(nonce, previous_hash)
    
    response = {
        "message" : "Mining Block completed",
        "index" : block["index"],
        "timestamp" : block["timestamp"],
        "nonce" : block["nonce"],
        "data" : block["data"],
        "previous_hash" : block["previous_hash"]
    }
    
    return jsonify(response),200

@app.route('/is_valid', methods = ["GET"])
def is_vaild() :
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {"message" : "Blockchain valid"}
    else :
        response = {"message" : "Have Problem, Blockchain Is Not Valid"}
    return jsonify(response),200

#ใช้งาน Blockchain
if __name__ == "__main__" :
    app.run()

    #encoded first block
    #print(blockchain.hash(blockchain.chain[0]))