CREATE KEYSPACE reviews WITH replication = {
    'class': 'NetworkTopologyStrategy', 'datacenter1': '3'};
