from flask import Flask,render_template,request
import os,xlrd
app = Flask(__name__)

UPLOAD_FOLDER = 'C:\Users\Ashish.Bainade@infovisionlabs.com\Desktop\Ashish\project\exercise_1\static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def validate_file(file):
    workbook = xlrd.open_workbook(file)
    worksheet = workbook.sheet_by_index(0)
    print "value at row 8,column 2 is :{}".format(worksheet.cell(8,4).value)
    
@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'GET':
        return render_template('upload.html')
    if request.method == 'POST':
        file = request.files['file_uploaded']
        filename=file.filename
        if filename :
            file_save_path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_save_path)
            return render_template('validation.html',file=file.filename)

if __name__== "__main__":
    app.run(debug=True)
    