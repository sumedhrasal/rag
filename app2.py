from flask import Flask, request, jsonify
from rag import data, service, logger, util
import json
import concurrent.futures


app = Flask(__name__)
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
    company_name = str(request_data['company']).lower().replace(" ", "")
    company_url = str(request_data['url']).lower().replace(" ", "")
    # Generate a unique ID
    request_id = util.generate_id()
    return jsonify({"id":request_id})


@app.route('/result/<int:request_id>')
def result(request_id):
    return jsonify({"id":request_id})


def get_response(request_data):
    company_name = str(request_data['company']).lower().replace(" ", "")
    structured_data = data.get_structured_data_by_company(company_name)
    unstructured_data = data.get_unstructured_data_by_company(company_name)
    return service.conflate(company_name, structured_data, unstructured_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', debug=True)
