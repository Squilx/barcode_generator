from io import BytesIO
from fpdf import FPDF
from barcode import Code128
from barcode.writer import SVGWriter

# Make a list of barcodes to pass to the pdf creator function create_pdf()
def create_codes_list(aisle, start_bay, end_bay, start_shelf, end_shelf, start_location, end_location):
    list_of_codes = []
    for x in range(start_bay, end_bay + 1):
        for y in range(start_shelf, end_shelf + 1):
            for z in range(start_location, end_location + 1):
                list_of_codes.append(f"{aisle}-{str(x).zfill(2)}-{str(y).zfill(2)}-{str(z).zfill(2)}")
    return list_of_codes

# Generate a Code128 Barcode as SVG:
def create_pdf(codes_list):
    pdf = FPDF(orientation="P", unit="mm", format="A4")

    # Create a new PDF document
    pdf = FPDF()
    pdf.add_page()

    # Set the starting position and size of the barcode in the PDF **MUST MATCH RESET (BELOW)**
    x = 20
    y = 20
    w = 57
    h = 20

    for codes in codes_list:
        #Adjust the text position for if barcode is in "AAA" or "AA" format
        if len(codes) > 11:
            x_adder = 4
        else:
            x_adder = 7

        #Create a new page when you get to the end of the current page
        if y > 240:
            pdf.add_page()
            #Reset the starting position **MUST MATCH ORIGINAL**
            x = 20
            y = 20
            w = 57
            h = 20

        #Create an image of the barcode and insert into position
        svg_img_bytes = BytesIO()
        Code128(codes, writer=SVGWriter()).write(svg_img_bytes)
        pdf.image(svg_img_bytes, x=x, y=y, w=w, h=h)

        #Insert text representation of the barcode in correct position
        pdf.set_font("helvetica", "B", 22)
        pdf.text(x=x+x_adder, y=y+28, txt=codes)

        # draw the rectangles relative to the barcode
        pdf.set_line_width(0.5)
        pdf.set_draw_color(1)
        pdf.rect(x=x, y=y-2, w=w, h=h)
        pdf.rect(x=x, y=y+18, w=w, h=h-5)

        #set up position for the next barcode
        if x > 105:
            x = 20
            y += 35
        else:
            x += 57

    # Output a PDF file
    pdf.output('barcode_labels.pdf')
