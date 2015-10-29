import re
from core.handler_baseclass import Handler
from errors.timegateerrors import HandlerError


__author__ = 'Harihar Shankar'


ACCEPTABLE_RESOURCE = "This TimeGate understands W3C specification uri of the format: %s" % "http://www.w3.org/TR/<spec_name>"
APIKEY = "2zrj0x1tom4gkkgc4w804o08gs8gs8o"


class W3cHandler(Handler):

    def __init__(self):
        Handler.__init__(self)

        # Local fields
        self.api_url = 'https://api-test.w3.org/specifications/%s/versions?_format=json&apikey=%s&embed=1'

        self.re_spec_name = re.compile("https?:\/\/(www.)?w3.org\/TR\/(.*)", re.IGNORECASE)

    def get_all_mementos(self, uri):

        match_spec_name = self.re_spec_name.match(uri)
        if not bool(match_spec_name):
            raise HandlerError("Unknown W3C specification uri. \n"
                               + ACCEPTABLE_RESOURCE, 404)

        spec_name = match_spec_name.groups()[1]
    
        api_response = self.request(self.api_url % (spec_name, APIKEY))

        if not api_response.status_code == 200:
            raise HandlerError("No versions were found for the requested specification with shortname: %s" % spec_name, 404)
        
        json_response = {}
        try:
            json_response = api_response.json()
            #for versions in json_response.get("_embedded").get("versions"):
            #    spec_versions.append((versions.get("uri"), versions.get("date")))
        except:
            raise HandlerError("The W3C API returned an unknown response.", 502)
        
        if not json_response.get("_embedded") and json_response.get("_embedded").get("versions"):
            raise HandlerError("The W3C API returned an unknown response.", 502)

        versions = map(
                lambda version: (version.get("uri"), version.get("date")),
                json_response.get("_embedded").get("version-history")
                )
        return sorted(versions, lambda version: version[1])
