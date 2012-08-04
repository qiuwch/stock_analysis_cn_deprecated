class BaseSource():
    def __init__(self):
        pass

    def Query(self, queryStr):
        return queryStr

class CompanyListSource(BaseSource):
    def __init__(self, companys):
        BaseSource.__init__(self)
        self.companys = companys

    def Query(self, queryStr):
        if queryStr == '':
            return self.companys
        
        queryResult = []
        for c in self.companys:
            # print c.fullName
            if c.fullName.find(queryStr) != -1:
                queryResult.append(c)
        print queryStr

        return queryResult
