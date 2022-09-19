from mdutils.mdutils import MdUtils
from mdutils import Html
from explore import *

class MdReport:
    def __init__(self, data):
        self.data = data

    def createMd(self):
        mdFile = MdUtils(file_name='Report', title='Attack Report')

        mdFile.new_header(level=1, title='Overview')
        mdFile.new_paragraph("This report serves as a ...")

        mdFile.new_header(level=1, title="Data")
        mdFile.new_paragraph("my IP:" + self.data['myIP'])
        mdFile.new_paragraph("Explored host:" + self.data['IP'])
        mdFile.new_paragraph("Service:" + str(self.data['Service']))
        mdFile.new_paragraph("OS:" + str(self.data['OS']))
        mdFile.new_paragraph("Port:" + str(self.data['Port']))
        mdFile.new_paragraph("Apache:" + str(self.data['Apache']))

        mdFile.create_md_file()