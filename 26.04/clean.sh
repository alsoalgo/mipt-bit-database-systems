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

cd docker
echo "${INFO} Stopping redis-app script..."
docker stop redis-app
docker rm redis-app
echo "${INFO} Stopping docker-compose..."
docker-compose down
cd ..

echo "${INFO} Stopping redis-cluster..."
rm -rf redis-cluster/data1
rm -rf redis-cluster/data2
rm -rf redis-cluster/data3

echo "${INFO} Removing docker network..."
docker network rm redis-network
