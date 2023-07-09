from pyzbar.pyzbar import decode
from pypdf import PdfReader
from pdf2image import convert_from_path
import imageio

def getBarcodes(path = 'examples/test_task.pdf') -> str:
    convert_from_path(path,poppler_path='D:/poppler-23.07.0/Library/bin')[0].save('examples/example.jpg', 'JPEG') # make an image from PDF
    barcodes = str(decode(imageio.v2.imread('examples/example.jpg'))).split('Decoded') # decode and split barcodes
    return barcodes

def getBarcodesPositions(barcodes:list[str]):
    """
    Use barcodes from getBarcodes()
    Return list[str] of barcode position polygons
    Example: Point(x=56, y=431), Point(x=56, y=511), Point(x=227, y=512), Point(x=227, y=430)
    """
    i = 1
    exampleBarcodesPositions = []
    while i < barcodes.__len__():
        startIndex = str(barcodes[i]).find('polygon') + 8
        endindex = str(barcodes[i]).find(', quality') - 2
        value = ''
        while startIndex < endindex:
            value += barcodes[i][startIndex+1]
            startIndex = startIndex + 1
        exampleBarcodesPositions.append(value)
        i = i + 1
    return exampleBarcodesPositions

def verifyBarcodesPositions(barcodesPositions1, barcodesPositions2):
    """
    Use data from getBarcodesPositions()
    Just assert =)
    """
    for x in barcodesPositions2:
        assert x in barcodesPositions1, 'Error while comparing barcodes positions. \n Actual:    ' + str(barcodesPositions2) + '\n Should be: ' + str(barcodesPositions1)

def getDataFromPdf(path):
    barcodes = getBarcodes()
    positions = getBarcodesPositions(barcodes)
    verifyBarcodesPositions(positions,positions)
    cleanBarcodesData = []
    i = 1
    while i < barcodes.__len__(): # fill list of data from barcodes
        startIndex = barcodes[i].find('\'')
        endindex = barcodes[i].find(',') - 2
        value = ''
        while startIndex < endindex:
            value += barcodes[i][startIndex+1]
            startIndex = startIndex + 1
        cleanBarcodesData.append(value) # 1, tst
        i = i + 1
    # getting data by parse list of strings by indexes
    reader = PdfReader(path)
    text = reader.pages[0].extract_text()
    text = text.split('\n')
    data = {
        'COMPANY' :     text[0], 
        'BARCDODE1' :   cleanBarcodesData[0],
        'PN' :          text[1][text[1].index(':')+2:text[1].index(' SN:')],
        'SN' :          text[1][text[1].index(' SN: ')+5:],
        'DESCRIPTION' : text[2][text[2].index(' ')+1:],
        'LOCATION' :    text[3][text[3].index(':')+2:text[3].index(' CONDITION')],
        'CONDITION' :   text[3][text[3].index(' CONDITION: ')+12:],
        'RECEIVER#' :   text[4][text[4].index(':')+2:text[4].index(' UOM')],
        'UOM' :         text[4][text[4].index('UOM: ')+5:],
        'EXP DATE' :    text[5][text[5].index(':')+2:text[5].index(' PO')],
        'PO' :          text[5][text[5].index(' PO: ')+5:],
        'CERT SOURCE' : text[6][text[6].index(': ')+2:],
        'REC.DATE' :    text[7][text[7].index(':')+2:text[7].index(' MFG')],
        'MFG' :         text[7][text[7].index(' MFG: ')+6:],
        'BATCH#' :      text[8][text[8].index(':')+2:text[8].index(' DOM')],
        'DOM' :         text[8][text[8].index(' DOM: ')+6:],
        'REMARK' :      text[9][text[9].index(':')+2:text[9].index(' LOT#')],
        'LOT#' :        text[9][text[9].index(' LOT# : ')+8:],
        'TAGGED BY' :   text[11],
        'BARCODE2' :    cleanBarcodesData[1],
        'Qty' :         text[12][text[12].index(':')+2:text[12].index('NOTES:')],
        'NOTES' :       text[13],
    }
    return data

getDataFromPdf('examples/test_task.pdf')
