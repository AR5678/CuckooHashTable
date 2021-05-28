# "I hereby certify that this program is solely the result of my own work and is in compliance with the Academic Integrity policy of the course syllabus and the academic integrity policy of the CS department.”

# Cuckoo Hash Tables are important becuase they allow O(1) find time. 
# The Cuckoo Hash Table can see if a key, data pair was inserted with O(1). 

from BitHash import BitHash
from BitHash import ResetBitHash
import pytest
import random

class Link(object):
    def __init__(self, key, data):
        self.key = key
        self.data = data

class CuckooHash(object):
    def __init__(self, size):
        # do not allow Cuckoo HashTable size 0. turn it into size 1
        if size == 0:
            size = 1
        self.__size = size
        self.__hashArr1 = [None] * size
        self.__hashArr2 = [None] * size
        self.__numKeys = 0
    
    # this function allows us to print both hashtables    
    def printAll(self):
        # for each bucket in the first hashTable
        for l in self.__hashArr1:
            # if there is something there, print the key/data pair
            if l:
                print("Key:", l.key, "Data:", l.data)   
                
        print("the second table is")
        
        # for each bucket in the second second hashTable
        for l in self.__hashArr2:
            # if there is something there, print the key/data pair
            if l:
                print("Key:", l.key, "Data:", l.data)          
    
    
    # insert key and data if the key isn't already in the tables. 
    def insert(self, key, data):
        # check that the key is not in the two hashtables already. 
        # if the key is already in the table, return False.
        if self.find(key) != False:
            return False   
        
        # make a new node and add one to numKeys
        newLink = Link(key, data)
        self.__numKeys += 1
        
        # hash the key to find the position in the first hash table it should go in
        hash1 = BitHash(key)
        bucket = hash1 % self.__size
        # get what is in that position
        l = self.__hashArr1[bucket]
        
        # if there is nothing in the positon where our key and data should go, 
        if l == None:
            # create a new link and put the new link in the first hash Table 
            self.__hashArr1[bucket] = newLink
            return True            
        
        # if there is something in the l position
        else:
            # set the node that we will evict to be temp
            temp = self.__hashArr1[bucket]
            # put the new node in the correct bucket
            self.__hashArr1[bucket] = newLink
            
            for i in range(2): # run this code twice 
                evictions = 0
                # loop though the hashtables- evicting if there is a key present where the temp key should go
                # stop looping when the evictions reach 50.
                while temp and evictions <= 50:
                    
                    # rehash the key we evicted from hash table 1 into hashTable2
                    seed = BitHash(temp.key)
                    # get what is in the position in the second hashtable, and increment evictions by 1
                    bucket = BitHash(temp.key, seed) % self.__size
                    
                    # if there nothing in the second hash table, put temp there.
                    if self.__hashArr2[bucket] == None:
                        self.__hashArr2[bucket] = temp
                        return True
                    
                    # if there is something in the second hash table
                    else:
                        temp2 = self.__hashArr2[bucket]
                        evictions += 1
                        self.__hashArr2[bucket] = temp
                        
                    position2 = BitHash(temp2.key) % self.__size
                    
                    if self.__hashArr1[position2] == None:
                        self.__hashArr1[position2] = temp2
                        return True
                    
                    else:
                        # set what was in that position in table 1 equal to temp and repeat the while loop
                        temp = self.__hashArr1[position2]  
                        evictions += 1
                        self.__hashArr1[position2] = temp2
                        
                # if we need to evict more than 50 times, grow the table
                self.__growHash()    
                
        
    def __growHash(self):
        # reset the BitHash
        ResetBitHash()
        # change the size of the array to be double
        self.__size = 2 * len(self.__hashArr1)
        
        # make two temp hashTable double the length as the old arrays
        newHash1 = self.__size * [None]
        newHash2 = self.__size * [None]
        
        # loop through the second hashTable.
        for i in self.__hashArr2:
            
            # if there is something in hashArray2 position i, hash the key of that link and get the position
            if i:
                hashed = BitHash(i.key) % len(newHash1)
                
                # if the position the key should be in (in the new hashTable) is none, place i there
                if newHash1[hashed] == None:
                    newHash1[hashed] = i
                
                # if there is something in the hash array
                else:
                    # get what is in that position and set that position to be i
                    temp = newHash1[hashed]
                    newHash1[hashed] = i
                    
                    evictions = 0
                    # loop through evicting and reBithashing.
                    while temp != None and evictions <= 50:
                        # find what buck the temp should go in the second hashTable
                        seed = BitHash(temp.key)
                        bucket = BitHash(temp.key, seed) % self.__size
                        # get what is in that position
                        inHash2 = newHash2[bucket]
                        
                        # if the second hash array is empty, put temp there
                        if inHash2 == None:
                            newHash2[bucket] = temp
                            temp = None
                            
                        # if the new hash array2 is not empty, get what is there as temp2 
                        else:
                            temp2 = newHash2[bucket]
                            evictions += 1
                            newHash2[bucket] = temp
                        
                        # if temp does not equal None, get the position where temp2 should go into the first array. 
                        if temp != None:
                            position2 = BitHash(temp2.key) % self.__size
                            
                        # if that position is None, set it to be temp2 and set temp to be None
                        if temp != None and newHash1[position2] == None:
                            newHash1[position2] = temp2
                            temp = None
                            
                        elif temp != None:
                            # set what was in that position in table 1 equal to temp and repeat the while loop
                            temp = newHash1[position2]  
                            evictions += 1
                            
                            newHash1[position2] = temp2        
        
        
        # iterates through the old first array, re-inserting all the existing key/data pairs from the old array into the newer, larger array.
        for i in self.__hashArr1:
            
            # if there is something in hashArray1 position i, hash the key of that link and get the position
            if i:
                hashed = BitHash(i.key) % len(newHash1)
                
                # if the position the key should be in (in the new hashTable) is none, place i there
                if newHash1[hashed] == None:
                    newHash1[hashed] = i
                
                # if there is something in the hash array, get what is in there and put i there
                else:
                    temp = newHash1[hashed]
                    newHash1[hashed] = i
                    
                    evictions = 0
                    while temp != None and evictions <= 50:
                        seed = BitHash(temp.key)
                        bucket = BitHash(temp.key, seed) % self.__size
                        # get what is in that position
                        inHash2 = newHash2[bucket]
                        
                        # if the second hash array is empty, put temp there
                        if inHash2 == None:
                            newHash2[bucket] = temp
                            temp = None
                            
                        # if the new hash array2 is not empty, get what is there as temp 
                        else:
                            temp2 = newHash2[bucket]
                            evictions += 1
                            newHash2[bucket] = temp
                        
                        # if temp does not equal None, get the position where temp2 should go into the first array. 
                        if temp != None:
                            position2 = BitHash(temp2.key) % self.__size
                        
                        # if that position is None, set it to be temp2 and set temp to be None
                        if temp != None and newHash1[position2] == None:
                            newHash1[position2] = temp2
                            temp = None
                            
                        elif temp != None:
                            # set what was in that position in table 1 equal to temp and repeat the while loop
                            temp = newHash1[position2]  
                            evictions += 1
                            
                            newHash1[position2] = temp2
                            
        # change our private attributes to be the new larger hashTables                
        self.__hashArr1 = newHash1
        self.__hashArr2 = newHash2
        
    # tries to see if the key is in the HashArray. This is where O(1) shines!
    def find(self, key):
        # hash the key to identify the bucket where the key might be in the first HashTable and mod it by the size to get the position in the table
        seed = BitHash(key)
        bucket = seed % self.__size
        
        # get whatever is at that position in HashTable1
        l = self.__hashArr1[bucket]
        
        # if there is something in the first hashTable, and the key matches the key we are looking for, return True
        if l:
            if l.key == key:
                return l.data
        
        # check the second position too (the key could be in the second position without the first one beign filled in the case where there is a remove)
        
        # hash the key with a seed from the other hash to get the bucket the key might be in the second HashTable
        bucket2 = BitHash(key, seed) % self.__size
        l2 = self.__hashArr2[bucket2] 
        # if the key in the second table matches the key we are looking for, return True
        if l2:
            if l2.key == key:
                return l2.data
        
        # if we get here, the key was not found in the hashTables and return False
        return False
    
    # removes the key in the hashTable. Returns the data of the key we just removed. 
    # the key can be in two positions - one position in the first table and one in the second
    def remove(self, key):
        ans = None
        # get the position in the first hash Table the key should be in
        seed = BitHash(key)
        bucket = seed % self.__size
        l = self.__hashArr1[bucket]
        
        # if that position is filled and the key matches the key we are looking for, set ans equal to the key data
        if l:
            if l.key == key:
                ans = l.data
                # set the bucket to be None and remove 1 to the number of Keys in the tables
                self.__hashArr1[bucket] = None
                self.__numKeys -= 1
                return ans
        
        # check the second table to remove the key
        bucket = BitHash(key, seed) % self.__size
        l2 = self.__hashArr2[bucket]
        if l2:
            if l2.key == key:
                ans = l2.data
                self.__hashArr2[bucket] = None
                self.__numKeys -= 1
                return ans
            
        return None
    
    # return the number of keys in both tables
    def __len__(self):
        return self.__numKeys

