lis = []
lis2 = []
for l in open("t.txt"):
	lis = l.split('-')
t = lis[0][0]
for i in range(1,len(lis)):
	if lis[i][:len(lis[i])//2] != lis[i][len(lis[i])//2:len(lis)]:
		lis2.append(str(int(t)/1000) + "-" + str(int(lis[i][:len(lis[i])//2])/1000))
		t = lis[i][len(lis[i])//2:len(lis)]
print(lis2)