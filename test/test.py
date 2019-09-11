import json
import logging
import os
import subprocess
import time
import unittest
from typing import List

import gremlin_python.driver.client
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.anonymous_traversal import traversal

from grafico import config
from grafico.load import Entity, Transformer

log = logging.getLogger(__file__)


class GraficoTestCase(unittest.TestCase):
    server_path = os.path.join(
        config.project_root,
        'apache-tinkerpop-gremlin-server-3.4.3',
        'bin',
        'gremlin-server.sh'
    )

    def setUp(self) -> None:
        server_config = os.path.join(config.project_root, 'gremlin-server-grafico.yaml')
        self.server_command(['start', server_config])
        timeout = time.time() + 10
        while True:
            try:
                gremlin_python.driver.client.Client('ws://localhost:8182/gremlin', 'g')
            except ConnectionRefusedError:
                if time.time() > timeout:
                    raise
                log.warning('Waiting for Gremlin Server to start...')
                time.sleep(1)
            else:
                break

    def tearDown(self) -> None:
        self.server_command(['stop'])

    def server_command(self, args: List[str]):
        subprocess.run([self.server_path] + args)

    def test_server_runs(self):
        g = traversal().withRemote(DriverRemoteConnection('ws://localhost:8182/gremlin', 'g'))
        print(g.V().values())


class TestEntity(unittest.TestCase):

    def test_load_entity_json(self):
        metadata = load_test_file('metadata.json')
        transformer = Transformer()
        entities = list(transformer.extract_json(metadata))
        self.assertEqual(len(entities), 329)
        for entity in entities:
            self.assertEqual(type(entity), Entity)
            self.assertIn(entity.entity_type, ('file', 'biomaterial', 'process', 'protocol'))
            self.assertEqual(len({e.document_id for e in entities}), len(entities))


def load_test_file(file_name):
    path = os.path.join(config.project_root, 'test', 'data', file_name)
    with open(path, 'r') as f:
        return json.load(f)
