#!/usr/bin/env python
#
#
import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
pageWidth  = inch*8.5
pageHeight = inch*11.0
leading =1.2
boxMargin = inch*.125

info={'user':'unknown'}

class MainHandler(webapp.RequestHandler):
    def get(self):
        info['user'] = self.request.get("user","unknown")
        info['address'] = self.request.get("address","1600 Pennsylvania Avenue")
        path = os.path.join(os.path.dirname(__file__), "index.html")
        self.response.out.write(template.render(path,info))

def labelGrid(c,addressList,defaultAddress="test address",across=3, down=10,hGap=inch*.375,vGap=inch*.125,hMargin=inch*.25,vMargin=inch*.5):
    boxWidth = (pageWidth-(hMargin*2+hGap*(across-1)))/across
    boxHeight = (pageHeight-(vMargin*2+vGap*(down-1)))/down
    addressList.extend([defaultAddress]*(across*down-len(addressList))) # work around not having proper next()
    addresses = iter(addressList)
    c.setStrokeColorRGB(0,0,0)
    for y in range(down):
        for x in range(across):
            #c.rect(hMargin+x*(hGap+boxWidth),vMargin+y*(vGap+boxHeight),boxWidth,boxHeight, fill=0,stroke=1)
            fitTextInBox(c,addresses.next(), hMargin+x*(hGap+boxWidth),vMargin+y*(vGap+boxHeight),boxWidth,boxHeight)
             
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

class AddressHandler(webapp.RequestHandler):
    def get(self):
        info['user'] = self.request.get("user","unknown")
        info['address'] = self.request.get("address","1600 Pennsylvania Avenue")
        path = os.path.join(os.path.dirname(__file__), "index.html")
        #self.response.out.write(template.render(path,info))
        c = canvas.Canvas(self.response.out)
        c.setPageSize((pageWidth,pageHeight))
        labelGrid(c,[],"%s\n%s" % (info['user'],info['address'] ),3,10)
        #fitTextInBox(c, "Goodbye\nSmall World",inch*2,inch*7,inch*4,inch )       
        c.showPage()
        self.response.headers['Content-Type'] = "application/pdf"
        c.save()


def main():
    application = webapp.WSGIApplication([('/', MainHandler),('/addresses.pdf', AddressHandler)], debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
