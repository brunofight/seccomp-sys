install:
    pip install -r requirements.txt
  
start:
    docker-compose up
  
complain-test:
	sudo tail -f /var/log/syslog | grep audit | grep "type=1326" > complain-log.json &
	sudo docker run --rm --security-opt seccomp=profiles/all_log.json -p 127.0.0.1:8000:80/tcp nginx:latest

