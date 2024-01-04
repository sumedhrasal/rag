

def get_company_prompt(company_name):
    obj = """
    Respond back your answer as a JSON object {
        "Company": {
            "Name": "", 
            "Address": ""
        },
        "Industry": "", 
        "Description": "", 
        "Leadership": {
            "CEO": "",
            "CTO": "",
            "CFO": "",
            "COO": ""
        },
        "Competitors": []
    }
    """
    prompt = f"""
    You have access to local data sources containing information about {company_name}. 
    Given the questions it is your responsibility to retrieve data from the local store 
    and provide the best possible answers. Your objective is to assist the user in making informed decisions 
    about the company they are inquiring about. 
    """ + obj
    return prompt

