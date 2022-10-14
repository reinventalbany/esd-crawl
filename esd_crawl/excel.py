from openpyxl import Workbook
from openpyxl.drawing.image import Image

wb = Workbook()
ws = wb.active
ws["A1"] = "You should see three logos below"

# create an image
img = Image("tables/0a047a178e1ccfb1da6d98d36c8cf8ff.png")

# add to worksheet and anchor next to cells
ws.add_image(img, "A1")
wb.save("logo.xlsx")
