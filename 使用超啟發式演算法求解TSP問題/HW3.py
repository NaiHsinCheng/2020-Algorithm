import datetime
import matplotlib.pyplot as plt

file_name = input('請輸入檔案名稱：')
print(file_name)


starttime = datetime.datetime.now()

"""讀檔"""
f = open(file_name, "r")
lines = f.readlines()      #讀取全部內容

city_name = []                #紀錄城市名字
city_code = dict()           #為城市編碼
x = dict()                      #key:城市編碼 value:城市x座標
y = dict()                     #key:城市編碼 value:城市y座標 
code = 97                  #要用來當城市的編碼

for i in range(0, lines.__len__(), 1):        #(開始 結束, 步長)
    j = 0
    for word in lines[i].split():
        if j == 0:
            city_name.append(word)
            city_code[i] = word
        elif j == 1:
            x[i] = int(word)
        else:
            y[i] = int(word)
        j = j + 1
    code = code + 1
    
#城市編碼從0開始


import numpy as np

coordinate = list()
for i in range(len(x)):
    coor = list()
    coor.append(x[i])
    coor.append(y[i])
    coordinate.append(coor)

coordinates = np.array(coordinate)


def getdistmat(coordinates):
    num = coordinates.shape[0]
    distmat = np.zeros((num,num))
    for i in range(num):
        for j in range(i,num):
            distmat[i][j] = distmat[j][i]=np.linalg.norm(coordinates[i]-coordinates[j])
    return distmat

distmat = getdistmat(coordinates)


numcity = coordinates.shape[0] #城市個數
numant = int(0.9*numcity) #螞蟻個數
alpha = 1   #訊息重要程度因子
beta = 5    #啟發函數重要程度因子
rho = 0.1   #訊息揮發速度
Q = 1

iter = 0
itermax = 250

etatable = 1.0/(distmat+np.diag([1e10]*numcity)) #啟發函數矩陣，表示螞蟻從城市i轉移到矩陣j的期望程度
pheromonetable  = np.ones((numcity,numcity)) # 訊息矩陣
pathtable = np.zeros((numant,numcity)).astype(int) #路徑記錄表

distmat = getdistmat(coordinates) #城市的距離矩陣

lengthaver = np.zeros(itermax) #各代路徑的平均長度
lengthbest = np.zeros(itermax) #各代及其之前遇到的最佳路徑長度
pathbest = np.zeros((itermax,numcity)) # 各代及其之前遇到的最佳路徑長度



while iter < itermax:


    # 隨機隨機產生各個螞蟻的起點城市
    if numant <= numcity:#城市數比螞蟻數多
        pathtable[:,0] = np.random.permutation(range(0,numcity))[:numant]
    else: #螞蟻數比城市數多，需要補足
        pathtable[:numcity,0] = np.random.permutation(range(0,numcity))[:]
        pathtable[numcity:,0] = np.random.permutation(range(0,numcity))[:numant-numcity]

    length = np.zeros(numant) #計算各個螞蟻的路徑距離

    for i in range(numant):


        visiting = pathtable[i,0] # 當前所在的城市

        #visited = set() #已訪問過的城市，防止重複
        #visited.add(visiting) #增加元素
        unvisited = set(range(numcity))#未訪問過的城市
        unvisited.remove(visiting) #刪除元素


        for j in range(1,numcity):#循環numcity-1次，訪問剩餘的numcity-1個城市

            #每次用輪盤法選擇下一個要訪問的城市
            listunvisited = list(unvisited)

            probtrans = np.zeros(len(listunvisited))

            for k in range(len(listunvisited)):
                probtrans[k] = np.power(pheromonetable[visiting][listunvisited[k]],alpha)\
                        *np.power(etatable[visiting][listunvisited[k]],alpha)
            cumsumprobtrans = (probtrans/sum(probtrans)).cumsum()

            cumsumprobtrans -= np.random.rand()

            k = listunvisited[np.where(cumsumprobtrans>0)[0][0]] #下一个要访问的城市

            pathtable[i,j] = k

            unvisited.remove(k)
            #visited.add(k)

            length[i] += distmat[visiting][k]

            visiting = k

        length[i] += distmat[visiting][pathtable[i,0]] #螞蟻的路徑距離包括最後一個城市和第一個程式的距離


    #print length
    #包含所有螞蟻的一個迴圈結束後統計本次回圈的若干統計參數

    lengthaver[iter] = length.mean()

    if iter == 0:
        lengthbest[iter] = length.min()
        pathbest[iter] = pathtable[length.argmin()].copy()      
    else:
        if length.min() > lengthbest[iter-1]:
            lengthbest[iter] = lengthbest[iter-1]
            pathbest[iter] = pathbest[iter-1].copy()

        else:
            lengthbest[iter] = length.min()
            pathbest[iter] = pathtable[length.argmin()].copy()    


    # 更新訊息
    changepheromonetable = np.zeros((numcity,numcity))
    for i in range(numant):
        for j in range(numcity-1):
            changepheromonetable[pathtable[i,j]][pathtable[i,j+1]] += Q/distmat[pathtable[i,j]][pathtable[i,j+1]]

        changepheromonetable[pathtable[i,j+1]][pathtable[i,0]] += Q/distmat[pathtable[i,j+1]][pathtable[i,0]]

    pheromonetable = (1-rho)*pheromonetable + changepheromonetable


    iter += 1 #迴圈次數指示器+1

    #觀察程式執行進度，此功能非必須
    if (iter-1)%20==0: 
        print(iter-1)


#做出找到的最優路徑圖
bestpath = pathbest[-1]

plt.plot(coordinates[:,0],coordinates[:,1],'r.',marker=u'$\cdot$')
plt.xlim([-100,2000])
plt.ylim([-100,1500])

for i in range(numcity-1):#
    m,n = bestpath[i],bestpath[i+1]
    #print(m,n)
    plt.plot([coordinates[int(m)][0],coordinates[int(n)][0]],[coordinates[int(m)][1],coordinates[int(n)][1]],'k')
plt.plot([coordinates[int(bestpath[0])][0],coordinates[int(n)][0]],[coordinates[int(bestpath[0])][1],coordinates[int(n)][1]],'b')

plt.show()


"""Best Vist Order: 1 3 2 11 9 10 5 4 6 7 8 
Best Distance: 167.80695975880067
Execution Time: 20(s)"""
