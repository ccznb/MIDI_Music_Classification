from  GetPassageFeature import *
from MIDI_Passage import *
from MainThemes import MainTheme

def getfeature(filepath):
    f_p_column_list1,f_p_column_list2 = get_node_unit_array(filepath)
    mainTheme=MainTheme(f_p_column_list2)       # 创建主旋律类对象
    mainThemeMat=mainTheme.method_getMainMelody()       # 获得主旋律矩阵
    passage = Passage() #乐段类
    passage.f_p_column_list1 = f_p_column_list1
    passage.f_p_column_list2 = f_p_column_list2
    passage.segmentDivision()
    SegmentList=passage.ReturnNewSegList()
    getPassageFeature=GetPassageFeature()
    # passageList为最终的乐段特征列表，二维列表
    passageList=getPassageFeature.MeathonGetPassageFeature(SegmentList,mainThemeMat)
    return passageList



