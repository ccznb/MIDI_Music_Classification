from nltk import flatten

import getNoteMat
from MainThemes import MainTheme

notemat,notemat_two=getNoteMat.get_node_unit_array("aigei_com.mid")
class Notes:
    def __init__(self, pitch, velocity, duration, start_time):
        self.pitch = pitch
        self.velocity = velocity
        self.duration = duration
        self.start_time = start_time
# notes=Notes(52,15,19,16)
#  noteMat=[[] for k in range(10)]
# for i in range(10):
# #     for j in range(10):
# #        noteMat[i].append(notes);
# mainTheme=MainTheme(notemat_two)
# mainThemeMat=mainTheme.method_getMainMelody()
# notes=[[]]
# notes=[[4,5],[7,5],[1,6,3],[2]]
# notes=flatten(notes)
# print(notes)
# notes.append(notess[0])
# notes.append(notess[1])
# notes.remove(notes[0])
# print(notess)
# print(len(notess))
