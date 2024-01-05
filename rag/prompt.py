

def get_company_prompt(company_name):
    obj = """
    Respond back your answer as a JSON object {        
        "Name": "", 
        "Address": "",
        "Industry": "", 
        "Description": "", 
        "CEO": "",
        "CTO": "",
        "CFO": "",
        "COO": "",
        "Competitors": []
    }
    """
    prompt = f"""
    "Utilize the local data sources at your disposal, which contain information about {company_name}. 
    Examine the JSON object and furnish as much relevant information as possible in under 20 words. 
    In cases where the local data is insufficient to populate all the keys of the JSON object, 
    draw upon your knowledge to address those queries. 
    Your goal is to aid the user in making well-informed decisions regarding the company under consideration."
    """ + obj
    return prompt


def get_company_financial_prompt(company_name):
    prompt = f"""
    Utilize the local data sources at your disposal, which contain information about {company_name}. 
    Examine the JSON object and furnish as much relevant information as possible in under 20 words. 
    In cases where the local data is insufficient to populate all the keys of the JSON object, 
    draw upon your knowledge to address those queries. 
    Your goal is to aid the user in making well-informed decisions regarding the company under consideration.
    Respond back your answer as a JSON object using following fields
    "Financials": "", # Does the company generate any revenue or has it raised any money?
    "Value Proposition": "", # A short description about the company's value proposition
    """
    return prompt


def get_industry_pest_prompt(industry):
    # prompt = f"""
    # Utilize the local data sources at your disposal, which contain information about {industry}. 
    # Examine the JSON object and furnish as much relevant information as possible
    # In cases where the local data is insufficient to populate all the keys of the JSON object, 
    # draw upon your knowledge to address those queries. 
    # Respond back your answer as a JSON object 
    # "Political": Do a political analysis on the {industry} industry in under 20 words. 
    # "Economicial": Do an economical analysis on the {industry} industry in under 20 words. 
    # "Social": Do a social analysis on the {industry} industry in under 20 words. 
    # "Technological": Do a technological analysis on the {industry} industry in under 20 words. 
    # """
    prompt = f"""
    Perform a PEST analysis for the {industry} industry.
    Respond back with a valid JSON schema
    """
    return prompt
