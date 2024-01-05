import json


class CompanyObject:
    def __init__(self, name, address):
        self.name = name
        self.address = address

    def to_json_string(self):
        # Convert the object to a JSON-formatted string
        return json.dumps(self.__dict__)

    def to_dict(self):
        """
        Convert the object to a dictionary.
        """
        return {
            'Name': self.name,
            'Address': self.address
        }

class CompanyLeadership:
    def __init__(self, ceo, cfo, cto, coo):
        self.ceo = ceo
        self.cfo = cfo
        self.coo = coo
        self.cto = cto

    def to_json_string(self):
        # Convert the object to a JSON-formatted string
        return json.dumps(self.__dict__)

    def to_dict(self):
        """
        Convert the object to a dictionary.
        """
        return {
            'CEO': self.ceo,
            'CFO': self.cfo,
            'CTO': self.cto,
            'COO': self.coo
        }

class PEST:
    def __init__(self, economical, political, social, technological) -> None:
        self.economical = economical
        self.political = political
        self.social = social
        self.technological = technological

    def to_json_string(self):
        # Convert the object to a JSON-formatted string
        return json.dumps(self.__dict__)

    def to_dict(self):
        """
        Convert the object to a dictionary.
        """
        return {
            'Political': self.political,
            'Economical': self.economical,
            'Social': self.social,
            'Technological': self.technological
        }

class StructuredResponse:
    def __init__(self, 
                 name, address, industry, description, 
                 competitors, ceo, cfo, cto, coo, financials,
                 economical, political, social, technological, value_proposition):
        self.company = CompanyObject(name, address)
        self.industry = industry
        self.description = description
        self.competitors = competitors
        self.leadership = CompanyLeadership(ceo, cfo, cto, coo)
        self.financials = financials
        self.pest = PEST(economical, political, social, technological)
        self.value_proposition = value_proposition

    def to_json_string(self):
        # Convert the object to a JSON-formatted string
        return json.dumps(self.__dict__)

    def to_dict(self):
        """
        Convert the object to a dictionary.
        """
        return {
            'Company': self.company,
            'Industry': self.industry,
            'Description': self.description,
            'Competitors': self.competitors,
            'Leadership': self.leadership,
            'Financials': self.financials,
            'PEST': self.pest,
            'Value Proposition': self.value_proposition
        }
