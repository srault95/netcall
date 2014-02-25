# vim: fileencoding=utf-8 et ts=4 sts=4 sw=4 tw=0 fdm=marker fmr=#{,#}

from gevent import monkey
monkey.patch_all()

from os       import removedirs
from tempfile import mkdtemp
from unittest import TestCase

from netcall.green import GeventRPCClient


class GeventClientTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tmp_dir = mkdtemp(prefix='netcall-test-')
        cls.urls    = [
            'ipc://%s/test-%s' % (cls.tmp_dir, i)
            for i in range(3)
        ]
        cls.extra   = ['ipc://%s/extra' % cls.tmp_dir]

    @classmethod
    def tearDownClass(cls):
        removedirs(cls.tmp_dir)

    def setUp(self):
        self.client = GeventRPCClient()

    def tearDown(self):
        self.client.socket.close(0)


    def test_initial_state(self):
        client = self.client

        self.assertTrue(not client.bound)
        self.assertTrue(not client.connected)


    def test_bind_one(self):
        client = self.client
        url    = self.urls[0]

        client.bind(url)

        self.assertEqual(client.bound, set([url]))
        self.assertTrue(not client.connected)

    def test_bind_many(self):
        client = self.client
        urls   = self.urls

        client.bind(urls)

        self.assertEqual(client.bound, set(urls))
        self.assertTrue(not client.connected)

    def test_rebind_many(self):
        client = self.client
        urls1  = self.urls
        urls2  = urls1[:2] + self.extra

        client.bind(urls1)
        client.bind(urls2)

        self.assertEqual(client.bound, set(urls1 + urls2))
        self.assertTrue(not client.connected)

    def test_rebind_many_only(self):
        client = self.client
        urls1  = self.urls
        urls2  = urls1[:2] + self.extra

        client.bind(urls1)
        client.bind(urls2, only=True)

        self.assertEqual(client.bound, set(urls2))
        self.assertTrue(not client.connected)


    def test_connect_one(self):
        client = self.client
        url    = self.urls[0]

        client.connect(url)

        self.assertEqual(client.connected, set([url]))
        self.assertTrue(not client.bound)

    def test_connect_many(self):
        client = self.client
        urls   = self.urls

        client.connect(urls)

        self.assertEqual(client.connected, set(urls))
        self.assertTrue(not client.bound)

    def test_reconnect_many(self):
        client = self.client
        urls1  = self.urls
        urls2  = urls1[:2] + self.extra

        client.connect(urls1)
        client.connect(urls2)

        self.assertEqual(client.connected, set(urls1 + urls2))
        self.assertTrue(not client.bound)

    def test_reconnect_many_only(self):
        client = self.client
        urls1  = self.urls
        urls2  = urls1[:2] + self.extra

        client.connect(urls1)
        client.connect(urls2, only=True)

        self.assertEqual(client.connected, set(urls2))
        self.assertTrue(not client.bound)

