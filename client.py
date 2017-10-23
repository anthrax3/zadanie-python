import asyncio

class Client:

    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout

    async def put_message(self,message,loop):
        try:
            reader, writer = await asyncio.open_connection(self.host, self.port,loop = loop)
            # message = "put {} {} {}\n".format(metric,value,timestamp)
            print("send:  {}".format(message))
            writer.write(message.encode())
            writer.close()
        except Exception:
            raise ClientError

    def put(self,metric, value, timestamp):
        loop = asyncio.get_event_loop()
        message = "put {} {} {}\n".format(metric,value,timestamp)
        loop.run_until_complete(self.put_message(message,loop))
        loop.close()


    async def get_message(self,message,loop):
        try:
            reader, writer = await asyncio.open_connection(self.host, self.port,loop = loop)
            print("send:  {}".format(message))
            result = writer.write(message.encode())
            writer.close()
        except Exception:
            return ""
        return result


    def get(self,metric):
        loop = asyncio.get_event_loop()
        message = "get {}\n".format(metric)
        result = loop.run_until_complete(self.get_message(message,loop))
        loop.close()
        return result

class ClientError(Exception):
    pass