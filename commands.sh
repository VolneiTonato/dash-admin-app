docker container stop dash-admin
docker container rm dash-admin
docker run -it -p 8082:8050 \
    --network=ssh_net \
    --env="REDIS_HOST=redis://redis" \
    --env="FLASK_DEBUG=True" \
    --env="FLASK_APP=pyapp.app" \
    --name=dash-admin \
    tonato/dash-admin-app:latest bash start_app.sh

