import threading
import unittest
import subprocess


class Ping(threading.Thread):
    def __init__(self, host, timeout=5):
        threading.Thread.__init__(self)
        self.host = host
        self.timeout = timeout

    def run(self) -> None:
        ping = subprocess.Popen(['ping', self.host], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            ping.communicate(timeout=self.timeout)
        except subprocess.TimeoutExpired as ex:
            pass


class TestPing(unittest.TestCase):
    def test_ping(self):
        hosts = ['www.baidu.com', 'google.com', 'youku.com', 'youtube.com', 'pangu_test.datacaciques.com'] * 10
        pings = []

        for host in hosts:
            ping = Ping(host)
            ping.start()
            pings.append(ping)

        for ping in pings:
            ping.join()

        print('all dome')
