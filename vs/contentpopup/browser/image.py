################################################################
# vs.contentpopup
# (C) 2012, Veit Schiele Communications GmbH
################################################################

from Products.Five.browser import BrowserView
from Products.ATContentTypes.interfaces import IATImage

class Image(BrowserView):

    @property
    def image(self):
        if IATImage.providedBy(self.context):
            return self.context
        return self.context.getField('image')

    def download(self):
        image = self.context.getField('image')
        img_data = str(image.get(self.context).data)
        mt = image.getContentType(self.context)
        self.request.response.setHeader('content-type', mt)
        self.request.response.setHeader('content-disposition', 'attachment; filename=%s.%s' % (self.context.getId(), mt.split('/')[-1]))
        self.request.response.setHeader('content-length', len(img_data))
        self.request.response.write(img_data)

    def image_format(self, id):
        try:
            return self.image.getContentType().split('/')[1].upper()
        except:
            return self.image.getContentType(self.context).split('/')[1].upper()

    def image_size(self, id):
        try:
            return self.image.getObjSize()
        except AttributeError:
            return '%d KB' % (len(str(self.context.getImage().data)) / 1024.0)
