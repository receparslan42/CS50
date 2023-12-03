while True:
    height = input("Height:")
    if height.isnumeric() and 0<int(height)<9:
        break

for i in range(int(height)):
    for j in range(int(height)-i-1):
        print(" ",end="")
    for k in range(i+1):
        print("#",end="")
    print(" ",end="")
    for l in range(i+1):
        print("#",end="")
    print()
