import apache_beam as beam

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

import logging
import re

class WordExtractingDoFn(beam.DoFn):
    """Parse each line of input text into words."""

    def process(self, element):
        """Returns an iterator over the words of this element.
        The element is a line of text.  If the line is blank, note that, too.
        Args:
            element: the element being processed
        Returns:
            The processed element.
        """
        return re.findall(r'[\w\']+', element, re.UNICODE)

class AstraStoreDoFn(beam.DoFn):
    """Adaptation of our example Flink application (https://github.com/absurdfarce/flink-astra) to work with Beam"""

    def __init__(self, scb, clientid, secret):
        self.scb = scb
        self.clientid = clientid
        self.secret = secret

        self.log = logging.getLogger()
        self.log.setLevel('DEBUG')

        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
        self.log.addHandler(handler)

    def setup(self):
        self.log.info("AstraStoreDoFn.setup started")

        self.cluster = Cluster(cloud={'secure_connect_bundle': self.scb},
                               auth_provider=PlainTextAuthProvider(self.clientid, self.secret))
        self.session = self.cluster.connect()
        self.ps = self._setupSchema()

        self.log.info("AstraStoreDoFn.setup complete")

    def teardown(self):
        self.session.shutdown()
        self.cluster.shutdown()

    def process(self, element):
        (word, count) = element
        self.log.info(
            "Executing prepared statement, word: %s, count: %s", word, count)
        self.session.execute(self.ps, element)

    def _setupSchema(self):
        self.session.execute("drop table if exists example.wordcount")
        self.session.execute("CREATE TABLE IF NOT EXISTS example.wordcount (\n" +
                             "word text,\n" +
                             "count bigint,\n" +
                             "PRIMARY KEY(word))\n")
        return self.session.prepare("insert into example.wordcount (word,count) values (?,?)")
