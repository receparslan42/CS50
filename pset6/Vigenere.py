from sys import argv,exit

def main():
    #Check usage
    if len(argv) != 2:
        print("Usage: python Vigenere.py k")
        exit(1)
    elif not argv[1].isalpha():
        print("Usage: python Vigenere.py k")
        exit(1)

    #Define values
    plaintext = input("plaintext: ")
    lengt = len(argv[1])
    ciphertext = ""
    l = 0

    for i in plaintext:

        #Check length of key
        if l == lengt:
            l = 0

        #Check if letter in alphabet
        if i.isalpha():
            #Check digit of plaintext is lowercase or uppercase
            if i.islower():
                ciphertext += chr((ord(i)%97+shift(argv[1][l]))%26+97)
            else:
                ciphertext += chr((ord(i)%65+shift(argv[1][l]))%26+65)
            l+=1
        else:
            ciphertext += i
    #Print cipher text
    print("ciphertext: "+ciphertext)

#Check digit of key is lowercase or uppercase
def shift(c):
    if c.islower():
        return ord(c)%97
    else:
        return ord(c)%65
    

if __name__ == "__main__":
    main()