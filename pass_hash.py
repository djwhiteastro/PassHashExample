#!/usr/bin/env python

'''
Hash testing script
Created by Darren White
Last modified: 2018-04-03
'''

import hashlib
import itertools
import random
import base64
import struct
import getpass
import sys
import argparse
import pickle

if sys.version_info.major == 3:
    get_input = input
if sys.version_info.major == 2:
    get_input = raw_input


def parse_command_line(description=("This basic tool allows people to input, "
    "save and load hashed, salted and pickled passwords. For education only, "
    "obvs.")):

    """
    Parser of command line arguments for SeqQC.py
    """

    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("-s", "--save", default=None, metavar='<filename>',
        help="Output file to save password hashes")
    parser.add_argument("-t", "--test", default=None, metavar='<filename>',
        help="Input file containing hashed password information")

    return parser.parse_args()

class Hash(object):
    ''' Creates object which stores hashed password and provides test '''
    def __init__(self):
        self.salt = self._MakeSalt()
        self.hashes = {}
        self.pwd = {}

    @staticmethod
    def _MakeSalt():
        '''This could be much better, but I took a basic version off stack
        exchange'''
        rand_float = random.SystemRandom().random()
        # print(rand_float)
        # print(base64.b64encode((struct.pack('!d', rand_float))))
        return base64.b64encode((struct.pack('!d', rand_float)))

    def HashPwd(self, txt):
        ''' Hashes password and letter combos'''
        m = hashlib.sha256()
        m.update(("{}{}".format(txt, self.salt)).encode('utf-8'))

        self.pwd.update({'pwd': m.hexdigest()})

        triplets = list(itertools.combinations(range(len(txt)), 3))

        for chars in triplets:
            m = hashlib.sha256()
            m.update("{}{}{}{}".format(txt[chars[0]], txt[chars[1]],
                txt[chars[2]], self.salt).encode('utf-8'))
            self.hashes.update({tuple(chars): m.hexdigest()})
            # print("{}: {}".format(chars, m.hexdigest()))

    def TestInput(self):
        '''Asks user for random letters from their password, and tests if
        correct'''
        combo_idx = random.randint(0, len(self.hashes)-1)
        hashidx = list(self.hashes.keys())
        combo = hashidx[combo_idx]
        one = get_input("Enter letter {}: ".format(combo[0]+1))
        two = get_input("Enter letter {}: ".format(combo[1]+1))
        thr = get_input("Enter letter {}: ".format(combo[2]+1))

        m = hashlib.sha256()
        m.update((one+two+thr+self.salt).encode('utf-8'))
        in_hash = m.hexdigest()
        test_hash = self.hashes[combo]

        if test_hash == in_hash:
            print("Congrats! You know your password!")
        else:
            print("That doesn't match... Did you put in the right letters?")
            print("Maybe you should try again!")
            sys.exit()

    def LoadHash(self, infile):
        ''' Loads hash from pickled file (needs to be same format as made by
        this script: salt, hash indeces, hashes)'''
        try:
            hash_file = open(infile, 'rb')
            print("Found input hash file, loading into hash object")
        except IOError:
            sys.exit("Error opening file to load hash, or something...")

        self.salt = str(pickle.load(hash_file))
        self.hashes = pickle.load(hash_file)
        hash_file.close()

        print("Now testing user knows their password!")
        self.TestInput()
        get_input("Press Enter key to print all hash combinations")
        self.print_hashes()

    def SaveHash(self, outfile):
        ''' Saves hash from pickled file to be loaded later'''
        try:
            hash_file = open(outfile, 'wb')
        except IOError:
            sys.exit("Error opening file to save hash, or something...")
        print("Random salt is: {}".format(self.salt))
        pwd1 = getpass.getpass("Input password: ")
        pwd2 = getpass.getpass("Reinput password: ")
        if pwd1 != pwd2:
            sys.exit("Error! Passwords don't match!")
        print("Hashing password and saving to file {}".format(args.save))
        self.HashPwd(pwd1)

        #Clear password variables, actual password no longer stored
        pwd1, pwd2 = None, None

        pickle.dump(self.salt, hash_file)
        pickle.dump(self.hashes, hash_file)

        hash_file.close()

    def print_hashes(self):
        ''' Prints hashes for each combo of letters'''
        for line in self.hashes:
            print("{}: {}".format(line, self.hashes[line]))

if __name__ == '__main__':
    args = parse_command_line()
    print("Hello!")
    print("Initiating hash object and generating random salt")
    myHash = Hash()
    if args.test:
        myHash.LoadHash(args.test)
    elif args.save:
        myHash.SaveHash(args.save)
    else:
        sys.exit("No options given. Exiting.")
