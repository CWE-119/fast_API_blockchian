import fastapi as _fastapi
import blockchain as _blockchain
import hashlib

blockchain = _blockchain.Blockchain()
app = _fastapi.FastAPI()


# endpoint to mine a block
@app.post("/mine_block/")
def show_hash_list(data: str):
    if not blockchain.is_chain_valid():
        return _fastapi.HTTPException(status_code=400, detail="The blockchain is invalid")
    block = blockchain.mine_block(data=data)

    return block


# merkle root
# it hashes the whole blockchain's hashes into one
@app.get("/ merkle root /")
def merkle_roots():
    sha256_hash = hashlib.sha256()
    if not blockchain.is_chain_valid():
        return _fastapi.HTTPException(status_code=400)
    all_prev_hash = str([d['previous_hash'] for d in blockchain.chain])
    sha256_hash.update(all_prev_hash.encode('utf-8'))
    merkle_root = sha256_hash.hexdigest()
    return merkle_root


# show genesis block
@app.get("/genesis block/")
def show_genesis_block():
    if not blockchain.is_chain_valid():
        return _fastapi.HTTPException(status_code=400)
    hash_list = blockchain.chain[0]
    return hash_list


# previous hash to merkle root
@app.get("/all hash list/")
def all_hash_list():
    if not blockchain.is_chain_valid():
        return _fastapi.HTTPException(status_code=400)
    hash_list = [d['previous_hash'] for d in blockchain.chain]
    return hash_list


# endpoint to return the blockchain
@app.get("/blockchain/")
def get_blockchain():
    if not blockchain.is_chain_valid():
        return _fastapi.HTTPException(status_code=400, detail="The blockchain is invalid")
    chain = blockchain.chain
    return chain


# endpoint to see if the chain is valid
@app.get("/validate/")
def is_blockchain_valid():
    if not blockchain.is_chain_valid():
        return _fastapi.HTTPException(status_code=400, detail="The blockchain is invalid")

    return blockchain.is_chain_valid()


# endpoint to return the last block
@app.get("/blockchain/last/")
def previous_block():
    if not blockchain.is_chain_valid():
        return _fastapi.HTTPException(status_code=400, detail="The blockchain is invalid")
    return blockchain.get_previous_block()
