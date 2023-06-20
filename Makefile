install:
	pip install -r requirements.txt
	curl -s https://download.sysdig.com/DRAIOS-GPG-KEY.public | sudo apt-key add -  
	sudo curl -s -o /etc/apt/sources.list.d/draios.list https://download.sysdig.com/stable/deb/draios.list  
	sudo apt-get update
	sudo apt-get -y install linux-headers-$(uname -r)
	sudo apt-get -y install sysdig

start:
	docker-compose up

nginx:
	docker run -d --rm --name nginx nginx:latest

sysdig-nginx:
	sysdig -pc container.name=nginx -S
