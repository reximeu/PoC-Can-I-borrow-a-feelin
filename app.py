import re
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from nltk.sentiment import SentimentIntensityAnalyzer


FILE = ""
FREQS = { 
    'W' : (0,0),
    'M' : (0,1),
    'D' : (1,0),
    'H' : (1,1),
}

data = []
parsed = []
analyzer = SentimentIntensityAnalyzer()

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

    scores = analyzer.polarity_scores(line)
    neg = scores.get('neg')
    neu = scores.get('neu')
    pos = scores.get('pos')
    com = scores.get('compound')
    
    date_time = datetime.datetime(
        day = int(date[0]), 
        month = int(date[1]), 
        year = int(date[2]) + 2000, 
        hour = int(time[0]), 
        minute = int(time[1]))
    data.append([date_time, name, pos, neu, neg, com])

# CONVERT TO DATAFRAME
data = pd.DataFrame(data)
data.columns =[ 'dates', 'names', 'pos', 'neu', 'neg', 'com' ]
data.dates = pd.to_datetime(data.dates, unit='s')

# CREATE THE FIGURE
fig, ax = plt.subplots(2, 2)

# FOR NAME IN A CHAT
names = np.unique(data.names)
for name in names:
    color = np.random.rand(3,)
    subset = data[data.names == name]

    # FOR ALL TYPES OF FREQUENCIES SETTED AT THE TOP
    for freq, freq_ax in FREQS.items():
        resample = subset.resample(freq, on='dates').sum()
        i1 = freq_ax[0]
        i2 = freq_ax[1]

        x = resample.index
        y = resample['pos']
        # PRINT POSITIVITY
        ax[i1, i2].plot(x, y, label = f'{name} {freq}', color=color)

# DISPLAY THE GRAPH
plt.legend(loc=(1.04,0))
plt.show()