# pytests 
def test_tryInsert():
    h = CuckooHash(10)
    h.insert("aaa", 32)
    h.insert("bbb", 22)
    h.insert("ccc", 2)
    h.insert("ddd", 3)
    h.insert("ggg", 4)
    h.insert("eee", 6)
    h.insert("yyy", 7)
    h.insert("iii", 8)
    h.insert("ppp", 9)    
    
    assert len(h) == 9
    
def test_trySameInsert():
    h = CuckooHash(10)
    h.insert("aaa", 1)
    h.insert("bbb", 2)
    h.insert("ccc", 3)
    
    h.insert("bbb", 4)
    h.insert("ccc", 5)
    
    assert len(h) == 3
    
def test_tryManySameInsert():
    h = CuckooHash(30)
    h.insert("aaa", 32)
    h.insert("bbb", 22)
    h.insert("ccc", 2)
    h.insert("ddd", 8)
    h.insert("dog", 1)
    h.insert("cat", 1)
    
    h.insert("aaa", 3)
    h.insert("bbb", 4)
    h.insert("ccc", 5)
    h.insert("ddd", 7)
    h.insert("ddd", 8)
    h.insert("dog", 1)
    h.insert("cat", 1)    
    
    assert len(h) == 6 
    
def test_tryingFindAfterInsert():
    h = CuckooHash(30)
    h.insert("aaa", 32)
    h.insert("bbb", 22)
    h.insert("ccc", 2)
    h.insert("ddd", 8)
    h.insert("dog", 1)
    h.insert("cat", 1)
    
    assert h.find("aaa") == 32
    assert h.find("bbb") == 22
    assert h.find("ccc") == 2
    assert h.find("dog") == 1
    
    assert len(h) == 6 

