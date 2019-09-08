# Grafico

Graphico is graph database of HCA metadata using Gremlin and Python to
interface with the data.

## Setup

1. Download Gremlin Console and Server
   `http://tinkerpop.apache.org/downloads.html` and unpack the archives
   to this directory.

2. Setup a virtual environment
   ```
   virtualenv .venv -p python3.6
   source .venv/bin/activate
   ```

3. Install Gremlin Python specifics
   ```
   apache-tinkerpop-gremlin-server-3.4.3/bin/gremlin-server.sh install org.apache.tinkerpop gremlin-python 3.4.3
   ```
   ```
   pip install gremlinpython
   ```

