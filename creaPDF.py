# header_footer.py
from fpdf import FPDF
from getSNMP import  consultaSNMP


class CustomPDF(FPDF):

    def header(self):
        # Set up a logo
        self.image('linux11.png', 10, 8, 33)
        self.set_font('Arial', 'B', 15)

        # Add an address
        self.cell(100)
        self.cell(0, 5, 'Reporte de agente', ln=1)
        self.cell(100)
        self.cell(0, 5, 'Info1', ln=1)
        self.cell(100)
        self.cell(0, 5, 'Info2', ln=1)

        # Line break
        self.ln(20)

    def footer(self):
        self.set_y(-10)

        self.set_font('Arial', 'I', 8)

        # Add a page number
        page = 'Page ' + str(self.page_no()) + '/{nb}'
        self.cell(0, 10, page, 0, 0, 'C')


def create_pdf(pdf_path):
    pdf = CustomPDF()
    # Create the special value {nb}
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Times', '', 12)
    line_no = 1
    for i in range(5):
        pdf.cell(0, 10, txt="Line #{}".format(line_no), ln=1)
        line_no += 1
    pdf.output(pdf_path)


if __name__ == '__main__':
    create_pdf('ejemplo.pdf')