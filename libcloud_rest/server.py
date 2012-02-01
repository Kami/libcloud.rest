import sys
import logging

from twisted.internet import reactor
from twisted.web import server, resource

from libcloud_rest.utils import get_and_setup_logger
from libcloud_rest.handlers import Root

if __name__ == '__main__':
    logger = get_and_setup_logger()
    logger.info('Starting Libcloud REST server')
    factory = server.Site(Root())
    reactor.listenTCP(8000, factory)
    reactor.run()
