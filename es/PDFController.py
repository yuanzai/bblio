from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from cStringIO import StringIO

class PDFController(object):
    def __init__(self):
        pass

    def get_string(self, pdf_path):
        fp = open(pdf_path, 'rb')
        parser = PDFParser(fp)
        document = PDFDocument(parser)
        if not document.is_extractable:
            raise PDFTextExtractionNotAllowed

        rsrcmgr = PDFResourceManager()
        outfp = StringIO()
        
        laparams = LAParams()
        device = TextConverter(rsrcmgr, outfp, codec='utf-8', laparams=laparams)

        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.get_pages(fp, set()):
            interpreter.process_page(page)
        fp.close()
        device.close()
        str = outfp.getvalue()
        outfp.close()
        return str
