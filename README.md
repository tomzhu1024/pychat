# PyChat

A online chat system written in Python 3.

NYU Shanghai ICS final project.

## Project Structure

- **demo** - a simple demo which implements basic UI, event-driven design and multi-threading server

- **pychat** - complete version

- **ui_design** - UI design files

## Introduction Video

- [Bilibili](https://www.bilibili.com/video/av38136634)
- [YouTube](https://www.youtube.com/watch?v=Dutin1C_JGA)

## Features

- Highly-robust logic design
- Friendly GUI
- Reliable AES-encrypted socket
- File transfer
- Facial recognition

## Required Library

To run this program, some libraries are required. Use command `pip3` to install them.

```bash
pip3 install cmake face_recognition numpy
pip3 install opencv-python
pip3 install pycryptodome
```

## Start Server

Use the following command to start the server. Also, optional parameter `-p` can be used to purge the server data before the server start up.

```bash
python server.py [-p user|chat|all]
```

## Start Client

Use the following command to start the client.

```bash
python client.py
```

You can change the filename to be `client.pyw` to get rid of the CLI interface.

## Problems Pending to be Fixed

1. Clients from **other machines** cannot send files to clients from **localhost**.