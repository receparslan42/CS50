from cs50 import get_string
from sys import argv


def main():
    #Check usage
    if len(argv) != 2:
        print("Usage: python Bleepnere.py dictionray")
        exit(1)
    
    #Get message
    print("What message would you like to censor?")
    message = input()
    message = list(message.split())

    #Open file
    file = open(argv[1],"r")

    #Set list from file
    data = []
    for i in file.readlines():
        data.append(i.replace("\n",""))

    counter = 0;

    #Check and print message
    for i in message:
        check = True
        counter+=1

        #Check banned words
        for j in range(len(data)):
            if i.casefold() == data[j].casefold():
                for k in range(len(i)):
                    print("*",end="")
                print(" ",end="")
                check = False
                break

        #print message
        if check:
            print(i,end="")
            if counter == len(message):
                print()
            else:
                print(" ",end="")

    #Close file
    file.close()

    


if __name__ == "__main__":
    main()
