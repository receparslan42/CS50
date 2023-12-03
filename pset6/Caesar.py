from sys import argv,exit

def main ():

    #Check usage
    if len(argv) !=2:
        print("Usage: python caesar.py k")
        exit(1)
    elif not argv[1].isnumeric():
        print("Usage: python caesar.py k")
        exit(1)
    elif int(argv[1]) <= 0:
        print("Usage: python caesar.py k")
        exit(1)
    else:
        #Get plain text
        plaintext = input("plaintext:")

        #Define cipher text
        ciphertext = []

        #Define k
        k = int(argv[1])
        # Get cipher text
        for i in range(len(plaintext)):
            if plaintext[i].islower():
                ciphertext.append(chr(((ord(plaintext[i])%97+k)%26+97)))
            elif plaintext[i].isupper():
                ciphertext.append(chr(((ord(plaintext[i])%65+k)%26+65)))
            else:
                ciphertext.append(plaintext[i])
        #Print cipher text
        print("ciphertext: ",end="")
        for i in range(len(ciphertext)):
            print(ciphertext[i],end="")
        print()

if __name__ == "__main__":
    main()