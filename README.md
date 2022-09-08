# beam-astra
Example(s) of using DataStax Astra with Apache Flink.

# Overview

For now this is just a simple adaptation of some of the Beam examples to work with DataStax Astra.  The current examples cover only the Python API; other examples for the other supported languages might be added in the future.

# Setup

Begin by creating a venv with Beam and the [DataStax Driver for Apache Cassandra](https://github.com/datastax/python-driver) installed.  [Instructions](https://beam.apache.org/get-started/quickstart-py/) for doing so can be found on the Apache Beam site.  This should work out to something like the following:

> python -m venv beam-astra
> . ./beam-astra/bin/activate
> pip install --upgrade pip
> pip install --upgrade setuptools
> pip install apache-beam
> pip install cassandra-driver

# Running the app

The app assumes that a keyspace named "example" has been created on Astra.  The app will create any additional schema that is necessary in this keyspace (if it is not already present).  You can run the app from the "python" directory with something like the following:

> python -m beam_astra.wordcount --input <path to input file> --scb <path to Astra SCB> --clientid <Astra clientid> --secret <Astra secret>

