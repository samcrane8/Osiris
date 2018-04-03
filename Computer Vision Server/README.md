

# Computer Vision Server (Tensorflow Serve)

The goal is to be able to have any multitude of analysis of streams: n streams can be analyzed by m programs and redistributed to c clients. 

In here will be a base vision module, and then the ability to inherit that structure so that vision processes can be added and removed at will.

The short-term implementation is simply sending a post-request everytime a frame is received from the stream. 