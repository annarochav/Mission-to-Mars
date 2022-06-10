# The next part is actually building the framework for the app using Flask and Mongo together.
# Let's begin by importing our tools.

# We're saying use Flask to render a template, redirecting to another url, and creating a URL.
from flask import Flask, render_template, redirect, url_for

# this line says we'll use PyMongo to interact with our Mongo database.
from flask_pymongo import PyMongo

#this line says that to use the scraping code, we will convert from Jupyter notebook to Python.
import scraping

#let's add the following to set up Flask:
app = Flask(__name__)

#We also need to tell Python how to connect to Mongo using PyMongo
# Use flask_pymongo to set up mongo connection
# app.config["MONGO_URI"] tells Python that our app will connect to Mongo using a URI
# "mongodb://localhost:27017/mars_app" is the URI we'll be using to connect our app to Mongo.
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#Set Up App Routes
#The code we create next will set up our Flask routes:
#one for the main HTML page everyone will view when visiting the web app.
#one to actually scrape new data using the code we've written.
# First, let's define the route for the HTML page. 

#@app.route("/"), tells Flask what to display when we're looking at the home page, index.html, home page.
@app.route("/")
def index():
    # uses PyMongo to find the "mars" in our db, convert our Jupyter scraping code to Python Script.
    #We will also assign that path to the mars variable for use later.
   mars = mongo.db.mars.find_one()
   #tells Flask to return an HTML template using an index.html file. 
   #We'll create this file after we build the Flask routes.
   #mars=mars tells Python to use the "mars" collection in MongoDB
   #This function is what links our visual representation of our work
   return render_template("index.html", mars=mars)

#Our next function will set up our scraping route.
#this route will be the "button" of the web application
#the one that will scrape updated data when we tell it to from the homepage of our web app.   

#defines the route that Flask will be using.
@app.route("/scrape")

#The next lines allow us to access the database
#scrape new data using our scraping.py script
# update the database, and return a message when successful.
def scrape():
    # we assign a new variable that points to our Mongo database: 
   mars = mongo.db.mars
   #we created a new variable to hold the newly scraped data
   #we're referencing the scrape_all in the scraping.py file exported from Jupyter Notebook.
   mars_data = scraping.scrape_all()
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   return redirect('/', code=302)

#Now that we've gathered new data, we need to update the database using
#Here, we're inserting data, but not if an identical record already exists.
.update_one(query_parameter, {"$set": data}, options)

#The syntax used is {"$set": data}. The document will be modified ("$set") with the data in question.
#Finally, the option we'll include is upsert=True. 
mars.update_one({}, {"$set":mars_data}, upsert=True)

#Finally, we will add a redirect after successfully scraping the data:
#this will navigate our page back to / where we can see the updated content.
return redirect('/', code=302)

#The final bit of code we need for Flask is to tell it to run. 
if __name__ == "__main__":
   app.run()