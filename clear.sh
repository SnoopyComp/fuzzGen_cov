docker rm $(docker ps -qa)
docker rmi $(docker image -q)
docker system prune -a
sudo rm -rf /tmp/*
rm -rf ~/.local/share/Trash/files/*
