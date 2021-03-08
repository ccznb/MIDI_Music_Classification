import numpy
import torch
from nltk import flatten

from getNoteMat import *

'''
class Note(object): #音符类
    def __init__(self,pitch,velocity,duration,start_time):
        self.pitch=pitch #音高
        self.velocity=velocity #音量
        self.duration=duration #持续时间
        self.start_time=start_time #开始时间
'''

class Bar(object): # 小结
    def __init__(self):
        self.note_list=[] #音符list
        self.melody_area=0 #旋律面积
        self.sound_area=0 #音量面积

    def melodyArea(self): #计算旋律面积
        if self.melody_area > 0:
            return self.melody_area
        for note in self.note_list:
            self.melody_area += note.pitch * note.duration
        return self.melody_area

    def soundArea(self): #计算音量面积
        if self.sound_area > 0:
            return self.sound_area
        for note in self.note_list:
            self.sound_area += note.velocity * note.duration
        return self.sound_area


class Passage(object): #乐段划分
    def __init__(self):
        self.f_p_column_list1 = []  #一维音符list
        self.f_p_column_list2 = []  #二维list
        self.note_list = [] #音符list
        self.bar_list=[] #小节的list
        self.segment_list=[] #乐段的list
        self.minl=2 #一个乐段最小小节数
        self.maxl=4 #一个乐段最大小节数
        self.bar_duration=4 #一个小节的时间
        self.m=0 #小节数
        self.t=0 #乐段相似度阈值

    def same(self,a,b):
        x = a.melodyArea() - b.melodyArea()
        y = a.soundArea() - b.soundArea()
        distance = x*x+y*y
        if distance <= self.t:
            return True
        else:
            return False

    def barDivision(self):
        self.t=36*self.bar_duration
        tot_time = self.f_p_column_list1[-1].start_time + self.f_p_column_list1[-1].duration
        self.m = tot_time // self.bar_duration
        if tot_time % self.bar_duration !=0:
            self.m+=1
        for note in self.f_p_column_list1:
            pre= note.start_time // self.bar_duration
            post = (note.start_time + note.duration) // self.bar_duration
            if post > pre:
                temp = Note(note.pitch, note.velocity, (pre+1)*self.bar_duration-note.start_time, note.start_time)
                self.note_list.append(temp)
                temp2 = Note(note.pitch, note.velocity, note.duration + note.start_time-post*self.bar_duration, (pre+1)*self.bar_duration)
                self.note_list.append(temp2)
            else:
                self.note_list.append(note)

        temp = -1
        bar_temp = Bar()
        for note in self.note_list:
            st = note.start_time // self.bar_duration
            if st != temp:
                temp = st
                self.bar_list.append(bar_temp)
                bar_temp = Bar()
            bar_temp.note_list.append(note)
        self.bar_list.append(bar_temp)
        del self.bar_list[0]




    def segmentDivision(self):
        self.barDivision()
        segment=[]
        i=0
        k=0
        while i < self.m:
            if k < self.minl:
                segment.append(self.bar_list[i])
                k += 1
            elif k > self.maxl:
                k=1
                segment.append(self.bar_list[i])
                self.segment_list.append(segment)
                segment=[]
            else:
                if self.same(self.bar_list[i-1],self.bar_list[i]):
                    segment.append(self.bar_list[i])
                    k += 1
                else:
                    k = 1
                    segment.append(self.bar_list[i])
                    self.segment_list.append(segment)
                    segment = []
            i+=1
    def ReturnNewSegList(self):
        NewSegmentList=list()
        for bl in self.segment_list:
            for b in bl:
                NewSegmentList.append(b)

        return NewSegmentList





