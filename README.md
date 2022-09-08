# beam-astra
Example(s) of using DataStax Astra with Apache Beam.

# Overview

For now this is just a simple adaptation of some of the Beam examples to work with DataStax Astra.  The current examples cover only the Python API; other examples for the other supported languages might be added in the future.  If you're familiar with [similar work](https://github.com/absurdfarce/flink-astra) around Apache Flink a lot of this will look familiar.

# Setup

Begin by creating a venv with Beam and the [DataStax Driver for Apache Cassandra](https://github.com/datastax/python-driver) installed.  [Instructions](https://beam.apache.org/get-started/quickstart-py/) for doing so can be found on the Apache Beam site.  This should work out to something like the following:

```
python -m venv beam-astra
. ./beam-astra/bin/activate
pip install --upgrade pip
pip install --upgrade setuptools
pip install apache-beam
pip install cassandra-driver
```

# Running the app

The app assumes that a keyspace named "example" has been created on Astra.  The app will create any additional schema that is necessary in this keyspace (if it is not already present).  You can run the app from the "python" directory with something like the following:

```
python -m beam_astra.wordcount --input <path to input file> --scb <path to Astra SCB> --clientid <Astra clientid> --secret <Astra secret>
```

After the run completes you can confirm the results by querying your Astra database:

```
token@cqlsh: select * from example.wordcount ;

 word   | count
--------+-------
   dogs |     1
 lazier |     1
  least |     1
  foxes |     1
 jumped |     1
     at |     1
    are |     1
   just |     1
  quick |     1
   than |     1
    fox |     1
    our |     1
    dog |     2
     or |     1
   over |     1
  brown |     1
   lazy |     1
    the |     2

(18 rows)
```
