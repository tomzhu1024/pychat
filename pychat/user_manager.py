import pickle

import face_recognition
import numpy

All_Users = dict()
# face recognition variables
known_names = []
known_faces = []


def register(usr, pwd, face):
    global All_Users
    if usr not in All_Users.keys():
        All_Users[usr] = [pwd, face]
        if face != []:
            known_names.append(usr)
            known_faces.append(face)
        # save automatically
        save_to_file()
        # register successfully
        return 0
    else:
        # user already exists
        return 1


def validate(usr, pwd):
    global All_Users
    if usr in All_Users.keys():
        # user exists
        if All_Users[usr][0] == pwd:
            # validation passed
            return 0
        else:
            # invalid password
            return 1
    else:
        # user not exists
        return 2


def change_pwd(usr, old, new):
    global All_Users
    vld = validate(usr, old)
    if vld == 0:
        # validation passed
        All_Users[usr][0] = new
        # save automatically
        save_to_file()
        return 0
    else:
        # 1 - invalid password
        # 2 - user not exists
        return vld


def purge(usr):
    global All_Users
    if usr in All_Users.keys():
        # user exists
        del All_Users[usr]
        save_to_file()
        return 0
    else:
        # user not exists
        return 1


def purge_all():
    global All_Users
    All_Users = dict()
    save_to_file()


def save_to_file():
    global All_Users
    try:
        pickle.dump(All_Users, open('users.dat', 'wb'))
        return 0
    except:
        return 1


def get_name_from_face(face_encoding_list):
    global known_names, known_faces
    face_encoding = numpy.array(face_encoding_list)
    matches = face_recognition.compare_faces(known_faces, face_encoding,tolerance=0.4)

    # If a match was found in known_face_encodings, just use the first one.
    if True in matches:
        first_match_index = matches.index(True)
        return known_names[first_match_index]
    return ''


def load_from_file():
    global All_Users
    try:
        All_Users = pickle.load(open('users.dat', 'rb'))
        for i in All_Users.items():
            if i[1][1] != []:
                known_names.append(i[0])
                known_faces.append(numpy.array(i[1][1]))
        return 0
    except:
        All_Users = dict()
        return 1
