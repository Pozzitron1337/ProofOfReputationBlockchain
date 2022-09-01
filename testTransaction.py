from primitives.transaction import Transaction

from eth_account import Account 

t1 = Transaction("adsads")
h_t1 = t1.getDataHash()
print(h_t1)
privateKey = "0x93efa01b2fe654a78f8ab8bafda18369cba7308db872f47d149f388a821ee19e"
a2 = Account.from_key("0x93efa01b2fe654a78f8ab8bafda18369cba7308db872f47d149f388a821ee19e")
print(a2.address)
s = t1.getSigners()
print(s)

t1.sign(privateKey=privateKey)

s = t1.getSigners()
print(s)