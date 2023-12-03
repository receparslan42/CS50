while True:
    carddigit = 0
    card = input("Card Number:")
    if card.isnumeric():
        for i in card:
            carddigit+=1
        if carddigit == 13 or 15 or 16:
            card = int(card)
            break

sum =0
list = []
for i in range(carddigit-1,0,-2):
    list.append((int(str(card)[i-1]))*2) 
for i in range(len(list)):
    if list[i] >= 10:
        sum += int((str(list[i]))[0]) + int((str(list[i]))[1])
    else:
        sum += list[i]

for i in range(carddigit,0,-2):
    sum += int(str(card)[i-1])

if sum%10==0:
    if str(card)[0] == "3" and str(card)[1] == "4" or "7" and carddigit == 15:
        print("AMEX")
    elif carddigit == 13 and str(card)[0] == "4":
        print("VISA")
    elif carddigit == 16:
        if str(card)[0] == "4":
            print("VISA")
        elif str(card)[0] == "5" and str(card)[1] == "1" or "2" or "3" or "4" or "5":
            print("MASTERCARD")
        else:
            print("INVALID")
    else:
        print("INVALID")
else:
    print("INVALID")
