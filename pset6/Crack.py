from crypt import crypt
from sys import argv,exit

def main():

    #Check hash
    if len(argv) != 2:
        print("Usage: python crack.py hash")
        exit(1)

    #Get hash
    hash = argv[1]

    #Alphabet list
    alphabet = list("0") + list(chr(a) for a in range(65,91)) + list(chr(a) for a in range(97,123))

    guess = ""
    
    for i in alphabet:
        for j in alphabet:
            for  k in alphabet:
                for l in alphabet:
                    for m in alphabet:
                        if i != "0": guess += i
                        if j != "0": guess += j
                        if k != "0": guess += k
                        if l != "0": guess += l
                        if m != "0": guess += m
                        
                        if check_match(hash,guess):
                            print(guess)
                            exit(0)
                        else:
                            guess = ""

    print("Invalid hash password !!!")                               
                        

def check_match(hash,guess):

    salt = hash[0:2]
    guess_hash = crypt(guess,salt)

    return guess_hash == hash

if __name__ == "__main__":
    main()