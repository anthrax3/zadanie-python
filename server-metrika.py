import asyncio


class DataServer:
    """ данные для хранения метрик"""
    def __init__(self):
        self.data ={}

    def __getitem__(self, item):
        if key in self.data:
            return self.data[key]
        return None

    def __setitem__(self, key, value):
        if key not in self.data:
            self.data[key] = []
            self.data[key].append(value)



class ClientServerProtocol(asyncio.Protocol):
    def __init__(self):
        self.data_server = DataServer()
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        try:
            resp = self.parse_data(data.decode())
            print(resp)
        except UnicodeDecodeError:
            self.transport.write("error\n".encode())
        self.transport.write(resp.encode())

    def parse_data(self,str):
        command = str.split(" ")
        print("command: ",command)
        result = ""
        try:
            if command[0] == "put":
                print("команда put")
            if command[0] == "get":
                if len(command)
                result = self.data_server[command[1]]   # сделать правильный отклик
        except IndexError:
            return "error\nwrong command\n\n"
        return "ok\n\n"+result

def run_server(host,port):
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
    run_server('127.0.0.1',8889)
