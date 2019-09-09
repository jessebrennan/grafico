
console:
	apache-tinkerpop-gremlin-console-3.4.3/bin/gremlin.sh

kill_server:
	kill $$(netstat -nlp | grep '127.0.0.1:8182' | awk '{ print $$7 }' | sed 's#/java##')
