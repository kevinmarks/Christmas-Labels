from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

leading =1.2
boxMargin = inch*.125

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

c = canvas.Canvas("hello.pdf")
# move the origin up and to the left
c.translate(inch,inch)
# define a large font
c.setFont("Helvetica", 80)
# choose some colors
#c.setStrokeColorRGB(0.2,0.5,0.3)
#c.setFillColorRGB(1,0,1)
# draw a rectangle
#c.rect(inch,inch,6*inch,9*inch, fill=1)
fitTextInBox(c, "Goodbye\nSmall World",inch*2,inch*4,inch*4,inch )

# make text go straight up
c.rotate(90)
# change color
c.setFillColorRGB(0,0,0.77)
# say hello (note after rotate the y coord needs to be negative!)
c.drawString(3*inch, -3*inch, "Hello World")
c.showPage()
c.save()