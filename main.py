from barcode_pdf import create_codes_list, create_pdf

aisle = "BDB"
start_bay = 1
end_bay = 1
start_shelf = 1
end_shelf = 1
start_location = 1
end_location = 2

codes_list = create_codes_list(aisle, start_bay, end_bay, start_shelf, end_shelf, start_location, end_location)
create_pdf(codes_list)
