import json
import struct

from Crypto import Random
from Crypto.Cipher import AES

# Global Key for encryption and decryption
key = b'WZ4T8bbw6XWGbjuV'


class ProtocolException(Exception):
    pass


class DisconnectException(Exception):
    pass


class L1Exception(Exception):
    pass


class L1HeadException(Exception):
    pass


def encrypt(data):
    iv = Random.new().read(AES.block_size)
    mycipher = AES.new(key, AES.MODE_CFB, iv)
    ciphertext = iv + mycipher.encrypt(data)
    return ciphertext


def decrypt(ciphertext):
    mydecrypt = AES.new(key, AES.MODE_CFB, ciphertext[:16])
    decrypttext = mydecrypt.decrypt(ciphertext[16:])
    return decrypttext


def layer1_pack(payload):
    if len(payload) >= 256 ** 2:
        # avoid too large stuff
        raise ("Payload too large")
    return struct.pack('>H', len(payload)) + payload


def layer1_pack_x(payload):
    if len(payload) >= 256 ** 8:
        # avoid too large stuff
        raise ("Payload too large")
    return struct.pack('>Q', len(payload)) + payload


def layer1_parse_length(packet):
    # split the length of payload from packet
    return struct.unpack('>H', packet[0:2])[0]


def send(socket, data_dict):
    layer3_packed = json.dumps(data_dict).encode('utf-8')
    layer2_packed = encrypt(layer3_packed)
    socket.send(layer1_pack(layer2_packed))


def recv(socket):
    # 配置单个消息最大长度
    max_split_size = 1024
    layer1_unpacked = b''
    # 只接收2字节的长度信息
    bytes_recv = socket.recv(2)
    if len(bytes_recv) == 0:
        # 客户端已断开，产生异常以便外部调用者捕捉
        raise DisconnectException
    elif len(bytes_recv) == 1:
        # 客户端不兼容协议，产生异常以便外部调用者捕捉
        raise L1HeadException
    # 计算总共需要接受的字节
    bytes_remained = struct.unpack('>H', bytes_recv)[0]
    # 设置套接字超时，防止不支持协议的对方套接字长期不发包而导致进程阻塞
    # 只有对方不支持协议，才会引发异常，因此不捕捉任何异常，意在通知外部调用者
    socket.settimeout(5)
    while bytes_remained != 0:
        if bytes_remained>max_split_size:
            bytes_recv = socket.recv(max_split_size)
        else:
            bytes_recv = socket.recv(bytes_remained)
        if bytes_recv == b'':
            raise DisconnectException
        layer1_unpacked+=bytes_recv
        bytes_remained-=len(bytes_recv)
        if bytes_remained==0:
            break
    # 恢复默认套接字超时，防止对其他操作造成影响
    socket.settimeout(None)
    layer2_unpacked = decrypt(layer1_unpacked)
    # json.loads() supports both string and bytes as parameter, no need to decode here
    layer3_unpacked = json.loads(layer2_unpacked)
    return layer3_unpacked
