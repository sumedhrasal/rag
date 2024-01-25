from flask import Flask, request, jsonify
from flask_cors import CORS 
from rag import data, service, logger, util
import concurrent.futures
import tempfile


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
logger.setup_logger()
executor = concurrent.futures.ProcessPoolExecutor(max_workers=1)


@app.route('/company/batch', methods=['POST'])
def batch_mode():
    # Get the JSON data from the request
    request_data = request.get_json()
    response = get_response(request_data)
    return jsonify({"response":response})


@app.route('/company/live', methods=['POST'])
def live_mode():
    request_data = request.get_json()
    response = get_response(request_data)
    return jsonify({"response":response})


@app.route('/company/query', methods=['POST'])
def query():
    # Get the JSON data from the request
    request_data = request.get_json()
    company_name = request_data['company']
    company_url = request_data['url']
    response = service.fetch_vc_information(company_name, company_url, util.generate_id())
    return jsonify(response)


@app.route('/result/<int:request_id>')
def result(request_id):
    return jsonify({"results":[request_id]})


@app.route('/upload', methods=['POST'])
def upload_pdf():
    try:
        # Check if the POST request contains a file
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})

        file = request.files['file']

        # Check if the file is empty
        if file.filename == '':
            return jsonify({'error': 'No selected file'})

        # Check if the file is a PDF
        if not file.filename.endswith('.pdf'):
            return jsonify({'error': 'Invalid file type. Please upload a PDF file'})

        # Create a temporary file to store the PDF content
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_pdf:
            temp_pdf.write(file.read())
            temp_pdf_path = temp_pdf.name

        name_url_dict = service.extract_http_links_from_pdf(temp_pdf_path)

        # Remove the temporary file
        temp_pdf.close()

        return jsonify(name_url_dict)
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'})


def get_response(request_data):
    company_name = str(request_data['company']).lower().replace(" ", "")
    structured_data = data.get_structured_data_by_company(company_name)
    unstructured_data = data.get_unstructured_data_by_company(company_name)
    return service.conflate(company_name, structured_data, unstructured_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', debug=True)
