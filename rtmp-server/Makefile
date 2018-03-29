RTMP_URL = https://github.com/arut/nginx-rtmp-module/archive/v1.2.1.tar.gz


download-rtmp-server:
	sudo apt-get install build-essential libpcre3 libpcre3-dev libssl-dev
	git clone https://github.com/sergey-dryabzhinsky/nginx-rtmp-module.git
	wget http://nginx.org/download/nginx-1.13.1.tar.gz
	tar -xf nginx-1.13.1.tar.gz
	cd nginx-1.13.1/

configure-rtmp-server:
	sudo ./configure --with-http_ssl_module --add-module=../nginx-rtmp-module
	make -j 1
	sudo make install
	export PATH=$PATH:/usr/local/nginx/sbin

update-config-file:
	cp configs/nginx.conf /etc/nginx/nginx.conf


test-config:
	/usr/local/nginx/sbin/nginx -t