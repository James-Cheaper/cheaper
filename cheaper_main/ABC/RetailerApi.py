from abc import ABC,abstractmethod

class RetailerApi(ABC):

    @abstractmethod
    def retrieve_access_token(self) -> str:
        """ retrieves the user access token for sandbox environment it's a long line
            of text, numbers, symbols
        """
        pass

    @abstractmethod
    def retrieve_response(self,httprequest:str,query:str) -> dict:
        """ retrieves a json of large data with category ids, names, parentcategorynodes """
        pass