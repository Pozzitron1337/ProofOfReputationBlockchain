import json
from aiohttp import web
import aiohttp

class ProofOfReputationNode:

    def __init__(self) -> None:
        self.nodes = set()

    def __repr__(self) -> str:
        pass

    async def test(self, request):
        responce_obj = {'status': 'test'}
        return web.Response(text=json.dumps(responce_obj), status=200)

    async def healthcheck(self, request):
        responce_obj = {'status': 'live'}
        return web.Response(text=json.dumps(responce_obj), status=200)

    async def remote(self,request):
        print(request.remote)
        return web.Response(text=str(request.remote), status=200)
    
    async def ab(self,request):
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:8080/remote') as resp:
                print(resp.status)
                text = await resp.text()
                print(text)
        return web.Response(text=str(text), status=200)

    async def attachToBlockchain(self, request):
        '''
        requester is node, that will attach to blockchain
        request: http://<ip>:<port>/attachToBlockchain?nodeIPAddress='<ip_address_of_node_to_connect>'
        responcer will send the other ip addresses of nodes in network
        '''
        print(request.remote)
        return web.Response(text='attach', status=200)
        

    async def connectToBlockchain(self, request):
        '''
        requester is blockchain node, that a
        '''
        nodeAddress = request.query['nodeAddress']
        print(dir(request))
        self.nodes.add(nodeAddress) # add new node to local set of nodes
        # broadcast that there are new node
        return web.Response(text=str(self.nodes), status=200)

    async def getNodes(self, request):
        '''
        return ip addresses of nodes which participate in making blocks
        '''
        return web.Response(text=str(self.nodes), status=200)



if __name__ == "__main__" :
    print("hello")
    node = ProofOfReputationNode()
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(node.broadcast())
    # nodes = set()
    # print(nodes)
    # nodes.add('http://localhost:8034')
    # nodes.add('http://localhost:8032')
    # nodes.add('http://localhost:8035')
    # nodes.add('http://localhost:8032')
    # nodes.add('http://localhost:8035')
    # print(nodes)
    # for node in nodes:
    #     print(node)

    app = web.Application()
    app.router.add_get('/', node.test)
    app.router.add_get('/healthcheck', node.healthcheck)
    app.router.add_get('/nodes', node.getNodes)
    app.router.add_get('/remote', node.remote)
    app.router.add_post('/attachToBlockchain', node.attachToBlockchain)
    app.router.add_get('/ab', node.ab)
    web.run_app(app, port=8081)


   