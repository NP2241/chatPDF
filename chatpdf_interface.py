import requests

API_KEY = 'sec_izbePdE9DuRdNE5jOGffw3xE1T8Jxxc2'

def add_pdf_via_file_upload(file_path):
    """
    Adds a PDF file via file upload

    Parameters:
    file_path (str): The local path to the PDF file to be uploaded.

    Returns:
    str or None: The source ID of the uploaded PDF if successful, None otherwise.
    """
    try:
        endpoint = 'https://api.chatpdf.com/v1/sources/add-file'
        headers = {'x-api-key': API_KEY}
        files = {'file': ('file', open(file_path, 'rb'), 'application/octet-stream')}

        response = requests.post(endpoint, headers=headers, files=files)

        if response.status_code == 200:
            print("PDF added successfully.")
            return response.json()['sourceId']
        else:
            print(f"Failed to add PDF via file upload. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def send_chat_message(source_id, messages):
    """
    Sends a chat message to a PDF

    Parameters:
    source_id (str): The source ID of the PDF.
    messages (list of str): List of messages to be sent.

    Returns:
    str or None: The content of the chat message if successful, None otherwise.
    """
    endpoint = 'https://api.chatpdf.com/v1/chats/message'
    headers = {'x-api-key': API_KEY, 'Content-Type': 'application/json'}
    data = {'sourceId': source_id, 'messages': messages}
    response = requests.post(endpoint, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['content']
    else:
        return None

def delete_pdf(source_id):
    """
    Deletes a PDF

    Parameters:
    source_id (str): The source ID of the PDF to be deleted.

    Returns:
    bool: True if deletion is successful, False otherwise.
    """
    endpoint = 'https://api.chatpdf.com/v1/sources/delete'
    headers = {'x-api-key': API_KEY, 'Content-Type': 'application/json'}
    data = {'sources': [source_id]}
    response = requests.post(endpoint, headers=headers, json=data)
    if response.status_code == 200:
        return True
    else:
        return False

def test_add_pdf_via_file_upload():
    """
    Test function to add a PDF via file upload.

    Prints success message along with the source ID if upload is successful.
    """
    file_path = '/Users/neilpendyala/Downloads/ch1-5,17-18_v1-compressed.pdf'
    source_id = add_pdf_via_file_upload(file_path)
    if source_id:
        print('PDF added successfully. Source ID:', source_id)
    else:
        print('Failed to add PDF via file upload.')

# Run the test
if __name__ == "__main__":
    test_add_pdf_via_file_upload()
