import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import firestore
from firebase_admin import storage

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog
from PyQt5.QtGui import QIntValidator,QDoubleValidator,QFont
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from fpdf import FPDF
import sys

# Using a service account
cred = credentials.Certificate('')
firebase_admin.initialize_app(cred, {'storageBucket': ''})

# Setting up the Database
db = firestore.client()

fileName = "books.pdf"


"""
  Uploads the local file with the name fileName to the firebase storage

    Parameters:
      fileName: string of a file name
"""
def upload_file(fileName):
  bucket = storage.bucket()
  name = fileName.split("/")[-1]
  print(name)
  blob = bucket.blob(name)
  blob.upload_from_filename(fileName)

""" 
  Creates a pdf with the provided text.

  Parameters: 
    text: string
"""
def make_pdf(text):
  pdf = FPDF()

  pdf.add_page()

  pdf.set_font("Arial", size = 15)

  for book in text:  
    book_info_processed = ""
    pdf.set_font("Arial", size = 15, style="U")
    book_info_processed = book_info_processed + book["name"]
    pdf.multi_cell(200, 10, txt = book["name"], 
            align = 'L')
    pdf.set_font("Arial", size = 15, style="")
    pdf.multi_cell(w = 0, h=10, txt = "          Rating: " + str(book["rating"]), 
            align = 'J')
    pdf.multi_cell(w = 0, h=20, txt = "          Thoughts: " + book["thoughts"], 
            align = 'J')


  pdf.output("books.pdf")   

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
Gets the list of books and their corresponding information.

"""
def download():
  doc_ref = db.collection('books')
  docs = doc_ref.stream()
  information = []
  for doc in docs:
    information.append(doc.to_dict())
  
  print(information)
  make_pdf(information)
  



"""  
  The main class, which creates the layout, creates all of the widgets, and
  adds them to the layout.

  Parameters: none
"""
class MainWindow(QWidget):
  def __init__(self):
    QWidget.__init__(self)
    #app = QApplication([])
    window = QWidget()
    window.setFixedWidth(400)
    window.setFixedHeight(250)

    label = QLabel("Add a book!")
    label.setFont(QFont("Courier New", 23))

    layout = QVBoxLayout()

    button1 = QPushButton('Add')
    button2 = QPushButton('Generate List')
    button3 = QPushButton('Add Pdf')
    
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

    layout.addWidget(label)
    layout.addWidget(e1)
    layout.addWidget(e2)
    layout.addWidget(e3)
    layout.addWidget(button3)
    layout.addWidget(button1)
    layout.addWidget(button2)

    button3.clicked.connect(lambda: self.get_file())
    button1.clicked.connect(lambda: upload(e1, e1.text(), e2, e2.text(), e3, e3.text()))
    button2.clicked.connect(lambda : download())


    window.setLayout(layout)
    window.show()
    app.exec()
  
  def get_file(self):
        file_name = QFileDialog.getOpenFileName(self, 'Open File', '.')
        upload_file(file_name[0])
        print(file_name[0])


"""
def window():
  app = QApplication([])
  window = QStackedWidget()
  window.addWidget(SecondWindow)
  window.setFixedWidth(400)
  window.setFixedHeight(250)

  label = QLabel("Add a book!")
  label.setFont(QFont("Courier New", 23))
  layout = QVBoxLayout()

  button1 = QPushButton('Add')
  button2 = QPushButton('Change')

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

  layout.addWidget(label)
  layout.addWidget(e1)
  layout.addWidget(e2)
  layout.addWidget(e3)
  layout.addWidget(button1)
  layout.addWidget(button2)

  
  button1.clicked.connect(lambda: upload(e1, e1.text(), e2, e2.text(), e3, e3.text()))
  button2.clicked.connect(lambda : window.setCurrentIndex(window.currentIndex()+1))


  window.setLayout(layout)
  window.show()
  app.exec()
"""

# Starts running the program
if __name__=='__main__':
  app = QApplication(sys.argv)
  MainWindow()
