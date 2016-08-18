from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class webserverHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            # View all restaurants
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                restaurants = session.query(Restaurant).all()

                output = ""
                output += "<html><body>"
                output += "<a href='/restaurants/new'> Make a New Restaurant</a><br><br>"
                for restaurant in restaurants:
                    output += restaurant.name
                    output += "<div>"
                    output += "<a href='/restaurants/%s/edit'>Edit</a>" % restaurant.id
                    output += "<br>"
                    output += "<a href='/restaurant/%s/delete'>Delete</a>" % restaurant.id
                    output += "</div>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            # Add a new restaurant
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                output = ""
                output += "<html><body>"
                output += "<h2>Create a new Restaurant: </h2>"

                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>"
                output += "<input name='r_name' type='text' placeholder='Restaurant Name' >"
                output += "<input type='submit' value='Submit'></form>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return 

            # Edit a restaurant
            if self.path.endswith("/edit"):
                # Grab third element
                restaurant_id = self.path.split("/")[2]
                the_restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()

                if the_restaurant:
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    
                    output = ""
                    output += "<html><body>"
                    output += "<h2>Edit Restaurant %s: </h2>" %the_restaurant.name
                    
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>" % restaurant_id
                    output += "<input name='new_r_name' type='text' placeholder='Restaurant Name' >"
                    output += "<input type='submit' value='Edit'></form>"
                    output += "</body></html>"
                    self.wfile.write(output)
                    print output
                    return 

            
            # Delete a restaurant
            if self.path.endswith("/delete"):
                # Grab third element
                restaurant_id = self.path.split("/")[2]
                the_restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()

                if the_restaurant:
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    
                    output = ""
                    output += "<html><body>"
                    output += "<h2>Are you sure you want to delete %s?</h2>" %the_restaurant.name
                    
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'>" % restaurant_id
                    output += "<input type='submit' value='Delete'></form>"
                    output += "</body></html>"
                    self.wfile.write(output)
                    print output
                    return 
                
                    
        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)
            
    def do_POST(self):
        
        try:

            if self.path.endswith("/restaurants/new"):
        
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('r_name')
                
                r_name = messagecontent[0]
                new_rest = Restaurant(name=r_name)
                session.add(new_rest)
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                

            if self.path.endswith('/edit'):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('new_r_name')
                    rest_id = self.path.split("/")[2]

                    the_restaurant = session.query(Restaurant).filter_by(id = rest_id).one()
                    if the_restaurant != []:
                        the_restaurant.name = messagecontent[0]
                        session.add(the_restaurant)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()

            if self.path.endswith('/delete'):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    rest_id = self.path.split("/")[2]

                    the_restaurant = session.query(Restaurant).filter_by(id = rest_id).one()
                    if the_restaurant != []:
                        session.delete(the_restaurant)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()
                        

        except:
            pass


        

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print "Web server running on port %s" % port
        server.serve_forever()
        
    
    except KeyboardInterrupt:
        print "^C entered stopping web server..."
        server.socket.close()
    


if __name__ == '__main__':
    main()
    