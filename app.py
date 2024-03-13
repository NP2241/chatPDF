from flask import Flask, render_template, request, redirect, url_for
import os
from chatpdf_interface import add_pdf_via_file_upload, send_chat_message, delete_pdf

app = Flask(__name__)

@app.route('/')
def index():
    """
    Renders the index page with optional source ID and file path.

    Returns:
    str: Rendered HTML page.
    """
    source_id = request.args.get('source_id')
    file_path = request.args.get('file_path')
    return render_template('index.html', source_id=source_id, file_path=file_path)

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Handles file upload and adds the PDF

    Returns:
    str: Redirects to the 'ask' route with source ID and file path if successful.
         Returns an error message if unsuccessful.
    """
    try:
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)

        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)

        source_id = add_pdf_via_file_upload(file_path)

        if source_id:
            os.remove(file_path)
            return redirect(url_for('ask', source_id=source_id, file_path=file_path))
        else:
            return "Failed to add PDF via file upload."
    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route('/ask/<source_id>', methods=['GET', 'POST'])
def ask(source_id):
    """
    Handles user queries

    Parameters:
    source_id (str): The source ID of the PDF.

    Returns:
    str: Rendered HTML page with source ID, file path, and answer if a POST request.
         Otherwise, just renders the template with source ID and file path.
    """
    file_path = request.args.get('file_path')  # Retrieve file_path from URL parameters
    if request.method == 'POST':
        question = request.form['question']
        answer = send_chat_message(source_id, [{'role': 'user', 'content': question}])
        return render_template('index.html', source_id=source_id, file_path=file_path, answer=answer)

    # If it's a GET request, just render the template with the source_id and file_path
    return render_template('index.html', source_id=source_id, file_path=file_path)

if __name__ == '__main__':
    app.run(debug=True)
