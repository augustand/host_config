# -*- coding:utf-8 -*-
import etcd

client = etcd.Client(host='10.1.51.133', port=2379)
client.write('/nodes/n1', 'ssss')
# with ttl
client.write('/nodes/n2', 2)  # sets the ttl to 4 seconds

c = client.read('/projects',recursive=True)
for child in c.children:
    print("%s: %s" % (child.key,child.value))


result = client.read('/nodes/n1')
print(result.value)  # bar
result.value += u'bar'
updated = client.update(result) # if any other client wrote '/foo' in the meantime this will fail
print(updated.value) # barbar

print client.machines
print client.leader

# mkdir
# client.write('/nodes/queue', None, dir=True)
# Append a value to a queue dir
client.write('/nodes/queue', 'test', append=True) #will write i.e. /nodes/queue/11
client.write('/nodes/queue', 'test2', append=True) #will write i.e. /nodes/queue/12

r = client.read('/nodes', recursive=True, sorted=True)
for child in r.children:
    print("%s: %s" % (child.key,child.value))