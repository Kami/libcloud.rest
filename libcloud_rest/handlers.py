from twisted.web import resource
from twisted.web.resource import Resource

class Root(resource.Resource):
    def getChild(self, name, target):
        print target.__dict__

        return MainDispatcher()

class RegexDispatcher(Resource):
    def render_GET(self, request):
        return ''
