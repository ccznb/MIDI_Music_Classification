

import struct
import os
from music21 import *


class Note:
    def __init__(self, pitch, velocity, duration, start_time):
        self.pitch = pitch
        self.velocity = velocity
        self.duration = duration
        self.start_time = start_time


def get_node_unit_array(filepath):
    class MidiEventNote:
        def __init__(self, tick, me):
            self.tick = tick
            self.me = me

        def __lt__(self, other):
            return self.tick < other.tick

    '''def readint(k):  # 读k个字节并转换为整数
        r = 0
        for i in range(k):
            r = r*256+ord(bf.read(1))
        return r
    bf = open(filepath, 'rb')  # 打开二进制文件
    size = os.path.getsize(filepath)  # 获得文件大小
    head = bf.read(4)  # 文件头部MThd
    if head != b'MThd':
        raise Exception("Unexcepted file head!")
    restSize = readint(4)
    if restSize != 6:
        raise Exception("Unexcepted ressize!")
    trackType = readint(2)
    bf.close()
    '''
    mf = midi.MidiFile()
    mf.open(filepath)
    mf.read()
    if mf.format == 2:
        return [],[]
    if mf.ticksPerSecond:
        t = mf.ticksPerSecond
    else:
        t = -1

    midiEventNotes = []
    for mt in mf.tracks:  # 读取NoteOn，NoteOff和Set tempo
        tick = 0
        for me in mt.events:
            #print(me)
            if me.isDeltaTime():
                tick += me.time
            elif me.isNoteOn():
                midiEventNotes.append(MidiEventNote(tick, me))
            elif me.isNoteOff():
                midiEventNotes.append(MidiEventNote(tick, me))
            else:
                str = me.getBytes()
                if str[0] == 255 and str[1] == 81:
                    midiEventNotes.append(MidiEventNote(tick, me))

    notes = []  # 一维数组
    notes2 = []  # 二维数组
    for i in range(len(mf.tracks)):
        notes2.append([])
    noteOns = []
    lastTick = 0
    time = 0
    midiEventNotes = sorted(midiEventNotes)
    for midiEventNote in midiEventNotes:
        #print(midiEventNote.tick,midiEventNote.me)
        deltatime = (midiEventNote.tick-lastTick)/t
        time += deltatime
        lastTick = midiEventNote.tick
        if midiEventNote.me.isNoteOn():
            noteOns.append(MidiEventNote(time, midiEventNote.me))
        elif midiEventNote.me.isNoteOff():
            flag = True
            for noteOn in noteOns:
                if (noteOn.me.matchedNoteOff(midiEventNote.me)):
                    tempNote = Note(
                        noteOn.me.pitch, noteOn.me.velocity, time-noteOn.tick, noteOn.tick)
                    notes.append(tempNote)
                    #print(tempNote.duration)
                    notes2[midiEventNote.me.track.index].append(tempNote)
                    noteOns.remove(noteOn)
                    flag = False
                    break
            if flag:
                raise Exception("NoteOn miss!")
        else:
            tempo = 0
            for i in midiEventNote.me.data:
                tempo = tempo*256+i
            t = mf.ticksPerQuarterNote/tempo*1e6
    if len(noteOns) != 0:
        raise Exception("NoteOff miss!")
    mf.close()
    return notes, notes2


#b = get_node_unit_array('千本樱_爱给网_aigei_com.mid')
#print("Finished!")
