# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# myapp = Flask(__name__)
# #myapp.config.from_object('config')
# myapp.config['SQLALCHEMY_DATABASE_URI']='mysql://root:wozai123@localhost:3306/UIAUTO'
# db = SQLAlchemy(myapp)
#
# from myapp import view11,model1
#
from flask import Flask
import  sys
sys.path.append('.')
myapplication = Flask(__name__)