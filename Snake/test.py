list = [[1,2],[2,3],[4,5]]
last = list[-1]
list.append(last)



oldlist = [1,2,3,4]
newlist = oldlist.copy()
newlist.append(5)
newlist[-1]
print(oldlist[-1], newlist[-1])