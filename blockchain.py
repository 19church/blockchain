# ,,,.,,,,,,,,,,,,,,,,,,,,,.,.,,.,,,,,,*/(///*,,.,,,.,,,,,,,..,..,..,.,,..,.,,,,.,
# ,,,,,,,,,,,,,,,,.,,,,,,,,,,,,,#%%&%%%%%%%&%%%%%%%#/*,,,.,,,,.,......,.,,,..,,,,.
# ,,,,,,,,.,,,,,,,,.,,,,,,,,(%&&&&&&&&&&&&&%&&%&&%%&%%%%%/,,,.,,....,,,....,.,,,,.
# ,,,,,,,..,,,...,,,.,.,./%%&&&&&&&&&&&&&&&&&&&&&&&%&%%%%%%%,,...........,........
# ,,,,,......,.....,..,*%&&&&&&&&&&&&&&&&&&&&&&&&&&&&&%&&%%%%#,,..................
# ,,,,.....,.,.......,#%&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&%%%%%%%##,..................
# ,..,...............(%&&&&&&&&&&&&&&&&&&&%&&&&%%%&&%#%%#%####((..................
# ,................,,%%&%&&&&&&%%&%&&&&&%(##%%###%%#(((/*(((((((..................
# ..................,%%%&%&%&&&&&%%%%%%#(/*/(*/*/(///**,,*(##%#(..................
# ..................,#%&&&&&&&%#(((/*//***,,,,,,,,,,,,,,,,(####,..................
# ...................,%&&&&%%#///***/**/***,,,,,,,******,,*###/...................
# ....................,%&&%%(/**/****,,******,,,,,,,,,,,,,,/(*....................
# .,.................,//*/##(/*******(##(***,,,,,*/#%#*,,,,***,...................
# ...................,,**///(/********/**,,,,,,.,,,**,,,,,,**,....................
# .....................,****///***,,***,,,,,,,,,,,,,,,,,,,,*,.....................
# ,.....,...............,**/////***,,,,,,,**,,,,,,,,.,.,,,,,,.....................
# ......,................,***///****,,,,**********,,,,,,,,,,,.....................
# .,.............,.......,..,*//****,,,,,****,,,,,,,,,,,,,........................
# ...............,.,..,......,*/*/*******/((/////(/,,,,,,.........................
# ,.,..,.........,...,,...,...,/////********///***,,,,,,..........................
# .,,...........,,...,,,...,,,*////////**********,,,***,..........................
# ,,,....,.......,,...,.,,,,,,(#//////(//**/**********#*,.....,...................
# ,,.,,,,...,,,,,,....,,,,,,,,,*/******///###((///***//,,,,,,..,,,................
# ..,,,,..,,...,,,.,,,,,,,,,,,,,,,/*****************(,,,,.,,,,,,,,,,......,..,....
# .,,.,....,,,,,,,,,,,,,,,,,,,,,,,,,****************,,,,,,,.,,,,,,,,,,,,.,..,,....
# ,,,,..,.,,*,*,,,,,,,,,,,,,,,,,,,,,,,*****,******,,,,,,,,,,,,,,,,,,,,,,,,,.......
# ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,********,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,.,,
# ,,,,,,*,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,**,,,,,,,,,,,,,,,,,*,,,,,,,,,,,,,,,,,,.
# .,,,,**,,,,,,,,,,,,,,,,,*,,,,,,,,,,,,**,,,,,,,,,,,,**,,,,,,,,,,,,,,,,,,,,,,,,,,.
# ,,,,,,*,,,,,,,,,,,,,,,,,,,*////**,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
# ,,**,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
# ,,**,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
# ,*,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,*,,,,,,,,,,,,

import datetime
import json
import hashlib
from flask import Flask,jsonify
import testdata

