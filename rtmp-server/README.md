
# RTMP Server

This will be detail how to setup a RTMP server that can manage the broadcaster and listener streams. Mostly this folder will contain configuration files and instructions.


## Instructions

### Adjust Security Group

	Open 1935 port to any ip for the RTMP stream (input, from the broadcaster).

	Open 8080 port to any ip for the HLS stream (output, to the client).

### Install Dependencies

	First, install make.

	'sudo apt-get install make'

	Here, inside the rtmp-server, is a Makefile that works for Ubuntu linux. First, install all the dependencies:

	`sudo make configure-rtmp-server'


### Helpful Blogs

	https://docs.peer5.com/guides/setting-up-hls-live-streaming-server-using-nginx/