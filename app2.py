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
    company_name = request_data['company']
    company_url = request_data['url']
    response = service.fetch_vc_information(company_name, company_url, util.generate_id())
    return jsonify(response)


@app.route('/result/<int:request_id>')
def result(request_id):
    return jsonify({"results":[request_id]})


def get_response(request_data):
    company_name = str(request_data['company']).lower().replace(" ", "")
    structured_data = data.get_structured_data_by_company(company_name)
    unstructured_data = data.get_unstructured_data_by_company(company_name)
    return service.conflate(company_name, structured_data, unstructured_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', debug=True)
