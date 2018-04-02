#!/usr/bin/env python

''' Hash testing script'''

import hashlib
import itertools
import random
import base64
import struct
import getpass
import sys


class Hash(object):
    ''' Creates object which stores hashed password and provides test '''
    def __init__(self):
        self.salt = self._make_salt()
        self.hashes = {}
        self.pwd = {}
        self.hashidx = []

    @staticmethod
    def _make_salt():
        '''This could be much better, but I took a basic version off stack
        exchange'''
        rand_float = random.SystemRandom().random()
        # print(rand_float)
        # print(base64.b64encode((struct.pack('!d', rand_float))))
        return base64.b64encode((struct.pack('!d', rand_float)))

    def hash_pwd(self, txt):
        ''' Hashes password and letter combos'''
        m = hashlib.sha256()
        m.update(txt+self.salt)

        self.pwd.update({'pwd': m.hexdigest()})

        triplets = list(itertools.combinations(range(len(txt)), 3))

        for chars in triplets:
            m = hashlib.sha256()
            m.update(txt[chars[0]]+txt[chars[1]]+txt[chars[2]]+self.salt)
            self.hashidx.append(tuple(chars))
            self.hashes.update({tuple(chars): m.hexdigest()})
            # print("{}: {}".format(chars, m.hexdigest()))

    def test_input(self):
        '''Asks user for random letters from their password, and tests if
        correct'''

        combo_idx = random.randint(0, len(self.hashes)-1)
        combo = self.hashidx[combo_idx]
        one = raw_input("Enter letter {}: ".format(combo[0]+1))
        two = raw_input("Enter letter {}: ".format(combo[1]+1))
        thr = raw_input("Enter letter {}: ".format(combo[2]+1))

        m = hashlib.sha256()
        m.update(one+two+thr+self.salt)
        in_hash = m.hexdigest()
        test_hash = self.hashes[combo]

        if test_hash == in_hash:
            print("Congrats! You know your password!")
        else:
            print("Erm, something went wrong...")

    def print_hashes(self):
        ''' Prints hashes for each combo of letters'''
        for line in self.hashes:
            print("{}: {}".format(line, self.hashes[line]))

if __name__ == '__main__':
    print("Hello!")
    print("Creating hash object and generating random salt")
    myHash = Hash()
    print("Salt is: {}".format(myHash.salt))
    pwd1 = getpass.getpass("Input password: ")
    pwd2 = getpass.getpass("Reinput password: ")
    if pwd1 != pwd2:
        sys.exit("Error! Passwords don't match!")
    myHash.hash_pwd(pwd1)
    # print(myHash.hashes)
    myHash.test_input()
    raw_input("Press any key to print all hash combinations")
    myHash.print_hashes()
