from fpdf import FPDF
import os

import glob

class Report:

    # Creating pdf object
    pdf = None
    # inx declaration
    inx = 60

    fonts = {"header":['helvetica',20],"summary":['Arial',13]}

    def __init__(self):
        self.remove_cache_files()
        # format ('A3','A4','Letter','Legal')
        self.pdf = FPDF('P','mm','A4')

        # Adding a page to the pdf file
        self.pdf.add_page()

        # Setting up font
        self.pdf.set_font('helvetica','',12)

    def header(self):

        # Arial bold 15
        self.pdf.set_font(self.fonts['header'][0], 'B',self.fonts['header'][1] )

        # Move to the right
        self.pdf.cell(46)

        # Title
        self.pdf.cell(90, 20, 'SUMMARY REPORT', 1, 0, 'C')

        self.pdf.line(0, 40,220,40)

        # Line break
        self.pdf.ln(40)

    def insert_text(self,user_details):
        # Add Text
        # w = width
        # h = height

        # Adding Title
        # for key,value

        inx  = self.inx
        for key,value in user_details.items():
            self.pdf.cell(0,inx,key + " : " + value)
            self.pdf.ln(2)
            inx+=20

        self.pdf.ln(1)
        inx+=10
        self.inx = inx

        
    def generate_pdf_report(self,summaries,titles):

        # Initiate Header
        self.header()
        for inx in range(len(summaries)):
            # Setting up Personal Details header
    
            # Arial bold 15
            self.pdf.set_font(self.fonts['header'][0], 'B',self.fonts['header'][1] )

            self.pdf.cell(0,inx,titles[inx])
            self.pdf.ln(4)

            self.pdf.set_font(self.fonts['summary'][0],'',self.fonts['summary'][1] )

            self.pdf.multi_cell(200,5,summaries[inx])
            self.pdf.ln(10)

        self.pdf.output('./cache/report.pdf')

    def refresh(self):
        # format ('A3','A4','Letter','Legal')
        self.pdf = FPDF('P','mm','A4')

        # Adding a page to the pdf file
        self.pdf.add_page()

        # Setting up font
        self.pdf.set_font('helvetica','',16)
        

    def remove_cache_files(self):
        files = glob.glob('./cache/*')
        for f in files:
            os.remove(f)
