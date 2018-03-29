# Osiris
This is server that allows n video streams to be analyzed by any given computer vision algorithm and then served to m clients, in a horizontally scaleable format.

There are two major servers running to make this system work: one built with Flask, and the other is a configuration of Nginx using nginx-rtmp-server to handle streamed data.

# Database

The database is postgres.

Database name: osiris.


## Useful links

These are articles that helped with different steps of running and developing this project.

setting up postgres with django: https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04
