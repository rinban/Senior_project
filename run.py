# Import methods
from flask import Flask, request, send_file, render_template, redirect, url_for
from cnvd_site import annotation
from fpdf import FPDF 

# save instance of flask class. 
# _name_ is the name of the application’s module
# save it in variable for easiest accessbility 
app = Flask(__name__)

# Specify the accepted type of file 
app.config['UPLOAD_EXTENSIONS'] = ['CSV']


@app.route('/')
def start ():
    return render_template('index.html')

@app.route('/', methods=['GET','POST'])
def tool_handel ():

    #  if user clicked submit (it means mostly he uploaded a file)
    if request.method == 'POST':

        # if he clicked Start Model button
        if 'start' in request.form:

            if request.files:
                # Get the user uploaded file from input button
                myfile = request.files["file_inp"] 
                cross_mark = u'\u274C'

                # There is no file
                if myfile.filename == '':
                    wrong_message='Upload CSV File'
                    # Print wrong message
                    return render_template('index.html',cross_mark= cross_mark,
                    wrong_message = wrong_message)

                # file not in right extension
                if not allowed_exten (myfile.filename): # !false -> true
                    wrong_message ='Upload CSV File Only'
                    # Print wrong message
                    return render_template('index.html',cross_mark= cross_mark, 
                    wrong_message=wrong_message)

                # method for feature extraction and model
                output_file = annotation(myfile)

                # print output
                print_pdf(output_file)

                check_mark =  u'\u2713'
                successful = 'Successful'
            # Print successful message
            return render_template('index.html', check_mark= check_mark, successful= successful)

        # if he clicked Download button
        elif 'download' in request.form :

                out = "tutorials1.pdf"
                return send_file(out,as_attachment=True)

    return redirect (url_for('start'))

# validate uploaded file
def allowed_exten (thefilename):

    if not '.' in thefilename:
        return False

    # take just extention from the name of file
    exten = thefilename.rsplit('.',1)[1]

    # if accepted return true, else return false
    if exten.upper() in app.config['UPLOAD_EXTENSIONS']:
        return True
    else:
        return False

# create pdf report
def print_pdf(output_file):
    # save FPDF() class into a variable pdf 
    pdf = FPDF()
    
    # Add a page 
    pdf.add_page('P') 

    # set style and size of font  
    pdf.set_font("Arial", size = 11) 
    pdf.cell(200, 10, txt = '--------------------------------- CNVD Report ---------------------------------',
            ln = 2, align = 'C') 

    pdf.set_font("Arial", size = 7) 
  
    # Print statement in the file
    for result in output_file:
        for i in result:

            pdf.cell(200, 6, txt = str(i),
            ln = 2, align = 'L') 
             
    pdf.set_font("Arial", size = 11) 
    pdf.cell(200, 10, txt = '--------------------------------- The End ---------------------------------',
            ln = 2, align = 'C') 

    # save the pdf with name .pdf 
    pdf.output("tutorials1.pdf")


# Make server still running while changing code
if __name__ == '__main__':
    app.run(debug=True)


