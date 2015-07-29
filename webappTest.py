#/usr/bin/python
import web.wsgiserver

def my_wsgi_app(env, start_response):
    status = '200 OK'                                                                                                                         
    response_headers = [('Content-type','text/plain')]
    start_response(status, response_headers)
    return 'Hello wsorld!'

server = web.wsgiserver.CherryPyWSGIServer(("127.0.0.1", 8080), my_wsgi_app);
server.start()