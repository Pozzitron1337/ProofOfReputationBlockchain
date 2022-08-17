from primitives.block import Block
from primitives.blockchain import Blockchain
import json

b3 = {'blockNumber': 131, 'leader': '8ed0096d-944c-4844-9d63-e68f862c3ae6', 'transactions': []}
print(type(b3))
a = json.dumps(b3)
print(type(a))
print(a)
b4 = Block()
b4.fromJSON(a)
print(b4.toJSON())

# b1 = Block(4323, "leadrrrr")
# b1_str = b1.toJSON()
# print(f'b1: {b1_str}')
# b2 = Block()
# print(f'b2: {b2.toJSON()}')
# b2.fromJSON(b1_str)
# print(f'b2: {b2.toJSON()}')

