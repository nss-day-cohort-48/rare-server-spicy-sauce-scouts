from tags import create_tag, delete_tag, get_all_tags, get_tags_by_post, get_tags_by_user, get_all_posttags, create_posttag, delete_posttag, update_tag
from comments import get_comments_by_user
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from users import get_all_users, get_single_user, create_user, delete_user, update_user
from posts import get_posts_by_category, update_post, create_post, delete_post, get_posts_by_subscription
from comments import get_comments_by_post, get_comments_by_user, create_comment, update_comment, delete_comment, get_all_comments
from categories import get_all_categories, create_category

#Need to import all the functions to create, edit, delete, etc.

#Didn't do any of these for subscriptions yet.

class HandleRequests(BaseHTTPRequestHandler):
    """Controls GET, PUT, POST, DELETE requests to the server    """

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

        if len(parsed) == 2:
            (resource, id) = parsed
            
            #Will put all all users, posts, comment, etc stuff here.
            if resource =="users": 
                #Single item on this but will need on others.
                if id is not None:
                    response = f"{get_single_user(id)}"
                else:
                    response = f"{get_all_users()}"
            elif resource == "posts":
                response = get_posts()

            elif resource == "comments":
                response = get_all_comments()

            elif resource == "categories":
                if id is not None:
                    response = f"{get_single_category(id)}"
                else:
                    response = get_all_categories()
            elif resource == "reactions":
                response = get_all_reactions()

            elif resource == "tags":
                response = get_all_tags()

            elif resource == "posttags":
                response = get_all_posttags()

            else:
                response = []
        
        elif (len(parsed)) == 3:
            #Will be our searches here, like user = this and comment = that
            #Proper url format is domain:port/resource?key=value
            (resource, key, value) = parsed
            
            if resource == "posts" and key == "category_id":
                intValue=(int(value))
                response = f"{get_posts_by_category(intValue)}"
            elif resource == "posts" and key == "subscriber_id":
                intValue=(int(value))
                response = f"{get_posts_by_subscription(intValue)}"
            elif resource == "comments" and key == "post_id":
                intValue=(int(value))
                response = f"{get_comments_by_post(intValue)}"
            elif resource == "comments" and key == "user_id":
                intValue=(int(value))
                response = f"{get_comments_by_user(intValue)}"
            elif resource == "tags" and key == "post_id":
                intValue=(int(value))
                response = f"{get_tags_by_post(intValue)}"
            elif resource == "tags" and key == "user_id":
                intValue=(int(value))
                response = f"{get_tags_by_user(intValue)}"
            else:
                response = {}
        
        self.wfile.write(f"{response}".encode())

    def do_POST(self):
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        post_body = json.loads(post_body)

        (resource, _) = self.parse_url(self.path)

        response = None

        if resource == "register":
            response = create_user(post_body)
        elif resource == "posts":
            response = create_post(post_body)
        elif resource == "comments":
            response = create_comment(post_body)
        elif resource == "categories":
            response = create_category(post_body)
        elif resource == "reactions":
            response = create_reaction(post_body)
        elif resource == "tags":
            response = create_tag(post_body)
        elif resource == "posttags":
            response = create_posttag(post_body)

        self.wfile.write(f"{response}".encode())

    def do_PUT(self):
        self._set_headers(204)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        (resource, id) = self.parse_url(self.path)

        success = False

        # Update a single item
        if resource == "users":
            success = update_user(id, post_body)
        if resource == "posts":
            success = update_post(id, post_body)
        if resource == "comments":
            success = update_comment(id, post_body)
        if resource == "categories":
            success = update_category(id, post_body)
        if resource == "reactions":
            success = update_reaction(id, post_body)
        if resource == "tags":
            success = update_tag(id, post_body)
        
        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())

    def do_DELETE(self):
        self._set_headers(204)

        (resource, id) = self.parse_url(self.path)

        # Delete a single object from the list
        if resource == "users":
            delete_user(id)
        if resource == "posts":
            delete_post(id)
        if resource == "comments":
            delete_comment(id)
        if resource == "categories":
            delete_category(id)
        if resource == "reaction":
            delete_reaction(id)
        if resource == "tags":
            delete_tag(id)
        if resource == "posttags":
            delete_posttag(id)

        self.wfile.write("".encode())

# Outside of the class. 
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()  
