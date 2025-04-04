import os
from flask import Flask, render_template, request, redirect, url_for, abort, \
    send_from_directory
from werkzeug.utils import secure_filename
import datetime
import pdfutil

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif','.pdf']
app.config['UPLOAD_PATH'] = 'uploads'

DELETE_AFTER=10
    
startTimer=True
@app.route('/stopBgThread/stop')
def stopBgThread():
    #timer_runs.clear()
    global startTimer
    startTimer=False
    return "Background thread will be stopped by now.."

@app.route('/')
def index():
    files = []
    return render_template('index.html', files=files)

@app.route('/', methods=['POST'])
def upload_files():
    requestid = request.form.get('requestid')
    parts = request.form.get('parts','0')
    if not parts or parts == '':
        parts = 0 
    else:
        parts = int(parts)
    pdf_operation = request.form.get('pdf_operation')
    uploaded_files = request.files.getlist('file')
    if uploaded_files:
        if pdf_operation == 'split':
            print('file uploaded '+str(uploaded_files[0]))
            print('files for splitting '+str(uploaded_files[0].filename))
        elif pdf_operation == 'merge':
            print('file uploaded '+str(uploaded_files))
            for file in uploaded_files:
                print('files for merging '+str(file.filename))
    else:
        return 'No Files Uploaded'

    
    if not requestid:
        requestid = datetime.datetime.now().strftime('%d%m%Y%H%M%S%f')
    #uploaded_file = request.files['file']
    for file in uploaded_files:
        filename = secure_filename(file.filename)
        if filename != '':
            os.makedirs(os.path.join(app.config['UPLOAD_PATH'],requestid),exist_ok=True)
            file.save(os.path.join(app.config['UPLOAD_PATH'],requestid, filename))

    if pdf_operation == 'split':
        pdfutil.splitPdfs(os.path.join(app.config['UPLOAD_PATH'],requestid, filename),parts=parts,pdfpath=os.path.join(app.config['UPLOAD_PATH'],requestid))
    else:
        pdfutil.mergePdfs(os.path.join(app.config['UPLOAD_PATH'],requestid))
    if pdf_operation == 'split':
        return redirect(url_for('showResults',pdf_operation=pdf_operation,requestid=requestid,filename=filename))
    else:
        return redirect(url_for('showResults',pdf_operation=pdf_operation,requestid=requestid,filename='merged-doc.pdf'))



@app.route('/<requestid>/<pdf_operation>/<filename>')
def showResults(requestid,pdf_operation,filename):
    files = []
    try:
        files = os.listdir(os.path.join(app.config['UPLOAD_PATH'],requestid))
        fileparts = [ f for f in files if f != filename ]
    except Exception as e:
        pass
    return render_template('index.html', pdf_operation=pdf_operation,origFile=filename,files=fileparts,requestid=requestid)

@app.route('/uploads/<requestid>/<filename>')
def upload(requestid,filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_PATH'],requestid), filename)

import threading
import time

#def deleteOldFiles(timer_runs):
def deleteOldFiles():
    #while timer_runs.is_set():
    while startTimer:
        print('Deleting older files')
        for (root,dirs,files) in os.walk(app.config['UPLOAD_PATH'], topdown=True): 
            for f in files: 
                # temp variable to store path of the file  
                file_path = os.path.join(root,f) 
                # get the timestamp, when the file was modified  
                timestamp_of_file_modified = os.path.getmtime(file_path) 
                # convert timestamp to datetime 
                modification_date = datetime.datetime.fromtimestamp(timestamp_of_file_modified) 
                # find the number of days when the file was modified 
                delta = (datetime.datetime.now() - modification_date)
                min_passed = round(delta.total_seconds() / 60)
                print('file_path '+str(file_path)+' mod ts '+str(timestamp_of_file_modified)+' mod date '+str(modification_date)+' delta '+str(delta)+' min_passed '+str(min_passed)) 
                
                if min_passed > DELETE_AFTER: 
                    # remove file  
                    os.remove(file_path) 
                    print(f" Delete : {f}")
        time.sleep(15)         
    print('Background thread is now stopped..')

def scheduleDelFiles():
    t = threading.Thread(target=deleteOldFiles)#, args=(timer_runs,))
    t.start()
    # Wait 10 seconds and then stop the timer.
    #time.sleep(10)
    print("The timer has been started!") 

#timer_runs = threading.Event()
#timer_runs.set()

scheduleDelFiles()

print('All app code inited')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)