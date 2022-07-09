# -*- coding: utf-8 -*-
"""
　  my uniqe cv2 gui classes
    rootclass : object
    rectangle : rectangle_object 
        place rectangle
    text : text_object
        place text
    button : button_object
        place button
        active bind function
"""
import cv2

fontlis =  [cv2.FONT_HERSHEY_SIMPLEX,
                    cv2.FONT_HERSHEY_PLAIN,
                    cv2.FONT_HERSHEY_DUPLEX,
                    cv2.FONT_HERSHEY_COMPLEX,
                    cv2.FONT_HERSHEY_TRIPLEX,
                    cv2.FONT_HERSHEY_COMPLEX_SMALL,
                    cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
                    cv2.FONT_HERSHEY_SCRIPT_COMPLEX,
                    cv2.FONT_ITALIC]

class object:
    def __init__(self,*ags):
        self.parentimg = None
        self.size = [None,None]
        self.color = (None,None,None)
        self.text = ""
        self.fontnum = 0
        self.fontscale = 0.0
        self.thickness =1
        self.lineType = cv2.LINE_4
        self.shift = 0
        
    def setting(self,constructsdic):
        for key in constructsdic:
            exec(f"self.{key} = constructsdic[\"{key}\"]")
            
class Rectangle(object):
    def __init__(self,img,size,color=(0,0,0),fill=False,thickness=3,lineType=cv2.LINE_4,shift=0):
        super().__init__()
        dic = {"parentimg":img,
               "size"  : size,
               "color" : color,
               "thickness" : thickness,
               "lineType" :lineType,
               "shift" : shift
              }
        self.setting(dic)
        
    def place(self,x,y):
        w,h = self.size
        p1 = (x,y)
        p2 = (x + w,y + h)
        cv2.rectangle(self.parentimg,
                      pt1      =p1,
                      pt2      =p2,
                      color    =self.color,
                      thickness=self.thickness,
                      lineType =self.lineType,
                      shift    =self.shift)
        
class Text(object):
    def __init__(self,img,text,color=(0,0,0),fontnum = 0,fontscale = 1.0,thickness=3,lineType=cv2.LINE_4):
        super().__init__()
        (w, h), baseline = cv2.getTextSize(str(text), fontlis[fontnum],fontscale, thickness)
        size = [w,h + baseline]

        dic = {"parentimg":img,
               "size"     : size,
               "color"    : color,
               "text"     : text,
               "fontnum"  : fontnum,
               "fontscale": fontscale,
               "thickness": thickness,
               "lineType" : lineType
              }
        self.setting(dic)
        
        
    def place(self,x,y):
        locate = (x,y+self.size[1])
        cv2.putText(self.parentimg,
                    text=self.text,
                    org= locate,
                    fontFace=fontlis[self.fontnum],
                    fontScale=self.fontscale,
                    color=self.color,
                    thickness=self.thickness,
                    lineType=self.lineType)
        
class Button(Text):
    def __init__(self,img,text,textcolor = (0,0,0),bg = (255,255,255),fill = True,fontnum = 5,fontscale = 1.0,thickness=3,lineType=cv2.LINE_4):
        super().__init__(img,text,color=textcolor,fontnum = fontnum,fontscale = fontscale,thickness=thickness,lineType=lineType)
        if textcolor == (0,0,0):
            bg = textcolor
        self.fill = fill
        self.buttoncolor = bg
        self.locate = [0,0,0,0]#top,left,bottom,left
        
        self.mosusein = False
        self.act = False
    def place(self,x,y):
        w,h = self.size
        padding = 10
        p1 = (x-padding,y)
        p2 = (x + w+padding,y + h+padding)
        self.locate = [y,x-padding,y + h+padding,x + w+padding]
        RoundedRectangle(self.parentimg,p1,p2,5,self.buttoncolor,self.thickness,self.lineType,fill = self.fill)
        super().place(x,y)
    def active(self,framename,*command,**keys):
        self.act = True
        cv2.setMouseCallback(framename, self.uerinterrupt)

        self.command = command
        self.keys = keys
        
        
        for key in self.keys:
            if type(self.keys[key]) != type(tuple()):
                self.keys.update({key:tuple([self.keys[key]])})
        
    def deactive(self):
        self.act = False
    def uerinterrupt(self,event, x, y, flags, param):
        if x>=self.locate[1] and x <= self.locate[3] and y >=self.locate[0] and y <= self.locate[2]:
            self.mousein = True
        else:
            self.mousein = False
        if self.mousein:
            if event == cv2.EVENT_LBUTTONDOWN:
                for com in self.command:
                    if com.__name__ in self.keys:
                        keydict = self.keys
                        params = keydict[com.__name__]
                        print(*params)
                        com(*params)
                    else:
                        com()
        

        
        
        
def RoundedRectangle(img,p1,p2,r,color,thickness,lineType,fill = False):
    #cv2.ellipse(img, center, axes, angle, startAngle, endAngle, color, thickness=1, lineType=cv2.LINE_8, shift=0)
    if p1[0] >=p2[0]:
        right = p2[0]
        left = p1[0]
    else:
        right = p2[0]
        left = p1[0]
    if p1[1] >=p2[1]:
        top = p1[1]
        bottom = p2[1]
    else:
        top = p1[1]
        bottom = p2[1]
    
    if fill:
        cv2.rectangle(img,pt1=(left,top+r),pt2=(right,bottom-r),color = color,thickness=-1,lineType=cv2.LINE_4,shift=0)
        cv2.rectangle(img,pt1=(left+r,top),pt2=(right-r,bottom),color = color,thickness=-1,lineType=cv2.LINE_4,shift=0)
        
        cv2.ellipse(img, (right-r, bottom-r), (r,r), 0, 0, 90, color, thickness=-1)
        cv2.ellipse(img, (left+r, bottom-r), (r,r), 90, 0, 90, color, thickness=-1)
        cv2.ellipse(img, (left+r, top+r), (r,r), 180, 0, 90, color, thickness=-1)
        cv2.ellipse(img, (right-r, top+r), (r,r), 270, 0, 90, color, thickness=-1)
    else:
        cv2.rectangle(img,pt1=(left,top+r),pt2=(right,bottom-r),color = color,thickness=thickness,lineType=lineType,shift=0)
        cv2.rectangle(img,pt1=(left+r,top),pt2=(right-r,bottom),color = color,thickness=thickness,lineType=lineType,shift=0)
        
        cv2.ellipse(img, (right-r, bottom-r), (r,r), 0, 0, 90, color, thickness=thickness)
        cv2.ellipse(img, (left+r, bottom-r), (r,r), 90, 0, 90, color, thickness=thickness)
        cv2.ellipse(img, (left+r, top+r), (r,r), 180, 0, 90, color, thickness=thickness)
        cv2.ellipse(img, (right-r, top+r), (r,r), 270, 0, 90, color, thickness=thickness)