def test_insertAndFindColors():
    h = CuckooHash(1000)
    listStr = ["red", "orange", "yellow", "blue", "green", "purple", "pink", "gray", "black", "brown", "silver", "gold", "sky", "black", "white", "light blue", "grass", "tan", "pearl", "cobalt", "amber", "blush"]
    # insert the list of colors
    for i in range(len(listStr)):
        h.insert(listStr[i], i)
    
    # try finding things not inserted        
    listNotIn = ["red2", "orange2", "yellow2", "blue2", "green2", "purple2"]
    for i in range(len(listNotIn)):
        if h.find(listNotIn[i]) != False:
            assert False    # just found something we never inserted
    
    assert True

def test_tryEmptyHash():
    # try testing an empty hashTable
    h = CuckooHash(3)
    assert len(h) == 0
    assert h.find("hey") == False

def test_tryZeroHash():
    # try testing an empty hashTable
    h = CuckooHash(0)
    assert len(h) == 0
    assert h.find("hey") == False

def test_growHashAnimal():
    h = CuckooHash(3)
    listStr = ["lion", "bear", "tiger", "chimp", "parrot"]
    # insert the list of colors
    for i in range(len(listStr)):
        h.insert(listStr[i], i)
        
    # try finding everything inserted
    for i in range(len(listStr)):
        if h.find(listStr[i]) != i:
            assert False
    assert True
    
def test_growHashLetter():
    h = CuckooHash(3)
    listStr = ["a1", "a2", "a3", "a4", "a5", "a6", "a7", "a8", "a9", "a10", "a11", "a12", "a13", "a14"]
    
    # insert the list of colors
    for i in range(len(listStr)):
        h.insert(listStr[i], i)
        
    # try finding everything inserted
    for i in range(len(listStr)):
        if h.find(listStr[i]) != i:
            assert False
            
    assert True

def test_growHashColors():
    h = CuckooHash(10)
    listStr = ["red", "orange", "yellow", "blue", "green", "purple", "pink", "gray", "black", "brown", "silver", "gold", "sky", "black", "white", "light blue", "grass", "tan", "pearl", "cobalt", "amber", "blush"]
    # insert the list of colors
    for i in range(len(listStr)):
        h.insert(listStr[i], i)
    
    # try finding things not inserted        
    listNotIn = ["red2", "orange2", "yellow2", "blue2", "green2", "purple2"]
    for i in range(len(listNotIn)):
        if h.find(listNotIn[i]) == True:
            assert False    # just found something we never inserted
    
    assert True

def test_trySmallRemove():
    h = CuckooHash(5)
    h.insert("aaa", 32)
    h.insert("bbb", 22)
    
    h.remove("aaa")
    
    assert h.find("bbb") == 22
    assert h.find("aaa") == False
    assert len(h) == 1   

def test_largeRemove():
    h = CuckooHash(40)
    listStr = ["red", "orange", "yellow", "blue", "green", "purple", "pink", "gray", "black", "brown", "silver", "gold", "sky", "black", "white", "light blue", "grass", "tan", "pearl", "cobalt", "amber", "blush"]
    # insert the list of colors
    for i in range(len(listStr)):
        h.insert(listStr[i], i)
    
    #assert len(h) == len(listStr) # everything got inserted
        
    for i in range(len(listStr)):
        h.remove(listStr[i])    
        
    for i in range(len(listStr)):
        if h.find(listStr[i]) != False:
            assert False

def test_growAndRemove():
    h = CuckooHash(1)
    
    # insert 
    for i in range(500):
        h.insert(str(i) + "aa", random.random())
    
    # try removing everything inserted
    for i in range(500):
        h.remove(str(i) + "aa")
            
    # make sure I cannot find everything
    for i in range(500):
        if h.find(str(i) + "aa") == True:
            # I found something I wasn't supposed too
            assert False
            
    assert True
            

pytest.main(["-v", "-s", "CuckooHashTable.py"])