class Blockchain:
    def __init__(self):
        #store group of Block
        self.chain = [] #list to store Block
        
        #data
        self.transaction = 0
        self.data_g = {
            "Dormitory_Name":"ข้าวโพด",
            "Room_Number":"000",
            "Room_Size":"4.00  meter square",
            "Monthly_Rent":"2 BTC",
            "Current_Roomer":"Ty Parin",
            "District":"ชาไทย",
            "Province":"หมูทะ"
        }

        #genesis block
        self.create_block(nonce = 1, previous_hash = "0", data = self.data_g)

    #hashing
    def hash(self, block, nonce):
        #convert python object(dict) => json object
        hhh = [block["data"],block["previous_hash"],nonce]
        encode_block = json.dumps(hhh, sort_keys=True).encode()

        #sha - 256

        return hashlib.sha256(encode_block).hexdigest()
    
    #create Block
    def create_block(self,nonce,previous_hash,data):
        #store component of each Block
        block = {
            "index":len(self.chain)+1,
            "timestamp":str(datetime.datetime.now()),
            "nonce":nonce,
            "data":data,
            "previous_hash":previous_hash ,
            "block_hash":""
        }

        hhh = [block["data"],block["previous_hash"],nonce]

        block_hash = hashlib.sha256(json.dumps(hhh, sort_keys=True).encode()).hexdigest()

        block_with_hash = {
            "index":len(self.chain)+1,
            "timestamp":str(datetime.datetime.now()),
            "nonce":nonce,
            "data":data,
            "previous_hash":previous_hash,
            "block_hash":block_hash
        }

        self.chain.append(block_with_hash)
        return block_with_hash

    #get previous block
    def get_previous_block(self):
        return self.chain[-1]

    #pow
    def proof_of_work(self,block, previous_nonce):
        #require nonce => target hash => 0000fxxxxxxxx
        new_nonce = 1 #wanted nonce
        check_proof = False #target require

        #solve
        while check_proof is False:
            #hexadecimal
            cal_nonce = new_nonce**2 - previous_nonce**2
            hash_operation = self.hash(block, cal_nonce)
            if hash_operation[:4] == "0000":
                block["nonce"] = new_nonce
                block["block_hash"] = hash_operation
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
            if block["previous_hash"] != previous_block["block_hash"]:
                return False
            previous_nonce = previous_block["nonce"] # nonce of previous block
            nonce = block["nonce"] # nonce of verify block
            cal_nonce = nonce**2 - previous_nonce**2
            hashoperation = self.hash(block, cal_nonce)
            if hashoperation[:4] != "0000":
                return False
            previous_block = block
            block_index += 1
        return True


def create_data():
    Dormitory_Name = "ข้าวโพด"
    Room_Size = "4.00 meter square : "
    Monthly_Rent = "1 BTC"
    District = "ชาไทย"
    Province = "หมูทะ"

    while True :
        Room_Number = input("Enter Room_Number : ")
        if Room_Number.isnumeric() and len(Room_Number) == 3:
            break
    Current_Roomer = input("Enter Your Name : ")

    data = {
    "Dormitory_Name":Dormitory_Name,
    "Room_Number":Room_Number,
    "Room_Size":Room_Size,
    "Monthly_Rent":Monthly_Rent,
    "Current_Roomer":Current_Roomer,
    "District":District,
    "Province":Province
    }
    return data

#web Sever

app = Flask(__name__)

#block

blockchain = Blockchain()

#routing
@app.route('/')
def hello():
    print("Hello")
    return "<h1>Hello Blockchain</h1>"

@app.route('/get_chain', methods=["GET"])
def get_chain():
    response={
        "chain":blockchain.chain,
        "length":len(blockchain.chain)
    }
    return jsonify(response),200

def get_all_block():
    for i in range(0,len(blockchain.chain)) :
        print("=======================================\n")
        print("block index :",blockchain.chain[i]["index"])
        print("timestamp :",blockchain.chain[i]["timestamp"])
        print("nonce :", blockchain.chain[i]["nonce"])
        print()
        print("Dormitory_Name :",blockchain.chain[i]["data"]["Dormitory_Name"])
        print("Room_Number :",blockchain.chain[i]["data"]["Room_Number"])
        print("Monthly_Rent :",blockchain.chain[i]["data"]["Monthly_Rent"])
        print("Current_Roomer :",blockchain.chain[i]["data"]["Current_Roomer"])
        print("District :",blockchain.chain[i]["data"]["District"])
        print("Province :",blockchain.chain[i]["data"]["Province"])
        print()
        print("Block Hash :",blockchain.chain[i]["block_hash"])
        print("Previous Hash :",blockchain.chain[i]["previous_hash"])
        print("\n=======================================\n")
    print("chain :", len(blockchain.chain))

