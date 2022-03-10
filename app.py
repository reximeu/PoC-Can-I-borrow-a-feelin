import re
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sentiment_analysis_spanish import sentiment_analysis


FILE = "/path/to/file.txt"
FREQS = [ 'Y', 'M', 'W', 'D', 'H', ]
ANONYMIZE = True

data = []
parsed = []
analyzer = sentiment_analysis.SentimentAnalysisSpanish()

date_regex = r"(\d{1,2}\/\d{1,2}\/\d{1,2})"
time_regex = r"(\d{1,2}:\d{1,2})"
user_regex = r"(.*?)"
text_regex = r"(.*)"
full_regex = date_regex + " " + time_regex + " - " + user_regex + ": " + text_regex

# READ FILE LINES
with open(FILE, 'r') as f:
    text = f.readlines()

# PARSE FORMAT
for line in text:
    index = re.search(full_regex, line)
    if index != None:
        parsed.append(line)
    else:
        try:
            parsed[-1] = parsed[-1] + " " + line
        except:
            pass

# APPEND TO LIST
for line in parsed:
    index = re.search(full_regex, line)
    date = index.groups()[0].split('/')
    time = index.groups()[1].split(':')
    name = index.groups()[2]
    text = index.groups()[3]

    score = analyzer.sentiment(line)
    
    date_time = datetime.datetime(
        day = int(date[0]), 
        month = int(date[1]), 
        year = int(date[2]) + 2000, 
        hour = int(time[0]), 
        minute = int(time[1])
    )
    data.append([date_time, name, score])

# CONVERT TO DATAFRAME
data = pd.DataFrame(data)
data.columns =[ 'dates', 'names', 'scores' ]
data.dates = pd.to_datetime(data.dates, unit='s')

# CREATE THE FIGURE
fig, ax = plt.subplots(nrows=len(FREQS), ncols=1)

# FOR NAME IN A CHAT
names = np.unique(data.names)
for name in names:
    color = np.random.rand(3,)
    subset = data[data.names == name]

    # FOR ALL TYPES OF FREQUENCIES SETTED AT THE TOP
    for index, freq in enumerate(FREQS):
        resample = subset.resample(freq, on='dates').sum()
        x = resample.index
        y = resample['scores']
        
        # PRINT SENTIMENT
        label = f'{freq}' if ANONYMIZE else f'{name} {freq}'
        ax[index].plot(x, y, label = label, color=color)
        
fig.legend(loc=7)
fig.tight_layout()
fig.subplots_adjust(right=0.75)  

# DISPLAY THE GRAPH
plt.show()