import numpy as np
import collections
import math
# import sys
from operator import itemgetter

class MainTheme:
    # 全局变量，记录音符矩阵每个音轨块的音符数量
    NoteNumList=list()
    f_p_column_list=[[]]
    # 参数为上一步提取到的音轨的二维list
    def __init__( self,_column_list=[[]]):
        for i in range(len( _column_list)):
            if len(_column_list[i])!=0:
                self.f_p_column_list.append(_column_list[i])
        self.f_p_column_list.remove(self.f_p_column_list[0])
    #  删除复调关系的音符，Skyline算法第一步
    # 删除复调音
    def method_DeleteRepitch(self):
        if not (self.f_p_column_list):  # 如果音符矩阵为空就直接返回该空矩阵
            return self.f_p_column_list
        i = 0  # 遍历音符矩阵的所有音符
        while i < len(self.f_p_column_list):
            j = 0
            while (len(self.f_p_column_list[i])!=0)and(j < len(self.f_p_column_list[i]) - 1):
                k = j + 1
                while k < (len(self.f_p_column_list[i])):
                    if self.f_p_column_list[i][j].start_time < self.f_p_column_list[i][k].start_time and (
                            self.f_p_column_list[i][j].start_time + self.f_p_column_list[i][j].duration) > (
                            self.f_p_column_list[i][k].start_time + self.f_p_column_list[i][k].duration):
                        if self.f_p_column_list[i][j].pitch < self.f_p_column_list[i][k].pitch:
                            del self.f_p_column_list[i][j]
                            print(2)
                        if self.f_p_column_list[i][j].pitch > self.f_p_column_list[i][k].pitch:
                            del self.f_p_column_list[i][k]
                            print(2)
                    k += 1
                j += 1
            i += 1
        return self.f_p_column_list      # 返回删除复调关系的矩阵


    # 将音符数组排序，Skyline算法的第二步
    def method_SortNote(self):
        if not (self.f_p_column_list):  # 如果音符矩阵为空就直接返回该空矩阵
            return self.f_p_column_list
        for i in range(len(self.f_p_column_list)):
            self.f_p_column_list[i].sort(key=lambda notes:notes.start_time)
        return self.f_p_column_list


    # 保留同时演奏里音调高的音符,Skyline算法的第三步
    def method_ReserveHighPitch(self):
        if not (self.f_p_column_list):  # 如果音符矩阵为空就直接返回该空矩阵
            return self.f_p_column_list
        i = 0                      # 遍历无复调关系的音符矩阵的所有音符
        while i < len(self.f_p_column_list):
            j = 0
            while j < len(self.f_p_column_list[i])-1:
                if self.f_p_column_list[i][j].pitch < self.f_p_column_list[i][j + 1].pitch and (
                        self.f_p_column_list[i][j].start_time + self.f_p_column_list[i][j].duration) < (
                        self.f_p_column_list[i][j + 1].start_time):
                    self.f_p_column_list[i][j].duration = self.f_p_column_list[i][j + 1].start_time - self.f_p_column_list[i][j].start_time
                j += 1
            self.NoteNumList.append(j)
            i += 1
        return self.f_p_column_list

    # Skyline算法，依次调用第一，二，三步实现Skyline算法，参数为传入的二维list，返回二维list
    def method_Skyline(self):
        self.method_DeleteRepitch()
        self.method_SortNote()
        return  self.method_ReserveHighPitch()

    # 获得音符矩阵的音高分布向量（规模为 len×12 ）
    def method_Get_PitchVector(self):
        h=len(self.f_p_column_list)
        PitchVector = np.zeros((h,12))
        for i in range(h):              #依次遍历整个音符矩阵 统计各个音轨块内各音质的出现次数之和
            for j in range(len(self.f_p_column_list[i])):
                PitchVector[i][self.f_p_column_list[i][j].pitch % 12]+=1
        return PitchVector

    # 获得整个音符矩阵的平均音高分布向量，参数为音高分布向量
    def method_Get_PitchVector_avg(self,PitchVector=[[]]):
        T=len(PitchVector)
        PitchVector_sum=0
        PitchVector_avg = np.zeros(12)
        for j in range(12):
            for i in range(T):
                PitchVector_sum += PitchVector[i][j]    #计算每个音轨块音质名为j的音符出现的次数的总和
            PitchVector_avg[j] = PitchVector_sum/12
        return PitchVector_avg

    # 获得音符矩阵的加权平均音高分布向量，参数为音高分布向量
    def method_Get_PitchVector_weight(self,PitchVector=[[]]):
        T=len(PitchVector)
        note_sum=sum(self.NoteNumList)       # 整个音符矩阵的音符数量
        PitchVector_sum=0
        PitchVector_weight = np.zeros(12)
        for j in range(12):
            for i in range(T):
                PitchVector_sum += PitchVector[i][j]*(self.NoteNumList[i]/note_sum)    #计算每个音轨块音质名为j的音符出现的次数的总和
            PitchVector_weight[j] = PitchVector_sum
        return PitchVector_weight

    #  求两个向量的欧式距离
    def method_distEclud(self,vecA, vecB):
       return np.sqrt(sum(np.power(vecA - vecB, 2)))

    # 凝聚层次聚类,返回存放类簇的序号的字典 字典的键从音高分布向量的长度依次加一即len（PitchVector）
    def method_hierarchy_cluster(self,PitchVector=[[]]):
        # 终止算法的距离阈值
        t=self.method_distEclud(self.method_Get_PitchVector_avg(PitchVector),self.method_Get_PitchVector_weight(PitchVector))/2
        cluster_dict=collections.OrderedDict()     # 用于存放合并的簇
        k=len(PitchVector)                        # 字典的键
        cluster_dict[k]=[0]
        i = 0
        sentinel=True                             # 设置哨兵，检测新的簇是否已经在存放类簇的字典里
        while i<len(PitchVector)-1:
            j = i + 1
            while j<len(PitchVector):
                if self.method_distEclud(PitchVector[i],PitchVector[j])<t:
                    for m in cluster_dict:
                        if (i in cluster_dict[m]) and (not (j in cluster_dict[m]) ):
                            cluster_dict[m].append(j)
                            sentinel=False
                            break
                        if (i not in cluster_dict[m]) and ( (j in cluster_dict[m]) ):
                            cluster_dict[m].append(i)
                            sentinel=False
                            break
                        if (i  in cluster_dict[m]) and ( (j in cluster_dict[m]) ):
                            sentinel=False
                            break
                    if sentinel:                # 新的类簇没有在字典里，则新建一个键值对
                        k+=1
                        cluster_dict[k]=[i,j]
                j+=1
            i+=1
        return cluster_dict

    # 选出代表音轨
    def method_RepresentTrace(self):
        # 先执行Skyline算法去掉复调音乐
        self.f_p_column_list = self.method_Skyline()
        # 得到音高分布向量
        pitchvector = self.method_Get_PitchVector()
        # 对音轨块进行类聚
        cluster_dict = self.method_hierarchy_cluster(pitchvector)
        pitch_avg=list()
        Xi=list()
        RepresentList=list()
        MaxOrder=list()             # 记录代表音轨号
        t=0                 # 记录最大音轨号
        temp=0
        i = 0                               # 遍历音符矩阵的所有音符
        while i < len(self.f_p_column_list):
            j = 0
            while j < len(self.f_p_column_list[i]):
                temp+= self.f_p_column_list[i][j].pitch
                j += 1
            pitch_avg.append(float(temp/self.NoteNumList[i]))                # 求得各音轨块的平均音高
            k = 0
            hc=0
            while k < 12:
                if self.NoteNumList[i] != 0 and pitchvector[i][k] != 0:
                    hc += (pitchvector[i][k]/self.NoteNumList[i])*math.log(float(pitchvector[i][k]/self.NoteNumList[i]),12)
                k += 1
            Xi.append(pitch_avg[i]-128*hc)
            i += 1
        for m in cluster_dict:
            if len(cluster_dict[m])>1:
                for n in range(len(cluster_dict[m])-1):
                    mn = n+1
                    while mn < len(cluster_dict[m]):
                        if Xi[cluster_dict[m][n]]>Xi[cluster_dict[m][mn]]:
                            t=cluster_dict[m][n]
                        else:
                            t=cluster_dict[m][mn]
                        mn += 1
                MaxOrder.append(t)
            else:
                MaxOrder.append(cluster_dict[m][0])
        for a in range(len(MaxOrder)):
            RepresentList.append(self.f_p_column_list[MaxOrder[a]])
        return RepresentList

    def method_getMainMelody(self):
        # 先选出代表音轨
        self.f_p_column_list=self.method_RepresentTrace()
        # 再进行skyline算法得到目标音轨，即为主旋律
        return self.method_Skyline()