def get_block() :
    name = input("Enter Current_Roomer : ")
    search_block = []
    count = 0

    for i in range(0,len(blockchain.chain)) :
        if name == blockchain.chain[i]["data"]["Current_Roomer"] :
            search_block.append(i)
            count += 1
    if count == 0 :
        print("Not Found!!!")
    else :
        print("\nFound %d"%len(search_block))
        for i in search_block :
            print("=======================================\n")
            print("block index :",blockchain.chain[i]["index"])
            print("timestamp :",blockchain.chain[i]["timestamp"])
            print("nonce :", blockchain.chain[i]["nonce"])
            print()
            print("Dormitory_Name :",blockchain.chain[i]["data"]["Dormitory_Name"])
            print("Room_Number :",blockchain.chain[i]["data"]["Room_Number"])
            print("Monthly_Rent :",blockchain.chain[i]["data"]["Monthly_Rent"])
            print("Current_Roomer :",blockchain.chain[i]["data"]["Current_Roomer"])
            print("District :",blockchain.chain[i]["data"]["District"])
            print("Province :",blockchain.chain[i]["data"]["Province"])
            print()
            print("Block Hash :",blockchain.chain[i]["block_hash"])
            print("Previous Hash :",blockchain.chain[i]["previous_hash"])
            print("\n=======================================\n")

#edit
def edit_block():
    not_found = True
    while True :
        try :
            s_block = int(input("Select Block Index : "))
            if type(s_block) is int:
                break
        except :
            print("Input only Integer")
    for i in range(0,len(blockchain.chain)) :
        if s_block == blockchain.chain[i]["index"] :
            not_found = False
            s_block -=1
    if not_found :
        print("Not Found!!!")
        return False
    
    blockchain.chain[s_block]["data"]["Dormitory_Name"] = input("Enter new Dormitory_Name : ")
    while True :
        blockchain.chain[s_block]["data"]["Room_Number"] = input("Enter new Room_Number : ")
        if blockchain.chain[s_block]["data"]["Room_Number"].isnumeric() and len(blockchain.chain[s_block]["data"]["Room_Number"]) == 3:
            break
    blockchain.chain[s_block]["data"]["Monthly_Rent"] = input("Enter new Monthly_Rent : ")
    blockchain.chain[s_block]["data"]["Current_Roomer"] = input("Enter new Current_Roomer : ")
    blockchain.chain[s_block]["data"]["District"] = input("Enter new District : ")
    blockchain.chain[s_block]["data"]["Province"] = input("Enter new Province : ")

    blockchain.chain[s_block]["block_hash"] = blockchain.hash(blockchain.chain[s_block],blockchain.chain[s_block]["nonce"])

    print("=======================================\n")
    print("block index :",blockchain.chain[s_block]["index"])
    print("timestamp :",blockchain.chain[s_block]["timestamp"])
    print("nonce :", blockchain.chain[s_block]["nonce"])
    print()
    print("Dormitory_Name :",blockchain.chain[s_block]["data"]["Dormitory_Name"])
    print("Room_Number :",blockchain.chain[s_block]["data"]["Room_Number"])
    print("Monthly_Rent :",blockchain.chain[s_block]["data"]["Monthly_Rent"])
    print("Current_Roomer :",blockchain.chain[s_block]["data"]["Current_Roomer"])
    print("District :",blockchain.chain[s_block]["data"]["District"])
    print("Province :",blockchain.chain[s_block]["data"]["Province"])
    print()
    print("Block Hash :",blockchain.chain[s_block]["block_hash"])
    print("Previous Hash :",blockchain.chain[s_block]["previous_hash"])
    print("\n=======================================\n")



