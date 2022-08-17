
from flask import Flask, request
import uuid
import json
import requests

# Создаем экземпляр узла
app = Flask(__name__)

node_uuid = uuid.uuid4()

nodes = set()

@app.route('/myip', methods=['GET'])
async def myip():
    host = request.environ['REMOTE_ADDR']
    port = request.environ['REMOTE_PORT']
    return str((host, port))

@app.route('/requestmyip', methods=['POST'])
async def requestmyip():
    
    responce = requests.get('http://localhost:5000/myip')
    print(responce.content)
    return {'status':'requested'}


@app.route('/node_uuid', methods=['GET'])
async def get_node_uuid():
    return str(node_uuid)
  
@app.route('/healthcheck', methods=['GET'])
async def healthcheck():
    return {'status':'live'}

@app.route('/connect', methods=['POST'])
async def connect():
    '''
    when node want to connect to other nodes, this request is called 
    '''
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        print(request.environ['REMOTE_ADDR'])
        print(request.environ['REMOTE_PORT'])
    # call node.uuid
    for node in nodes:
        #call node.accept_connect(...)
        pass
    return str(nodes)
    

@app.route('/accept_connect', methods=['POST'])
async def accept_connect():
    '''
    when node want to connect to other nodes, this request is called 
    '''
    pass

 
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)


