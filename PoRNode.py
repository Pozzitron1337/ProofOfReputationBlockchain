from quart import Quart, request
from enum import Enum
import asyncio
import httpx
import uuid
import json
import sys

from reputationModel.mock.MockReputation import MockReputationModel
from reputationModel.mock.MockIOC import MockIOCModel

from primitives.block import Block
from primitives.blockchain import Blockchain



class NodeState(Enum):
    PREPATING_FOR_ELECTING = 0
    ELECTING_LEADER = 1
    LEADER_ELECTED = 2
    LEADER_CREATING_BLOCK = 3
    BLOCK_ADDED_TO_BLOCKCHAIN = 4

app = Quart(__name__)

node_uuid = uuid.uuid4()

pending_nodes = set()

nodes = set()

transactions = set()

iocModel = MockIOCModel()

isAttachedToNodes = False;

reputationModel = MockReputationModel()

nodeState = NodeState.PREPATING_FOR_ELECTING

blockchain = Blockchain()

async def _background_task(timeout):
    async with httpx.AsyncClient() as client:
        response = await client.get('http://0.0.0.0:5000/test')
        print("Response from test route", response.text)
    await asyncio.sleep(timeout)
    print("I am completed")
 
@app.route("/", methods=["POST", "GET"])
async def main_route():
    print("Hello from main route")
    app.add_background_task(_background_task, 10)
    return "Hello from root"

@app.route("/test", methods=["POST", "GET"])
async def test_route():
    print("Hello from test route")
    #await asyncio.sleep(0.5)
    return "Hello from test"

###################################################################
############### VIEW NODES FUNCTIONALITY ###############

@app.route("/healthcheck", methods=["GET", "POST"])
async def healthcheck():
    return {'status':'live'}

@app.route("/node_uuid", methods=["GET", "POST"])
async def get_node_uuid():
    return node_uuid

@app.route("/node_state", methods=["GET", "POST"])
async def get_node_state():
    return nodeState

@app.route("/nodes", methods=["GET", "POST"])
async def getNodes():
    return str(nodes)

@app.route("/address", methods=["GET", "POST"])
async def getAddress():
    local_node_socket = request.server #get socket of local node
    local_node_host = local_node_socket[0]   #retrieve the host from local_node_socket
    local_node_port = local_node_socket[1]   #retrieve the port from local_node_socket

    return json.dumps(f'http://{local_node_host}:{local_node_port}')

@app.route("/getAddressAsString", methods=["GET", "POST"])
async def getAddressAsString():
    local_node_socket = request.server #get socket of local node
    local_node_host = local_node_socket[0]   #retrieve the host from local_node_socket
    local_node_port = local_node_socket[1]   #retrieve the port from local_node_socket

    return str(f'http://{local_node_host}:{local_node_port}')

###################################################################
############### CONNECT NODES FUNCTIONALITY ###############

@app.route("/attach", methods=["POST"])
async def attach():
    '''
    Attach this node to remote blockchain node
    Request example: http://<node_host>:<node_port>/attach?remote_node_url='<remote_address>'
    Example: http://127.0.0.1:5000/attach?remote_node_url='http://127.0.0.1:5001'
    Steo 0. Verify that this node is not attacher
    Step 1. Check if remote node is live 
    Step 2. If remote node is live, than add to set nodes
    Step 3. Call on remote node method broadcastNewPeer
    Step 4. The responce from remote node will be the nodes in blockchain network. Add this remote nodes
    Step 5. 
    '''
    
    # Step 0
    global isAttachedToNodes
    if isAttachedToNodes: # check that node attached to nodes
        return {'error':'attached'}
    
    # Step 1
    remote_node_url = request.args.get('remote_node_url')   #getting the remote_node_url from request
    #print(remote_node_url)
    try:
        async with httpx.AsyncClient() as client:
            healthcheck_responce = await client.get(f'{remote_node_url}/healthcheck')   #send request to remote node to healthcheck
    except httpx.ConnectError:
        return {'error':'remote server is not live'}
    # Step 2
    nodes.add(remote_node_url)  #add remote node to set of nodes
    
    # Step 3
    local_node_socket = request.server #get socket of local node
    local_node_host = local_node_socket[0]   #retrieve the host from local_node_socket
    local_node_port = local_node_socket[1]   #retrieve the port from local_node_socket
    broadcastNewPeer_url = f'{remote_node_url}/broadcastNewPeer?peer=http://{local_node_host}:{local_node_port}' #form the request to remote node
    print(broadcastNewPeer_url)
    addPeerResponse = None
    try:
        async with httpx.AsyncClient() as client:
            addPeerResponse = await client.post(broadcastNewPeer_url)    #send request to remote node
            print("Response from test route", addPeerResponse.text)
    except:
        return {'error':'failed to attach to network'}
    print(f'AddPeerResponce: {addPeerResponse.text}')

    # Step 4.
    responce_nodes = json.loads(addPeerResponse.text) #list of response nodes
    # print(type(responce_nodes))
    # print(responce_nodes)
    # print(len(responce_nodes))

    for responce_node in responce_nodes:
        print(f'Responce_node: {responce_node}')
        if responce_node in nodes:
            continue
        else:
            nodes.add(responce_node)
    
    print(f'Nodes: {nodes}')

    isAttachedToNodes = True

    return str(node_uuid)

