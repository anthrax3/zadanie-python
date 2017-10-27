import asyncio
import time


class DataServer:
    """ данные для хранения метрик"""
    def __init__(self):
        self.data = {}

    def __getitem__(self, key):
        result =""
        if key in self.data:
            result = self.data[key]
            value = ""
            for i in sorted(result):
                # print("i = ", i)
                value += "{} {} {}\n".format(key, i[1], i[0])
            result = value
        return result

    def __setitem__(self, key, value):
        if key not in self.data:
            self.data[key] = []
        self.data[key].append(value)

    def get_all2(self):
        result = ""
        for key in self.data:
            value = ""
            for i in sorted(self.data[key]):
                # print("i = ", i)
                value += "{} {} {}\n".format(key, i[1], i[0])
            result += value
        return result

    def get_all(self):
        # result = ""
        # for key in self.data:
        #     value = ""
        #     for i in sorted(self.data[key]):
        #         # print("i = ", i)
        #         value += "{} {} {}\n".format(key, i[1], i[0])
        #     result += value
        return self.data.__str__()


class ClientServerProtocol(asyncio.Protocol):
    """ реализация протокола сервера"""
    def __init__(self):
        self.data_server = DataServer()

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        try:
            resp = self.parse_data(data.decode())
            # print(resp)
        except UnicodeDecodeError:
            self.transport.write("error\n".encode())
        self.transport.write(resp.encode())

    def parse_data(self, str):
        result = ""
        try:
            if str[-1] != "\n":
                raise IndexError
            command = str.split(" ")
            # print("command: ", command)
            if command[0] == "put":
                result = ""
                # print(command[1])
                if len(command) == 3:
                    self.data_server[command[1]] = (int(time.time()), float(command[2]))
                elif len(command) == 4:
                    self.data_server[command[1]] = (int(command[3]), float(command[2]))
                else:
                    raise IndexError
            elif command[0] == "get":
                command[1] = (command[1].splitlines())[0]
                # print(command[1])
                if command[1] == "*":
                    result = self.data_server.get_all()
                else:
                    result = self.data_server[command[1]]
            else:
                raise IndexError
        except IndexError:
            return "error\nwrong command\n\n"
        return "ok\n" + result + "\n"


def run_server(host, port):
    print("server {}:{}".format(host, port))

    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host, port
    )

    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == "__main__":
    run_server('127.0.0.1', 9999)
