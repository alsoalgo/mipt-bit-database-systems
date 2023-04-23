GREEN='\033[0;32m'
PURPLE='\033[0;35m'
RED='\033[0;31m'
LIGHT_RED='\033[1;31m'
LIGHT_GRAY='\033[0;37m'
LIGHT_GREEN='\033[1;32m'
LIGHT_BLUE='\033[1;34m'
LIGHT_PURPLE='\033[1;35m'
YELLOW='\033[1;33m'
NC='\033[0m'

INFO="${LIGHT_PURPLE}info    | ${NC}"
ERROR="${LIGHT_RED}error   | ${NC}"
SUCCESS="${GREEN}success | ${NC}"

echo "${INFO} Creating redis-network..."
docker network create redis-network

cd docker

echo "${INFO} Running docker-compose... "
echo "${INFO} Setting up master instances on nodes... "
docker-compose up -d --quiet-pull

cd ..

echo "${INFO} Setting up slave instances on nodes..."
docker exec -idt redis1 sh -c "redis-server /usr/local/etc/redis/slave.conf"
docker exec -idt redis2 sh -c "redis-server /usr/local/etc/redis/slave.conf"
docker exec -idt redis3 sh -c "redis-server /usr/local/etc/redis/slave.conf"

echo "${INFO} Waiting for the cluster to be configured..."
docker exec -it redis1 sh -c "echo \"yes\n\" | redis-cli --cluster create redis1:7001 redis1:7003 redis2:7002 redis2:7001 redis3:7003 redis3:7002 --cluster-replicas 1" 
echo "${INFO} Finished configuring cluster..."
sleep 0.5

echo "${INFO} Waiting for the cluster to be ready..."
sleep 5

attempts=4
ok=false
for i in $(seq 1 $attempts); do
    echo "${INFO} Attempt $i of $attempts..."
    cluster_state=$(redis-cli -p 7001 cluster info | grep cluster_state | cut -d: -f2 | tr -d '[:space:]')
    if [ "$cluster_state" != "ok" ]; then
        echo "${ERROR} Cluster state is not ok, waiting 5 seconds..."
        sleep 5
    else
        echo "${SUCCESS} Cluster state is ${GREEN}ok${NC}, continuing..."
        ok=true
        break
    fi
done

if [ "$ok" = false ]; then
    echo "${ERROR} Cluster state is ${LIGHT_RED}fail${NC}, exiting..."
    $(./clean.sh)
    exit 1
fi

echo "${INFO} Running redis-app script..."

cd docker 
docker build -t redis-app -f Dockerfile.python ..
cd .. 

echo "${INFO} Running docker container with id: $(docker run -d --network=redis-network --name redis-app redis-app)"

echo "${INFO} Data began to be generated and inserted into the cluster"
echo "${INFO} Container logs will be shown below in ~2 minutes:"
echo "${INFO} Loading..."
spin='-\|/'

while :
do
  printf "\b${spin:i++%${#spin}:1}"
  if [ ! "$(docker ps -q -f name=redis-app)" ]; then
    printf "\b"
    break
  fi
  sleep 0.1
done

docker logs -f redis-app

echo "${INFO} End of container logs"

echo "${INFO} Data was generated and inserted into the cluster"
echo "${INFO} Now you can use redis-cli to check it"

echo "${INFO} Additional info about cluster:"

dbsize1=$(redis-cli -p 7001 dbsize)
dbsize2=$(redis-cli -p 7002 dbsize)
dbsize3=$(redis-cli -p 7003 dbsize)

echo "${INFO} dbsize on node 1: $dbsize1"
echo "${INFO} dbsize on node 2: $dbsize2"
echo "${INFO} dbsize on node 3: $dbsize3"
echo "${INFO} Total dbsize: $(($dbsize1 + $dbsize2 + $dbsize3))"

echo "${INFO} Benchmark info:"

docker exec -it redis1 sh -c "redis-benchmark -c 100 -n 100000 -t set,get -P 16 --cluster --csv -p 7001"

#$(./clean.sh)
