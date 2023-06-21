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

web-serving-start:	
	docker run -it --net=host --name=database_server cloudsuite/web-serving:db_server
	docker run -dt --net=host --name=memcache_server cloudsuite/web-serving:memcached_server
	docker run -dt --net=host --name=web_server cloudsuite/web-serving:web_server /etc/bootstrap.sh ${http} ${127.0.0.1} ${127.0.0.1} ${127.0.0.1} ${4} ${auto}

web-serving-benchmark:
	docker run --net=host --name=faban_client -v ./faban_output:/faban/output cloudsuite/web-serving:faban_client ${127.0.0.1} ${1}	

	
