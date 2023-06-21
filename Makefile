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
	docker run -d --rm --name nginx -p 8080:80 nginx:latest

sysdig-nginx:
	sysdig -pc -c ./scripts/countSyscalls container.name=nginx -S

web-server-start:	
	docker run --rm -it --net=host --name=database_server cloudsuite/web-serving:db_server
	docker run --rm -dt --net=host --name=memcache_server cloudsuite/web-serving:memcached_server
	docker run --rm -dt --net=host --name=web_server cloudsuite/web-serving:web_server /etc/bootstrap.sh http 10.0.2.15 10.0.2.15 10.0.2.15 4 auto

web-server-stop:
	docker stop web_server memcache_server database_server

web-server-benchmark:
	docker run --net=host --name=faban_client -v ./faban_output:/faban/output cloudsuite/web-serving:faban_client 10.0.2.15 1	

	
