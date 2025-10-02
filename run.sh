SERVER_NAME=tmp-pg-server
DB_PASSWORD=test

docker network create pg-network >/dev/null 2>&1 || true
docker run \
  --rm \
  --name $SERVER_NAME \
  -e POSTGRES_PASSWORD=$DB_PASSWORD \
  -p 5432:5432 \
  -d \
  --network pg-network \
  -v $1/seeds:/docker-entrypoint-initdb.d/ \
  postgres >/dev/null 2>&1 || true
echo "Waiting for postgres server to start..."

# Wait until Postgres is ready
docker run \
  --rm \
  --network pg-network \
  postgres /bin/bash -c "export PGPASSWORD='$DB_PASSWORD';psql -h $SERVER_NAME -U postgres" >/dev/null 2>&1
while [ $? -ne 0 ] ; do
#   echo "Waiting for postgres server to start..."
  sleep 1
  docker run \
    --rm \
    --network pg-network \
    postgres /bin/bash -c "export PGPASSWORD='$DB_PASSWORD';psql -h $SERVER_NAME -U postgres" >/dev/null 2>&1
done

# Postgres is ready
echo "Postgres server is up and running"
docker run -it --rm --network pg-network -e PGPASSWORD=$DB_PASSWORD postgres psql -h $SERVER_NAME -U postgres
docker stop $SERVER_NAME
docker network remove pg-network