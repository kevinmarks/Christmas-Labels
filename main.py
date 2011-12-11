#!/usr/bin/env python
#
#
import os

import csv
import StringIO

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.units import mm
usPageWidth  = inch*8.5
usPageHeight = inch*11.0
leading =1.2
boxMargin = inch*.125
# across and down are no of labels in each direction. hMargin and vMargin space around the edges; hGap and vGap space between labels
# leftIndent is a per label space for an image on the LHS of the label; topOffset is for labels that are asymmetric vertically
labelTypes =    {   "Avery5160":{"across":3, "down":10 },
                    "AveryXmas":{"across":3, "down":10, "leftIndent":inch*.5625, "topOffset":inch/16.0},
                    "Avery5163":{"across":2, "down":5},
                    "Avery5164":{"across":2, "down":3},
                    "Avery7160":{"across":3, "down":7, "pageWidth":mm*210,"pageHeight":mm*297}
                }

info={'user':'unknown'}

class MainHandler(webapp.RequestHandler):
    def get(self):
        info['user'] = self.request.get("user","unknown")
        info['address'] = self.request.get("address","1600 Pennsylvania Avenue NW\nWashington, DC 20500")
        path = os.path.join(os.path.dirname(__file__), "index.html")
        self.response.out.write(template.render(path,info))

def labelGridType(c,addressList,defaultAddress="test address",temp=labelTypes["Avery5160"],drawEdges=False):
    across = temp.get('across',3)
    down = temp.get("down",10)
    hGap = temp.get("hGap",inch*.25)
    vGap = temp.get("vGap",inch*.125)
    hMargin = temp.get("hMargin",inch*.25)
    vMargin = temp.get("vMargin",inch*.5625)
    leftIndent = temp.get("leftIndent",0)
    topOffset = temp.get("topOffset",0)
    pageWidth = temp.get("pageWidth", usPageWidth)
    pageHeight = temp.get("pageHeight", usPageHeight)    
    
    boxWidth = (pageWidth-(hMargin*2+hGap*(across-1)))/across
    boxHeight = (pageHeight-(vMargin*2+vGap*(down-1)))/down
    addressList.extend([defaultAddress]*(across*down-len(addressList))) # work around not having proper next()
    addresses = iter(addressList)
    c.setStrokeColorRGB(0,0,0)
    for y in range(down):
        for x in range(across):
            if (drawEdges):
                c.rect(hMargin+x*(hGap+boxWidth),pageHeight-(vMargin+boxHeight+vGap+topOffset)-y*(vGap+boxHeight),boxWidth,boxHeight, fill=0,stroke=1)
            fitTextInBox(c,addresses.next(), hMargin+x*(hGap+boxWidth)+leftIndent ,pageHeight-(vMargin+boxHeight+vGap+topOffset)-y*(vGap+boxHeight),boxWidth-leftIndent,boxHeight)
             
def fitTextInBox(c,text,x,y,width,height):
    try:
        lines = text.splitlines()
    except:
        return
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

class AddressHandler(webapp.RequestHandler):

    def post(self):
        info['user'] = self.request.get("user","unknown")
        info['address'] = self.request.get("address","1600 Pennsylvania Avenue")
        info['addressfile'] = self.request.get("addressfile",None)
        info['template'] = self.request.get("template","Avery5160")
        path = os.path.join(os.path.dirname(__file__), "index.html")
        pageWidth = labelTypes[info['template']].get("pageWidth", usPageWidth)
        pageHeight = labelTypes[info['template']].get("pageHeight", usPageHeight)
        c = canvas.Canvas(self.response.out)
        c.setPageSize((pageWidth,pageHeight))
        if info['addressfile']:
            try:
                reader = csv.reader(StringIO.StringIO(info['addressfile']))
                i = reader.next().index("Address 1 - Formatted")
                addresses = ["%s\n%s" % (x[0],x[i]) for x in reader if len(x[i])>5]
            except:
                addresses = ["No Addresses Found\nin your file\nemail:help@xmllabels.com",]
            while (addresses):
                labelGridType(c,addresses[:30],"%s\n%s" % (info['user'],info['address'] ),labelTypes[info['template']])
                c.showPage()
                addresses[0:30]=[]
        else:
        	labelGridType(c,[],"%s\n%s" % (info['user'],info['address'] ),labelTypes[info['template']])
        	c.showPage()
        self.response.headers['Content-Type'] = "application/pdf"
        c.save()


def main():
    application = webapp.WSGIApplication([('/', MainHandler),('/addresses.pdf', AddressHandler)], debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
