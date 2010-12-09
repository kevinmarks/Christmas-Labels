from reportlab.pdfgen import canvas
import csv
c = canvas.Canvas("labels.pdf")
from reportlab.lib.units import inch
pageWidth  = inch*8.5
pageHeight = inch*11.0
leading =1.2
boxMargin = inch*.125
c.setPageSize((pageWidth,pageHeight))
defaultAddress = "Kevin Marks\nSomewhere in\nSan Jose\nCA 95125"

def labelGrid(c,addressList,across=3, down=10,hGap=inch*.375,vGap=inch*.125,hMargin=inch*.25,vMargin=inch*.5):
    boxWidth = (pageWidth-(hMargin*2+hGap*(across-1)))/across
    boxHeight = (pageHeight-(vMargin*2+vGap*(down-1)))/down
    addresses = iter(addressList)
    c.setStrokeColorRGB(0,0,0)
    for y in range(down):
        for x in range(across):
            #c.rect(hMargin+x*(hGap+boxWidth),vMargin+y*(vGap+boxHeight),boxWidth,boxHeight, fill=0,stroke=1)
            fitTextInBox(c,next(addresses,defaultAddress), hMargin+x*(hGap+boxWidth),vMargin+y*(vGap+boxHeight),boxWidth,boxHeight)
             
def fitTextInBox(c,text,x,y,width,height):
    lines = text.splitlines()
    fontSize = (height-2*boxMargin)/(len(lines)*leading)
    maxWidth = rawWidth = width-2*boxMargin
    for line in lines:
        maxWidth= max(maxWidth, c.stringWidth(line,"Helvetica",fontSize))
    if maxWidth >rawWidth:
        fontSize = fontSize*rawWidth/maxWidth
    baseline=y+height-(fontSize+boxMargin)
    c.setFont("Helvetica", fontSize)
    for line in lines:
        c.drawString(x+boxMargin,baseline,line)
        baseline -= fontSize*leading
    
#for i in range(3):
#    labelGrid(c,[])
#    c.showPage()
import csv
reader = csv.reader(open("google.csv", "rb"))
i = reader.next().index("Address 1 - Formatted")
addresses = ["%s\n%s" % (x[0],x[i]) for x in reader]
#addresses[0:1]=[]
while (addresses):
    labelGrid(c,addresses[:10],2,5)
    c.showPage()
    addresses[0:10]=[]
c.save()
