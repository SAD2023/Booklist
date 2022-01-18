import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import firestore

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtGui import QIntValidator,QDoubleValidator,QFont
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt


# Using a service account
cred = credentials.Certificate('')
firebase_admin.initialize_app(cred)

# Setting up the Database
db = firestore.client()


""" 
 Takes several QT Widgets and their text inputs and adds the corresponding info
 to the collection "books" by creating a new document with the name of the book.

 Parameters:
  Field1, Field2, Field3: QLineEdit Widgets from the layout
  name, rating, comment: text input (strings) from the QLineEdit widgets

"""
def upload(field1, name, field2, rating, field3, comment):
  # print(name)
  field1.setText("")
  field2.setText("")
  field3.setText("")
  doc_ref = db.collection('books').document(name)
  doc_ref
  doc_ref.set({
    'name': name,
    "rating": 10, 
    "thoughts": comment
})

"""  
  The main function, which creates the layout, creates all of the widgets, and
  adds them to the layout.

  Parameters: none
"""
def window():
  app = QApplication([])
  window = QWidget()
  window.setFixedWidth(400)
  window.setFixedHeight(250)
  label = QLabel("Add a book!")
  label.setFont(QFont("Courier New", 23))
  layout = QVBoxLayout()
  button1 = QPushButton('Add')
  layout.addWidget(label)

  e1 = QLineEdit()
  e1.setAlignment(Qt.AlignRight)
  e1.setFont(QFont("Courier New",15))
  e1.setPlaceholderText("Name of the book ") 

  
  e2 = QLineEdit()
  e2.setAlignment(Qt.AlignRight)
  e2.setFont(QFont("Courier New",15))
  e2.setPlaceholderText("A Rating for the book ") 

    
  e3 = QLineEdit()
  e3.setAlignment(Qt.AlignRight)
  e3.setFont(QFont("Courier New",15))
  e3.setPlaceholderText("Thoughts on the book ") 

  layout.addWidget(e1)
  layout.addWidget(e2)
  layout.addWidget(e3)
  layout.addWidget(button1)

  
  button1.clicked.connect(lambda: upload(e1, e1.text(), e2, e2.text(), e3, e3.text()))


  window.setLayout(layout)
  window.show()
  app.exec()

# Starts running the program
window()
