# 从各个乐段中提取乐段的特征
class GetPassageFeature():
    # 用于提取乐段的特征
    # bar 是上一步划分的乐段 包括一个list数组
    def __init__(self):
        self.dt=0.2
    def getPartPassageFeature(self,passage,mainTheme):
        maxVolume = passage.note_list[0].velocity
        PlayingNode = list()  # 存放正在演奏的音符
        ListLen = len(passage.note_list)
        for i in range(len(passage.note_list)):
            if maxVolume < passage.note_list[i].velocity:
                maxVolume = passage.note_list[i].velocity
        j = 0
        EncodeArr = [0] * 128
        while self.dt * j <= passage.note_list[ListLen - 1].start_time + passage.note_list[ListLen - 1].duration:
            p = 0
            while p < ListLen:
                if passage.note_list[p].start_time <= self.dt * j and self.dt * j< passage.note_list[p].start_time + passage.note_list[p].duration:
                    PlayingNode.append(passage.note_list[p])
                p += 1
            for i in PlayingNode:
                if i in mainTheme:
                    EncodeArr[i.pitch] += i.velocity / maxVolume;
                else:
                    EncodeArr[i.pitch] += 0.6 * (i.velocity / maxVolume);
            j += 1
        return EncodeArr;
    def MeathonGetPassageFeature(self,segmentList,mainTheme):
        PassageList=[]
        for i in range(len(segmentList)):
            PassageList.append(self.getPartPassageFeature(segmentList[i],mainTheme))
        return PassageList














