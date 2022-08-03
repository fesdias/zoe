from datetime import datetime, timedelta
from CaptionsSplitterSrt import Caption
import re

#Converte o tempo inicial e final para o formato do str
def Duration(initialTime, finalTime):
    timeI = str(timedelta(seconds = initialTime))
    timeI = "0" + timeI
    timeI = timeI.replace(',','.')

    if len(timeI) > 9:
        timeI = timeI[:-3]

    timeF = str(timedelta(seconds = finalTime))
    timeF = "0" + timeF
    timeF = timeF.replace(',','.')

    if len(timeF) != 9:
        timeF = timeF[:-3]

    return str(timeI + " --> " + timeF)

def CaptionsGenerator(caption, fileTitle):

    with open(fileTitle, 'w') as file:

        for i in range(len(caption)):
            file.write(str(i+1)+"\n")
            file.write(Duration(caption[i].start_time, caption[i].end_time)+"\n")
            file.write(caption[i].content+"\n")
            file.write("\n")

    file.close()
    return file