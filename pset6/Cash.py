while True:
    money = input("Change owed:")
    counter=0
    for i in money:
        if i.isnumeric() or i=='.':
            counter+=1
    if counter == len(money):
            money =float(money)*100
            break

n=0
while money>=25:
    n+=int(money/25)
    money %=25

while money>=10:
    n+=int(money/10)
    money %=10

while money>=5:
    n+=int(money/5)
    money %=5

n+=int(money/1)
print(n)