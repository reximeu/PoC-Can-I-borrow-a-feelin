# PoC-Can-I-borrow-a-feelin

## Description

The goal of this project is to materialize an idea:

Draw on a graph the variation of emotions in the flow of a conversation.

Invidivual chat:

![Individual Chat](Graphs_Individual.png "Individual Chat")

Group Chat

![Group Chat](Graphs_Group.png "Group Chat")

## Export Whatsapp Chat History

- Go to WhatsApp
- Go to a Chat
- More options (three dots)
- More
- Export
- Export without multimedia

## Configuration

There are two variables:

- FILE: Chat file location (absolute path)
- FREQS: Frequencies that Pandas uses to resample the data by date-ranges ('Y' == Year, 'W' == Week, ...)

```python
FILE = ""
FREQS = { 
    'M' : (0,0),
    'W' : (0,1),
    'D' : (1,0),
    'H' : (1,1),
}
```

## Usage

```bash
virtualenv .env
source .env/bin/activate
pip install -r requirements
python3 app.py
```
 
### TODO

- Translate text to english to improve results
- Translate VADER Lexicon (idk if it's possible)
- Train a model with tweets
