from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class HandleRequests(BaseHTTPRequestHandler):
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server    """

    def parse_url(self, path):
        path_params = path.split("/")
        resource = path_params[1]

        #Check if there is a query string parameter
        if "?" in resource:

            param = resource.split("?")[1]  
            resource = resource.split("?")[0] 
            pair = param.split("=")  
            key = pair[0]  
            value = pair[1] 

            return (resource, key, value)

        #No query string parameter"""
        else:
            id = None

            try:
                    id = int(path_params[2])
            except IndexError:
                pass  # No route parameter exists
            except ValueError:
                pass  # Request had trailing slash

            return (resource, id)

    def _set_headers(self, status):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods','GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers','X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_GET(self): 
        #requests to server
        self._set_headers(200)
        response = {}

        parsed = self.parse_url(self.path)

        if (len(parsed)) == 2:
            (resource, id) = parsed
            
            #Will put all all users, posts, comment, etc stuff here.
            if resource =="users":
                response = f"{get_all_users()}"

            else:
                response = []
        
        elif (len(parsed)) == 3:
            #Will be our searches here, like user = this and comment = that
            (resource, key, value) = parsed

            response = {}
        
        self.wfile.write(f"{response}".encode())

    # def do_POST(self):

    # def do_PUT(self):

    # def do_DELETE(self):



# Outside of the class. 
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()  