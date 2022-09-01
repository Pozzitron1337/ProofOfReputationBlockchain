from eth_account import Account 
acct = Account.create()
# print(acct.address)
# print(acct.privateKey.hex())


###SIGN###

a2 = Account.from_key("0x93efa01b2fe654a78f8ab8bafda18369cba7308db872f47d149f388a821ee19e")

print(a2.address)
privateKey = a2.privateKey.hex()
print(privateKey)
print(type(privateKey))

messageHash = "0x345fa0199fe654a78f8ab8bafda6669caa7308db872f47d149f388a821ee000"

sign = Account.signHash(messageHash, privateKey)
print()
print(f'{sign}')
print()
print(f'messageHash: {sign.messageHash.hex()}')
print(f'r: {hex(sign.r)}')
print(f's: {hex(sign.s)}')
print(f'v: {hex(sign.v)}')
print(f'signature: {sign.signature.hex()}')

###VERIFICATION###

recoverAccount_signature = Account.recoverHash(message_hash=messageHash, signature=sign.signature.hex())
print(recoverAccount_signature)

recoverAccount_vrs = Account.recoverHash(message_hash=messageHash, vrs=(hex(sign.v), hex(sign.r), hex(sign.s)))
print(recoverAccount_vrs)

recoverAccount_vrs_signature = Account.recoverHash(message_hash=messageHash, vrs=(hex(sign.v), hex(sign.r), hex(sign.s)), signature=sign.signature.hex())
print(recoverAccount_vrs_signature)

