# from flask import Flask, render_template, request
# import os
# import tempfile
# import streamlit as st
# from Ecg import ECG

# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

# from flask import redirect

# @app.route('/', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         # Handle file upload
#         uploaded_file = request.files['file']
#         if uploaded_file.filename != '':
#             # Save the uploaded file
#             file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
#             uploaded_file.save(file_path)

#             # Process the uploaded file with ECG analysis
#             result = process_ecg(file_path)

#             # Render results and option to upload another file
#             return render_template('result.html', result=result, filename=uploaded_file.filename)

#     # Render file upload form
#     return render_template('upload.html')

# @app.route('/remove_and_upload_another/<filename>', methods=['GET'])
# def remove_and_upload_another(filename):
#     # Remove the uploaded file
#     file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#     if os.path.exists(file_path):
#         os.remove(file_path)

#     # Redirect back to the upload page
#     return redirect('/')

# def process_ecg(file_path):
#     # Initialize ECG object
#     ecg = ECG()

#     # Perform ECG analysis on the uploaded file
#     ecg_user_image_read = ecg.getImage(file_path)
#     ecg_user_gray_image_read = ecg.GrayImgae(ecg_user_image_read)
#     dividing_leads = ecg.DividingLeads(ecg_user_image_read)
#     ecg_preprocessed_leads = ecg.PreprocessingLeads(dividing_leads)
#     ec_signal_extraction = ecg.SignalExtraction_Scaling(dividing_leads)
#     ecg_1dsignal = ecg.CombineConvert1Dsignal()
#     ecg_final = ecg.DimensionalReduciton(ecg_1dsignal)
#     ecg_model = ecg.ModelLoad_predict(ecg_final)

#     return ecg_model

# @app.route('/remove_file/<filename>', methods=['GET'])
# def remove_file(filename):
#     # Remove the uploaded file
#     file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#     if os.path.exists(file_path):
#         os.remove(file_path)

#     # Redirect back to the upload page
#     return redirect('/')


# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template, request, redirect
import os
import tempfile
from Ecg import ECG

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    uploaded_filename = None

    if request.method == 'POST':
        # Handle file upload
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            # Save the uploaded file
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            uploaded_file.save(file_path)
            uploaded_filename = uploaded_file.filename  # Store the filename

            # Process the uploaded file with ECG analysis
            result = process_ecg(file_path)

            # Render results and option to upload another file
            return render_template('result.html', result=result, filename=uploaded_filename)

    # Pass uploaded filename to template for display
    return render_template('upload.html', uploaded_filename=uploaded_filename)

@app.route('/uploads/<filename>')
def show_uploaded_file(filename):
    # Construct the path to the uploaded file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    # Check if the file exists
    if os.path.exists(file_path):
        # Render the uploads.html page with the filename
        return render_template('uploads.html', filename=filename)

    # Handle file not found (optional)
    return render_template('file_not_found.html')

@app.route('/remove_and_upload_another/<filename>', methods=['GET'])
def remove_and_upload_another(filename):
    # Remove the uploaded file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)

    # Redirect back to the upload page
    return redirect('/')

def process_ecg(file_path):
    # Initialize ECG object
    ecg = ECG()

    # Perform ECG analysis on the uploaded file
    ecg_user_image_read = ecg.getImage(file_path)
    ecg_user_gray_image_read = ecg.GrayImgae(ecg_user_image_read)
    dividing_leads = ecg.DividingLeads(ecg_user_image_read)
    ecg_preprocessed_leads = ecg.PreprocessingLeads(dividing_leads)
    ec_signal_extraction = ecg.SignalExtraction_Scaling(dividing_leads)
    ecg_1dsignal = ecg.CombineConvert1Dsignal()
    ecg_final = ecg.DimensionalReduciton(ecg_1dsignal)
    ecg_model = ecg.ModelLoad_predict(ecg_final)

    return ecg_model

@app.route('/remove_file/<filename>', methods=['GET'])
def remove_file(filename):
    # Remove the uploaded file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)

    # Redirect back to the upload page
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
