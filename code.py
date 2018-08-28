from optparse import OptionParser
import os, base64, uuid, hashlib
from Crypto.Cipher import AES
import time
import pickle
  
lastOwnerId = 1
nodeNumber = 0

class Node:
  
  def __init__(self, t, user, **kwargs):
    if t is 0:
      global nodeNumber
      nodeNumber +=1
      self.timestamp = time.time()
      self.nodeNumber = nodeNumber
      self.nodeId = uuid.uuid4().int & (1<<32) - 1
      self.referenceNodeId = None
      self.childReferenceNodeId = ""
      value = float(input("Enter the amount for genesis block in float digits only"))
      self.data = self.encrypt(value=value, owner=user)
      if self.data is False:
         raise ValueError()
      self.hashValue = hashlib.sha256(str([self.timestamp, self.data, self.nodeNumber, self.nodeId, self.referenceNodeId, self.childReferenceNodeId]).encode('utf-8')).hexdigest()
    else:
      pass
    
  def create():
    self.timestamp = time.time()
    self.data = self.encrypt()
    self.nodeNumber = self.setNodeNumber
    
    # dump as pickle
    self.dump(GenesisNode)
    
  def encrypt(self,**kwargs):
    val = 0
    if 'value' in kwargs:
      val = kwargs['value']
    owner = kwargs['owner']
    hashV = hashlib.sha256(str([owner[0], val, owner[1]]).encode()).hexdigest()
    
    
#     if self.referenceNodeId is not None:
#       pass
#       parent = self.referenceNodeId
#       parentNode = findNode(parent)
#       children = parentNode.childReferenceNodeId.split(",")
#       total=0
#       for c in children:
#         total += c.decrypt()
        
    message = str([owner[0], val, owner[1], hashV])
    
    skey = base64.b64decode(owner[2])
    cipher = AES.new(skey)
    padded_private_msg = message + ("_" * ((16-len(message)) % 16))
    encrypted_msg = cipher.encrypt(padded_private_msg)
    encoded_encrypted_msg = base64.b64encode(encrypted_msg)
    return encoded_encrypted_msg
        

def createUser(t):
  global lastOwnerId
  name = input(t + " name:")
  ownerId = lastOwnerId+1
  lastOwnerId+=1
  key = generate_key()
  return [ownerId, name, key]

def generate_key():
  return base64.b64encode(os.urandom(16))

genUser = createUser("Genesis User ")

Nodes = {}
GenesisNode = Node(0, genUser)
Nodes[GenesisNode.nodeId] = GenesisNode
currentNode = GenesisNode

print("==== Genesis Node ===-")
print("NodeNumber: " + str(GenesisNode.nodeNumber))
print("time: " + str(GenesisNode.timestamp))
print("Encrypted Data: "+ str(GenesisNode.data))


user1 = createUser("Another User ");
print("your key: " + str(user1[2]))

users = {}
users[genUser[2]] = genUser
users[user1[2]] = user1

owner = -1

def longestChain(node):
  if seen is None: seen = []
  if path is None: path = []
  path.append(node.nodeId)
  children = node.childReferenceNodeId.split(",")
  if children == "":
    return []
  
  for c in children:
    return path + longestChain(Nodes[c])  
    
    
option = -1

while option is not 0:
  option = input("Type 1 to add child node. Type 2 to find longest chain.")
  
  if option is '1':
    newNode = Node(1, None)
    print("Err! Logic not prepared.")
  elif option is '2':
    print(longestChain())

#   saving the data into pickle
  with open("data.pk", 'wb') as f:
    pickle.dump(Nodes, f)
    
# if __name__ == '__main__':
#   createUser()
#   print("Use this key to create initial child nodes to genesis node.")
#   parser = OptionParser()
#   parser.add_option("-c", "--createUser", help="Create a new User")

#   (options, args) = parser.parse_args()

#   action = input("Enter action to perform")
#   action = 'createUser'
  
#   if action is 'createUser':
#     createUser()
  
