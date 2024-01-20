import threading
from threading import Thread, Lock
from socketserver import TCPServer
from http.server import BaseHTTPRequestHandler, SimpleHTTPRequestHandler, HTTPServer
import os
import json
import socket
from tkinter import *
from tkinter.simpledialog import askstring
from time import sleep

global UDP_RESP
global UDP_SERVER

global webServer
global jsonServer

UDP_RESP = b""
UDP_SERVER = "127.0.0.1"

responseLock = Lock()
stop_threads = threading.Event()

class HttpdServer(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        webroot = os.path.dirname(os.path.realpath(__file__)) + "/webroot"
        super().__init__(*args, directory=webroot, **kwargs)

class JsonServer(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def do_GET(self):
        self.do_HEAD()
        responseLock.acquire()
        self.wfile.write(UDP_RESP)
        responseLock.release()

class MyThreads():

    def UdpThread():
        UDP_PORT = 65243

        sock = socket.socket(socket.AF_INET, # Internet
                            socket.SOCK_DGRAM) # UDP
        sock.bind((UDP_SERVER, UDP_PORT))
        sock.settimeout(1)

        print("UDP socket bound")

        while not stop_threads.is_set():
            global UDP_RESP
            try:
                data, addr = sock.recvfrom(1024*1024)
                # drop trailing null character
                data = data[:(len(data)-1)]
                print(data + b"\n")
                # only handle next athlete and measurement
                if (data.find(b"\"JIDS\":\"WMTNX") >= 0) or (data.find(b"\"JIDS\":\"WMTMS") >= 0):
                    responseLock.acquire()
                    UDP_RESP=data
                    responseLock.release()
            except socket.timeout:
                pass

        webServer.shutdown()
        jsonServer.shutdown()

        sock.close()
        print("UDP socket closed")

    def HttpThread():
        global webServer

        hostName = "localhost"
        serverPort = 55555
        webServer = TCPServer((hostName, serverPort), HttpdServer)
        print("HTTP server started http://%s:%s" % (hostName, serverPort))

        webServer.serve_forever()

        webServer.server_close()
        print("HTTP server stopped")

    def JsonThread():
        global jsonServer

        hostName = "localhost"
        serverPort = 55556

        jsonServer = HTTPServer((hostName, serverPort), JsonServer)
        print("JSON server started http://%s:%s" % (hostName, serverPort))

        jsonServer.serve_forever()

        jsonServer.server_close()
        print("JSON server stopped.")

if __name__ == "__main__":
    myThreads = MyThreads

    configfile = None

    try:
        configFile = open("settings.json", "r")
        config = json.load(configFile)
        UDP_SERVER=config["server"]
    except:
        pass

    if configfile != None:
        configFile.close()

    win=Tk()
    win.withdraw()

    ip = askstring('UDP Server', 'IP Addresse aus Weitenmessung GUI\t', initialvalue=UDP_SERVER)
    win.destroy()

    if ip != None:
        UDP_SERVER = ip
        config={}
        config["server"]=ip
        configFile = open("settings.json", "w")
        json.dump(config, configFile)
        configFile.close()
        print("UDP Server IP is " + ip)

    thHttpd = Thread(target=myThreads.HttpThread)
    thHttpd.start()

    thJson = Thread(target=myThreads.JsonThread)
    thJson.start()

    thUdp = Thread(target=myThreads.UdpThread)
    thUdp.start()

    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        stop_threads.set()

    thUdp.join()
    thHttpd.join()
    thJson.join()
