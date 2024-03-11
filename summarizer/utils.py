import fitz

"""
    extract text from the pdf
"""
def extract_text_from_pdf(filename: str):
    doc = fitz.open(f"{filename}")
    totalLength = 0
    finalText = ""

    for page in doc:
        page_text = page.get_text()

        finalText = finalText + page_text 
        totalLength = totalLength + round(len(page_text)/7)
        print(f"The number of words in {page} is: {round(len(page_text)/7)}")
    
    return finalText, totalLength
    
    
"""
splits based on no. of words of containing wordlength and provide array 
"""    
def splittext(text, wordlength, splitinwords) -> list[str]:
    templength = wordlength
    textarray = []

    while templength >= 0:
        part = " ".join(text.split()[:splitinwords])
        text = " ".join(text.split()[splitinwords:])
        templength = templength - splitinwords
        textarray.append(part)

    return textarray