@app.route("/broadcastNewPeer", methods=["POST"])
async def broadcastNewPeer():
    '''
    Broadcasting peer to blockchain network. 
    Request example: http://<node_host>:<node_port>/broadcastNewPeer?peer=http://<peer_node_host>:<peer_node_port>
    Step 1. Check if remote node is live
    Step 2. Add peer to nodes
    Step 3. Call on nodes method addPeer()
    '''
    # http://local_host:local_port/addPeer?peer='http://remote_host:remote_port'
    peer = request.args.get('peer')
    print(f'Peer: {peer}')
    try:
        async with httpx.AsyncClient() as client:
            healthcheck_responce = await client.get(f'{peer}/healthcheck')
    except httpx.ConnectError:
        return {'error':'remote server is not live'}
    try:
        for node in nodes:
            print(f'Node: {node}')
            async with httpx.AsyncClient() as client:
                response = await client.post(f'{node}/addPeer?peer={peer}')
                print("Response from test route", response.text)
    except:
        return {'error':'failed to attach to network'}

    response_to_requester = json.dumps(list(nodes))
    nodes.add(peer)
    print(response_to_requester)
    return response_to_requester

@app.route("/addPeer", methods=["POST"])
async def addPeer():
    '''
    Adding peer to blockchain network. 
    Step 1. Check if remote node is live
    Step 2. Add peer to nodes
    '''
    # http://local_host:local_port/addPeer?peer='http://remote_host:remote_port'
    peer = request.args.get('peer')
    print(f'Peer: {peer}')
    try:
        async with httpx.AsyncClient() as client:
            healthcheck_responce = await client.get(f'{peer}/healthcheck')
    except httpx.ConnectError:
        return {'error':'remote server is not live'}
   
    response_to_requester = {"status":"added"}
    nodes.add(peer)
    print(response_to_requester)
    return response_to_requester

###################################################################
############### ELECTING LEADER FUNCTIONALITY ###############

@app.route("/broadcastElectLeader", methods=["POST"])
async def broadcastElectLeader():
    
    for node in nodes:
        try:
            print(f'Node: {node}')
            async with httpx.AsyncClient() as client:
                response = await client.post(f'{node}/electLeader')
                print("Response from test route", response.text)
        except:
            return {'error':'failed to attach to network'}

@app.route("/electLeader", methods=["POST"])
async def electLeader():
    if nodeState > NodeState.ELECTING_LEADER:
        return {'status' : 'leader elected'}

    node_ioc = await getIoC()
    maxReputation = reputationModel.reputation(node_ioc)
    leader = await getAddressAsString()

    for node in nodes:
        try:
            print(f'Elect Node: {node}')
            async with httpx.AsyncClient() as client:
                node_ioc_responce = await client.get(f'{node}/getIoC')
                print("Response from test route", node_ioc_responce.text)
                print(f'Type ioc response: {type(node_ioc_responce.text)}')
                node_reputation = reputationModel.reputation(node_ioc_responce.text)
                if node_reputation > maxReputation:
                    leader = node
                    maxReputation = node_reputation
        
        except:
            return {'error':'failed to attach to network'}    
    return json.dumps(leader)

@app.route("/getIoC", methods=["GET"])
async def getIoC():
    local_node_socket = request.server #get socket of local node
    local_node_port = local_node_socket[1]   #retrieve the port from local_node_socket
    print(type(local_node_port))
    ioc = iocModel.getIoC(local_node_port)
    return json.dumps(ioc)

###################################################################
############### MINING BLOCK FUNCTIONALITY ###############

@app.route("/mineBlock", methods=["POST"])
async def mineBlock():
    blockNumber = blockchain.getBlockchainLength()
    leader = str(node_uuid)
    block = Block(blockNumber=blockNumber, leader=leader)
    # add transactions to block
    blockchain.addBlock(block)
    data = block.__repr__()
    for node in nodes:
        try:
            print(f'Node: {node}')
            async with httpx.AsyncClient() as client:
                addBlock_responce = await client.post(f'{node}/addBlock',data=data)
        except:
            return {'error':'failed to attach to network'}
    return {'asd':'sda'}

@app.route("/addBlock", methods=["POST"])
async def addBlock():
    '''
    Request example: http://<node_host>:<node_port>/addBlock
    with body that contains JSON format of block
    '''

    data = await request.get_data()
    data_decoded = data.decode() # Type: <class 'str'>
    block = Block()
    block.loadBlockFromJSON(data_decoded)
    blockchain.addBlock(block=block)
    return {'sda':"123"}

@app.route("/getBlock", methods=["GET"])
async def getBlock():
    '''
    Request example: http://<node_host>:<node_port>/getBlock?blockNumber=<blockNumber>
    '''
    blockNumber = request.args.get('blockNumber')
    block = blockchain.getBlock(blockNumber)
    return block.toJSON()

@app.route("/getLastBlock", methods=["GET"])
async def getLastBlock():
    '''
    Request example: http://<node_host>:<node_port>/getLastBlock
    '''
    block = blockchain.getLastBlock()
    return block.toJSON()

@app.route("/getBlockchainLength", methods=["GET"])
async def getBlockchainLength():
    '''
    Request example: http://<node_host>:<node_port>/getBlockchainLength
    '''
    blockchainLength = blockchain.getBlockchainLength()
    return {'blockchainLength' : blockchainLength}

###################################################################
############### TRANSACTION FUNCTIONALITY ###############

@app.route("/transact", methods=["POST"])
async def transact():
    '''
    Request example: http://<node_host>:<node_port>/transact
    with body that contains transaction
    '''
    pass

@app.route("/appendTransaction", methods=["POST"])
async def appendTransaction():
    pass


###################################################################

if __name__ == '__main__':
    from hypercorn.config import Config
    from hypercorn.asyncio import serve
    
    argv = sys.argv
    port = 5000
    if '--port' in argv:
        port = argv[argv.index('--port') + 1] # receive the port from console

    print(port)
    Config.bind = [f'0.0.0.0:{port}']
    asyncio.run(serve(app, Config()))