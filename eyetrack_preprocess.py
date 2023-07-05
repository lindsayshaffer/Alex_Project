#python3
#coding:utf-8

import numpy as np
import sklearn as sk
import pandas as pd
import os

# Janky Solutions Prior to Scripting:
# 1. Rename file & convert to csv
# 2. Added row above in eyetrack_saccades as header
# 3. Removed rows 2-3 in saccades csv NOTE: This could be fixed with drop()


#######################################################
#                                                     #
#                 GLOBAL CONSTANTS                    #
#                                                     #
#######################################################


dir_path = os.path.dirname(os.path.realpath("__file__"))

DATA_FILE_NAME = "pilotData" + "/" + "eyetrack_"
DF_NAME_SACC = "saccade.csv"
DF_NAME_BEHAV = "beh.csv"

print("dir_path: ", dir_path) # for debugging

#contrast = np.loadtxt(dir_path + DATA_FILE_NAME)
saccades = pd.read_csv(dir_path + DATA_FILE_NAME + DF_NAME_SACC)
behavior = pd.read_csv(dir_path + DATA_FILE_NAME + DF_NAME_BEHAV)



#######################################################
#                                                     #
#                 DATA PRE-PROCESSING                 #
#                                                     #
#######################################################


# take a look
saccades

# drop rows 2-3
saccades = saccades.drop(saccades.index[1:2])

# Not dropping but omitting rows that have Column A as "nan"
# col C or D = col 2 or 3
# remove whitespace
saccades = saccades.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

# remove last row aka start of "block 6"
saccades = saccades[saccades.blockNum != 6.0]

#remove brackets
saccades = saccades['pos_x'].str.strip('[')
saccades = saccades['pos_y'].str.strip(']')

# convert decimal to int for blockNum
saccades = saccades.astype({"blockNum":"int"})

# re-order trialNum and blockNum to match behavior data
saccades['trialNum'] = saccades['trialNum'] - 1
saccades['blockNum'] = saccades['blockNum'] - 1

# turn None into NaN
saccades = saccades.replace(to_replace = 'None', value = 'NaN')

# take a look
saccades

# drop row based on index value
behavior = behavior.drop(behavior.index[1085])

# convert decimal to int for blockNum
# turn None into NaN
# need to fillna first otherwise astype line will call error
behavior = behavior.fillna(int('-99'))
behavior = behavior.astype({"zoom":"int", "blocks.thisN":"int", "trials.thisTrialN":"int"})

# take a look
behavior