import json
import random
import string
from typing import *
import config
import mimetypes
import os
from framework import HTTPServer, HTTPRequest, HTTPResponse


def random_string(length=20):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))


def default_handler(server: HTTPServer, request: HTTPRequest, response: HTTPResponse):
    response.status_code, response.reason = 404, 'Not Found'
    print(f"calling default handler for url {request.request_target}")


def task2_data_handler(server: HTTPServer, request: HTTPRequest, response: HTTPResponse):
    tar = request.request_target
    # print(tar.find('/data'))
    data = tar.split('/')
    # print(data)
    if tar.find('/data') == 0:
        list = os.listdir('./data')
        if data[2] in list:
            print('dl', data, list)
            response.status_code, response.reason = 200, 'OK'
            with open('.'+tar, 'rb') as file:
                response.body = file.read()
            if data[2].split('.')[1] == 'html':
                response.add_header('Content-Type', 'text/html')
            elif data[2].split('.')[1] == 'js':
                response.add_header('Content-Type', '/javascript')
            elif data[2].split('.')[1] == 'jpg':
                response.add_header('Content-Type', 'image/jpeg')
            response.add_header('Content-Length', len(response.body))
        else:
            response.status_code, response.reason = 404, 'Not Found'
    # TODO: Task 2: Serve static content based on request URL (20%)
    pass


def task3_json_handler(server: HTTPServer, request: HTTPRequest, response: HTTPResponse):
    # TODO: Task 3: Handle POST Request (20%)
    response.status_code, response.reason = 200, 'OK'
    if request.method == 'POST':
        binary_data = request.read_message_body()
        obj = json.loads(binary_data)
        server.task3_data = obj.get('data')
        # TODO: Task 3: Store data when POST
        pass
    else:
        obj = {'data': server.task3_data}
        return_binary = json.dumps(obj).encode()
        response.body = return_binary
        response.add_header('Content-Length', len(response.body))
        pass


def task4_url_redirection(server: HTTPServer, request: HTTPRequest, response: HTTPResponse):
    # TODO: Task 4: HTTP 301 & 302: URL Redirection (10%)
    response.status_code, response.reason = 302, 'Found'
    if request.method == 'GET':
        response.add_header('Location', 'http://127.0.0.1:8080/data/index.html')
    pass

def task5_test_html(server: HTTPServer, request: HTTPRequest, response: HTTPResponse):
    response.status_code, response.reason = 200, 'OK'
    with open("task5.html", "rb") as f:
        response.body = f.read()

def task5_cookie_login(server: HTTPServer, request: HTTPRequest, response: HTTPResponse):
    # TODO: Task 5: Cookie, Step 1 Login Authorization
    obj = json.loads(request.read_message_body())
    if obj["username"] == 'admin' and obj['password'] == 'admin':
        response.status_code, response.reason = 200, 'OK'
        response.add_header('Set-Cookie', 'Authenticated=yes')
        pass
    else:
        response.status_code, response.reason = 403, 'Forbidden'
        pass

def task5_cookie_getimage(server: HTTPServer, request: HTTPRequest, response: HTTPResponse):
    # TODO: Task 5: Cookie, Step 2 Access Protected Resources
    str = request.get_header('Cookie')
    if str == 'Authenticated=yes':
        response.status_code, response.reason = 200, 'OK'
        with open('./data/test.jpg', 'rb') as file:
            response.body = file.read()
        response.add_header('Content-Type', 'image/jpeg')
        response.add_header('Content-Length', len(response.body))
    else:
        response.status_code, response.reason = 403, 'Forbidden'
    pass


def task5_session_login(server: HTTPServer, request: HTTPRequest, response: HTTPResponse):
    # TODO: Task 5: Cookie, Step 1 Login Authorization
    obj = json.loads(request.read_message_body())
    if obj["username"] == 'admin' and obj['password'] == 'admin':
        response.status_code, response.reason = 200, 'OK'
        session_key = random_string()
        while session_key in server.session:
            session_key = random_string()
        server.session[session_key] = True
        response.add_header('Set-Cookie', 'SESSION_KEY='+session_key)
        # print('SESSION_KEY='+session_key)
        pass
    else:
        response.status_code, response.reason = 403, 'Forbidden'


def task5_session_getimage(server: HTTPServer, request: HTTPRequest, response: HTTPResponse):
    # TODO: Task 5: Cookie, Step 2 Access Protected Resources
    str = request.get_header('Cookie')
    if str != None:
        str = str.split('=')[1]
        # print('str', str)
        # print(server.session)
        if server.session.get(str) != None:
            response.status_code, response.reason = 200, 'OK'
            with open('./data/test.jpg', 'rb') as file:
                response.body = file.read()
            response.add_header('Content-Type', 'image/jpeg')
            response.add_header('Content-Length', len(response.body))
        else:
            response.status_code, response.reason = 403, 'Forbidden'
    else:
        response.status_code, response.reason = 403, 'Forbidden'
    pass


# TODO: Change this to your student ID, otherwise you may lost all of your points
YOUR_STUDENT_ID = 12013029

http_server = HTTPServer(config.LISTEN_PORT)
http_server.register_handler("/", default_handler)
# Register your handler here!
http_server.register_handler("/data", task2_data_handler, allowed_methods=['GET', 'HEAD'])
http_server.register_handler("/post", task3_json_handler, allowed_methods=['GET', 'HEAD', 'POST'])
http_server.register_handler("/redirect", task4_url_redirection, allowed_methods=['GET', 'HEAD'])
# Task 5: Cookie
http_server.register_handler("/api/login", task5_cookie_login, allowed_methods=['POST'])
http_server.register_handler("/api/getimage", task5_cookie_getimage, allowed_methods=['GET', 'HEAD'])
# Task 5: Session
http_server.register_handler("/apiv2/login", task5_session_login, allowed_methods=['POST'])
http_server.register_handler("/apiv2/getimage", task5_session_getimage, allowed_methods=['GET', 'HEAD'])

# Only for browser test
http_server.register_handler("/api/test", task5_test_html, allowed_methods=['GET'])
http_server.register_handler("/apiv2/test", task5_test_html, allowed_methods=['GET'])


def start_server():
    try:
        http_server.run()
    except Exception as e:
        http_server.listen_socket.close()
        print(e)


if __name__ == '__main__':
    start_server()