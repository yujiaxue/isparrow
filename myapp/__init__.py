# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# myapp = Flask(__name__)
# #myapp.config.from_object('config')
# myapp.config['SQLALCHEMY_DATABASE_URI']='mysql://root:wozai123@localhost:3306/UIAUTO'
# db = SQLAlchemy(myapp)
#
# from myapp import view11,model1
#
import sys

reload(sys)
sys.setdefaultencoding('utf8')
from flask import Flask

myapplication = Flask(__name__)
