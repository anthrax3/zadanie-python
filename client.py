import socket
import time

class Client:

    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock = socket.create_connection((self.host, self.port))



    def put(self,metrika,value,timestamp = str(int(time.time()))):
        try:
            message = "put {} {} {}\n".format(metrika,value, timestamp)
            self.sock.sendall(message.encode("utf8"))
        except ClientError:
            pass

    def parse_msg(self, str):
        """ Парсинг строки сообщения типа:  метрика значение timestamp """
        result = str.split(" ")
        if len(result)!=3:
            return "","",""
        return result[0], (float) (result[1]), (int) (result[2])

    def create_data(self, argv):
        """ создание структуры анных ответа с сервера"""
        result = dict()
        for arg in argv:
            # print("args = ",arg)
            if arg == "":
                continue
            m, v, t = self.parse_msg(arg)
            if not(m in result):
                result[m] = list()
            result[m].append((t, v))
        return result


    def get(self,metrika):
        get_result = None
        message = "get {}\n".format(metrika)
        self.sock.send(message.encode("utf8"))
        result = (self.sock.recv(1024)).decode("utf8")     # получить данные с сервера
        result = result.split("\n")
        # print(result)
        if "ok" == result[0]:
            get_result = self.create_data(result[1:])
            # print(get_result)
        elif "error" == result[0]:
            raise ClientError(result[1])
        return get_result


class ClientError(Exception):
    pass