from flask import Flask, request, jsonify
from rag import data, service


app = Flask(__name__)


@app.route('/company/batch', methods=['POST'])
def batch_mode():
    # Get the JSON data from the request
    request_data = request.get_json()
    company_name = str(request_data['company']).lower()
    structured_data = data.get_structured_data_by_company(company_name)
    unstructured_data = data.get_unstructured_data_by_company(company_name)
    response = service.conflate(company_name, structured_data, unstructured_data)
    return jsonify({"response":response})


@app.route('/company/live', methods=['POST'])
def live_mode():
    request_data = request.get_json()
    company_name = str(request_data['company']).lower()
    structured_data = data.get_structured_data_by_company(company_name)
    unstructured_data = data.get_unstructured_data_by_company(company_name)
    response = service.conflate(company_name, structured_data, unstructured_data)
    return jsonify({"response":response})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', debug=True)
