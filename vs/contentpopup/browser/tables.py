#####################################################################
# vs.contentpopup
# (C) 2011, Veit Schiele Communications GmbH
#####################################################################

import re
from Products.Five.browser import BrowserView
from Products.CMFCore.interfaces import ISiteRoot
from Products.ATContentTypes.interfaces import IATFolder
from Products.CMFCore.utils import getToolByName
import lxml.html

def extract_table(html, id):
    if not isinstance(html, unicode):
        html = unicode(html, 'utf-8')
    root = lxml.html.fromstring(html)
    nodes = root.xpath('//table[@id="%s"]' % id)
    if len(nodes) == 1:
        return lxml.html.tostring(nodes[0], encoding=unicode)
    return ''

class TableHandler(BrowserView):
    """ Table folding - return a rendered HTML table by its ID """

    def show_table(self, uid, id):
        """ Return the HTML code of a table given by its id """

        refcat = getToolByName(self.context, 'reference_catalog')
        obj = refcat.lookupObject(uid)

        if IATFolder.providedBy(obj) or ISiteRoot.providedBy(obj):
            default_page = obj.getDefaultPage()
            context = obj[default_page]
            text_field = context.getField('text')
        else:
            text_field = obj.getField('text')
            context = obj

        if text_field:
            self.request.response.setHeader('content-type', 'text/html;charset=utf-8')
            return extract_table(text_field.get(context), id)
