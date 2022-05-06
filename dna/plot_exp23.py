import matplotlib.pyplot as plt

s = ''
with open('data.txt', 'r') as f:
    s = f.read()
s = s.split('\n')
tme, length, tmeH, lengthH = s[0], s[1], s[2], s[3]
tme = tme.split(' ')
tme = [1000*float(i) for i in tme]

length = length.split(' ')
length = [float(i) for i in length]

tmeH = tmeH.split(' ')
tmeH = [1000*float(i) for i in tmeH]

lengthH = lengthH.split(' ')
lengthH = [float(i) for i in lengthH]

xAxisH = [i for i in range(5, 20)]
xAxis = [i for i in range(5, 20)]


plt.plot(xAxis, tme, 'ro-', label='GBSC')
plt.plot(xAxisH, tmeH, 'b+-', label='Huffman')
plt.plot(xAxis, tme, 'ro-', xAxisH, tmeH, 'b+-')
# plt.title('The average time cost for different numbers of exons')
plt.xlabel("n")
plt.ylabel('Running time(ms)')
plt.legend(loc='best')
plt.savefig('./BHTime.pdf')
plt.show()

plt.plot(xAxis, length, 'ro-', label='GBSC')
plt.plot(xAxisH, lengthH, 'b+-', label='Huffman')
plt.plot(xAxis, length, 'ro-', xAxisH, lengthH, 'b+-')
# plt.title('The expected number of detections for different numbers of exons')
plt.xlabel("n")
plt.ylabel('Expected number of detection')
plt.legend(loc='best')
plt.savefig('./BHLength.pdf')
plt.show()
