#!/usr/bin/env python

import tkinter as tk
import random
from datetime import datetime

possible_characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

# 3884 possible 2 character combinations
# (26 + 26 + 10) * (26 + 26 + 10)
datastore = []
short_to_long = {}
long_to_short = {}

def retire_oldest(long):
    oldest_date = datetime.now()
    index = 0
    short = ""
    for i in range(len(datastore) + 1):
        if datastore[i]['time'] < oldest_date:
            index = i
            short = datastore[i]['short'][-2:]
            oldest_date = datastore[i]['time']

    # delete old one
    datastore.pop(index)

    # add in new one and update dicts
    long_to_short[long] = short
    short_to_long[short] = long
    datastore.append({"short": "applau.se/" + short,
                      "long": long,
                      "time": datetime.now(),
                      "call_count": 1})
    return short

def increase_call_count(long_link):
    for l in datastore:
        if l["long"] == long_link:
            # update call count and time
            l["call_count"] += 1
            l["time"] = datetime.now()

def get_unique_id(long_link):

    # if we have generated a shortened link for this link.. return that
    if long_link in long_to_short:
        increase_call_count(long_link)
        return long_to_short[long_link]
    else:
        id = random.sample(possible_characters, 2)
        clean_id = "".join(id)

        # if all unique have been used up...
        if len(datastore) == 3884:
            return retire_oldest(long_link)
        # if the id is already used.. regenerate
        if clean_id in short_to_long:
            return get_unique_id()
        else:
            short_to_long[clean_id] = long_link
            long_to_short[long_link] = clean_id
            datastore.append({"short":"applau.se/"+clean_id,
                              "long": long_link,
                              "time": datetime.now(),
                              "call_count": 1})
            return clean_id


def process_link(link):

    # retrieve original link
    if link[0:9] == "applau.se":

        long = short_to_long.get(link[10:], None)
        if long is not None:
            increase_call_count(long)
            return long
        else:
            return "link does not exist"


    # shorten link
    else:
        output = get_unique_id(link)
        return "applau.se/" + output

# ASSUME THE INPUT IS A PROPERLY FORMATTED URL
def submit():
    link = entry.get()
    output = process_link(link)

    entry.delete(0,len(entry.get()))
    link_output.set(output)
    #print(sorted(datastore, key = lambda i: i['call_count'], reverse=True))

def show():
    output = ""
    for l in sorted(datastore, key = lambda i: i['call_count'], reverse=True):
        output += "call_count: " + str(l['call_count']) + ", " + l['long'] + " --> " + l['short'] + " " \
                  + l['time'].strftime("%m/%d/%Y, %H:%M:%S") + '\n'

    print(output)
    data_box.insert(tk.END, output)



# initialize gui
window = tk.Tk()

link_output = tk.StringVar()

window.title("applau.se")

# set window size
window.geometry("600x400")

greeting = tk.Label(text="Welcome to applau.se, a link shortening program" + "\n"
                    + "enter your link or an applau.se link below")
greeting.pack()

entry = tk.Entry(window)
entry.pack()

sub_btn=tk.Button(window,text = 'Submit', command = submit)
sub_btn.pack()

out = tk.Entry(textvariable=link_output, state = "readonly")
out.pack()

sub_btn=tk.Button(window,text = 'show the data', command = show)
sub_btn.pack()

data_box = tk.Text(window, width = 100, height = 20)
data_box.pack()

# run the GUI
window.mainloop()