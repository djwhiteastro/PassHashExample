# PassHashExample

From a Twitter discussion about services that ask for individual letters
of passwords, I was curious how this can be done without storing the
passwords as plaintext. This script has two modes: save and test, and works
on both Python 2.7 and 3.6 (on my machine at least...)

## Save password

The first stage is to input a password which will be salted, hashed and pickled.
For example:

```shell
python pass_hash.py --save my.pass
```

This takes the password, creates triplets of letters and then salts/hashes the
combinations. These are then pickled for easy access later.

## Test user password

In order to verify that everything worked correctly, you can run:

```shell
python pass_hash.py --test my.pass
```

This will pick a triplet of letters at random, and ask for their values. By
comparing the pickled set of triplets with your input, it is possible to check
that the password is valid, all without actually storing your plaintext
password anywhere.

## Disclaimer

Obviously, this is not a fully-fledged robust way of doing this. It is merely
a quick test to see how something like this might work. If you use this in
anything serious and it turns out that it's not fully secure, that's not my
fault.