import pickle
import time

# 以两个用户名的tuple为键，以聊天记录条目的tuple的list为值
# 聊天记录tuple数据结构：(sender, time, msg)
All_Chat_History = dict()


def get_history_keys(u1, u2):
    global All_Chat_History
    if (u1, u2) in All_Chat_History.keys():
        return (u1, u2)
    elif (u2, u1) in All_Chat_History.keys():
        return (u2, u1)
    else:
        return None


def append_history(sender, receiver, msg):
    global All_Chat_History
    if receiver == '':
        key = ('','')
    else:
        key = get_history_keys(sender, receiver)
        if key==None:
            key = (sender, receiver)
    if key in All_Chat_History.keys():
        # history already exists
        All_Chat_History[key].append((sender, time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())), msg))
    else:
        # create new history entry
        All_Chat_History[key] = [
            (sender, time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())), msg)]
    # save automatically
    save_to_file()


def get_history(sender, receiver):
    global All_Chat_History
    if receiver == '':
        key = ('','')
    else:
        key = get_history_keys(sender, receiver)
    if key in All_Chat_History.keys():
        return All_Chat_History[key]
    else:
        return []


def purge(u1, u2):
    global All_Chat_History
    key = get_history_keys(u1, u2)
    if key != None:
        del All_Chat_History[key]
        save_to_file()


def purge_all():
    global All_Chat_History
    All_Chat_History = dict()
    save_to_file()


def save_to_file():
    global All_Chat_History
    try:
        pickle.dump(All_Chat_History, open('logs.dat', 'wb'))
        return 0
    except:
        return 1


def load_from_file():
    global All_Chat_History
    try:
        All_Chat_History = pickle.load(open('logs.dat', 'rb'))
        return 0
    except:
        All_Chat_History = dict()
        return 1

