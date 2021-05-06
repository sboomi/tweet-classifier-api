"""Web Server Gateway Interface"""
##################
# FOR PRODUCTION
####################
from src import create_app

app = create_app()

if __name__ == "__main__":
    ####################
    # FOR DEVELOPMENT
    ####################
    app.run(host='0.0.0.0', debug=True)
