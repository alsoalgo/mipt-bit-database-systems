from redis.cluster import RedisCluster as Redis
from redis.cluster import ClusterNode

from utils.generator import Generator
from utils.redis_data_inserter import RedisDataInserter

import time

def main():
    nodes = [ClusterNode('redis1', 7001), ClusterNode('redis2', 7002), ClusterNode('redis3', 7003)]
    rc = Redis(startup_nodes=nodes)
    
    generator = Generator()
    generator.generate()
    data = generator.get_data()
    
    redis_data_inserter = RedisDataInserter(rc)

    start = time.process_time()
    redis_data_inserter.insert(data)
    print("Time:", time.process_time() - start, "s")


if __name__ == '__main__':
    main()