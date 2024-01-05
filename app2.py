from flask import Flask, request, jsonify
from rag import data, service
import json


app = Flask(__name__)


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


def get_response(request_data):
    company_name = str(request_data['company']).lower().replace(" ", "")
    structured_data = data.get_structured_data_by_company(company_name)
    unstructured_data = data.get_unstructured_data_by_company(company_name)
    return service.conflate(company_name, structured_data, unstructured_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', debug=True)
