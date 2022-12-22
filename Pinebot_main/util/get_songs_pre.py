# RUN UNDER WINDOWS!!!!!!!!!!!!!

import os
import time

IIDX_HDD_SOUND_PATH = """C:\iidx 29\data\sound\\"""

for f in os.listdir(IIDX_HDD_SOUND_PATH):
    if ".ifs" in f:
        number = f.replace(".ifs", "")
        os.system("ifstools.exe \""+ IIDX_HDD_SOUND_PATH + f + "\" -y -e")
        path = os.path.join(os.getcwd(), number+"_ifs", number, number + "_pre.2dx")
        print(path)
        time.sleep(2)
        os.system("BemaniToBMS.exe" + path)
        break
    
    
    