#add block
@app.route('/mining', methods=["GET"])
def mining_block():

    #data
    data = create_data()

    #pow
    previous_block = blockchain.get_previous_block()
    previous_nonce = previous_block["nonce"]

    #nonce
    nonce = 1

    #hash previous block
    previous_hash = previous_block["block_hash"]

    #update new block
    block = blockchain.create_block(nonce, previous_hash, data)
    blockchain.proof_of_work(block, previous_nonce)
    
    response = {
        "message" : "Mining Block completed",
        "index" : block["index"],
        "timestamp" : block["timestamp"],
        "nonce" : block["nonce"],
        "data" : block["data"],
        "previous_hash" : block["previous_hash"]
    }
    
    return jsonify(response),200

def add_new_block():

    #data
    data = create_data()

    #pow
    previous_block = blockchain.get_previous_block()
    previous_nonce = previous_block["nonce"]

    #nonce
    nonce = 1

    #hash previous block
    previous_hash = previous_block["block_hash"]

    #update new block
    block = blockchain.create_block(nonce, previous_hash, data)
    blockchain.proof_of_work(block, previous_nonce)

    print("Mining Block completed\n")
    print("=======================================\n")
    print("block index :",block["index"])
    print("timestamp :",block["timestamp"])
    print("nonce :",block["nonce"])
    print()
    print("Dormitory_Name :",block["data"]["Dormitory_Name"])
    print("Room_Number :",block["data"]["Room_Number"])
    print("Monthly_Rent :",block["data"]["Monthly_Rent"])
    print("Current_Roomer :",block["data"]["Current_Roomer"])
    print("District :",block["data"]["District"])
    print("Province :",block["data"]["Province"])
    print()
    print("Block Hash :",block["block_hash"])
    print("Previous Hash :",block["previous_hash"])
    print("\n=======================================\n")

def create_block_with_no_input(data):
    #pow
    previous_block = blockchain.get_previous_block()
    previous_nonce = previous_block["nonce"]

    #nonce
    nonce = 1

    #hash previous block
    previous_hash = previous_block["block_hash"]

    #update new block
    block = blockchain.create_block(nonce, previous_hash, data)

    blockchain.proof_of_work(block, previous_nonce)
    
    response = {
        "message" : "Mining Block completed",
        "index" : block["index"],
        "timestamp" : block["timestamp"],
        "nonce" : block["nonce"],
        "data" : block["data"],
        "previous_hash" : block["previous_hash"]
    }
    
    return response

@app.route('/is_valid', methods = ["GET"])
def is_vaild() :
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {"message":"Blockchain valid"}
    else :
        response = {"message":"Have Problem, Blockchain Is Not Valid"}
    return jsonify(response),200

def valid() :
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {"message":"Blockchain valid"}
    else :
        response = {"message":"Have Problem, Blockchain Is Not Valid"}
    print(response["message"])

#create block
create_block_with_no_input(testdata.data1)
create_block_with_no_input(testdata.data2)
create_block_with_no_input(testdata.data3)
create_block_with_no_input(testdata.data4)
create_block_with_no_input(testdata.data5)
create_block_with_no_input(testdata.data6)
create_block_with_no_input(testdata.data7)
create_block_with_no_input(testdata.data8)
create_block_with_no_input(testdata.data9)
create_block_with_no_input(testdata.data10)
create_block_with_no_input(testdata.data11)


#ใช้งาน Blockchain
if __name__ == "__main__" :
    while True :
        print("=======================================\n")
        print("============= Select Mode =============")
        print("1 : add new block")
        print("2 : show all block")
        print("3 : show block by Current_Roomer")
        print("4 : edit block (for test is blockchain valid)")
        print("5 : valid")
        print("0 : exit")
        print("\n=======================================\n")

        try :
            s_mode = int(input("Mode : "))
        except :
            print("input integer")
            continue
        if s_mode == 1 :
            add_new_block()
        elif s_mode == 2:
            get_all_block()
            pass
        elif s_mode == 3:
            get_block()
            pass
        elif s_mode == 4:
            edit_block()
        elif s_mode == 5:
            valid()
        elif s_mode == 0:
            break
        else :
            print("invalid input")

    #input = int(input("Select Mode : "))

    #app.run()
    #encoded first block
    #print(blockchain.hash(blockchain.chain[0]))