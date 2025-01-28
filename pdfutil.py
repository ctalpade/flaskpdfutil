from pypdf import PdfWriter,PdfReader
import os

def mergePdfs(filelist : list):
    mergedFileName = "merged-pdf.pdf"
    merger = PdfWriter()
    for pdf in filelist:
        print('merging '+str(pdf))
        merger.append(pdf)
    merger.write(mergedFileName)
    merger.close()
    print('Merging Completed '+str(mergedFileName))

#mergePdfs(["file1.pdf", "file2.pdf"])


def splitPdfs(pdfName : str, parts : int = -1,pdfpath :str = '.'):
    reader = PdfReader(pdfName)
    pagecount = len(reader.pages)
    #print('pdfname '+str(pdfName)+' has page count '+str(pagecount)+' parts requested '+str(parts))
    if parts <=0:
        parts = 2
    pageperpart = round(pagecount / parts)
    #print('pageperpart '+str(pageperpart))
    parts_calc = int(pagecount / pageperpart)
    print('parts_calc '+str(parts_calc))
    remainOddPages = int(pagecount - (pageperpart * parts_calc))
    #print('remainingOddPages '+str(remainOddPages))

    input = open(pdfName, "rb")
    pstart = 0
    for p in range(parts_calc+remainOddPages):
        merger = PdfWriter()
        #print('loop pstart '+str(pstart)+' pageperpart '+str(pageperpart))
        if remainOddPages > 0 and p == parts_calc+remainOddPages - 1:
            merger.append(fileobj=input, pages=(pstart, pstart+remainOddPages))
        else:    
            merger.append(fileobj=input, pages=(pstart, pstart+pageperpart))
        pstart = pstart+pageperpart

        output = open(os.path.join(pdfpath,"part"+str(p+1)+".pdf"), "wb")
        merger.write(output)
        # Close file descriptors
        merger.close()
        output.close()
    

#splitPdfs("ira-school-info.pdf",2)