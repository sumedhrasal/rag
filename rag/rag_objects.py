import json


class CompanyObject:
    def __init__(self, name, address):
        self.name = name
        self.address = address

    def to_json_string(self):
        # Convert the object to a JSON-formatted string
        return json.dumps(self.__dict__)


class CompanyLeadership:
    def __init__(self, ceo, cfo, cto, coo):
        self.ceo = ceo
        self.cfo = cfo
        self.coo = coo
        self.cto = cto

    def to_json_string(self):
        # Convert the object to a JSON-formatted string
        return json.dumps(self.__dict__)


class PEST:
    def __init__(self, economical, political, social, technological) -> None:
        self.economical = economical
        self.political = political
        self.social = social
        self.technological = technological

    def to_json_string(self):
        # Convert the object to a JSON-formatted string
        return json.dumps(self.__dict__)


class StructuredResponse:
    def __init__(self, 
                 name, address, industry, description, 
                 competitors, ceo, cfo, cto, coo, finanicals,
                 economical, political, social, technological):
        self.company = CompanyObject(name, address)
        self.industry = industry
        self.description = description
        self.competitors = competitors
        self.leadership = CompanyLeadership(ceo, cfo, cto, coo)
        self.finanicals = finanicals
        self.pest = PEST(economical, political, social, technological)

    def to_json_string(self):
        # Convert the object to a JSON-formatted string
        return json.dumps(self.__dict__)

