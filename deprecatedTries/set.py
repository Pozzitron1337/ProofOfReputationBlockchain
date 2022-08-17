
import json

s = {'http://127.0.0.1:5000', 'http://127.0.0.1:5001'}

print(type(s))

print(s)

s_str = str(s)
print(s_str)

l = list(s)
print(l)

j = json.dumps(f'{l}')
print(j)

ls = set(l)

print(ls)


jl = json.loads('["http://127.0.0.1:5000", "http://127.0.0.1:5001"]')

print(len(jl))

