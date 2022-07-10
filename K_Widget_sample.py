
import numpy as np
import cv2

#my module
import K_Widget
#functinon sample
def function():
    print("Text1")
def function2(text):
    print(text)
def functino3(num,num2):
    print(num*num2)

def function4(img):
    cv2.imwrite("sample.jpg",img)
    
def main():
    nullcanvas = np.zeros((1000,1000,3),np.int8)
                          
    rectangle = K_Widget.Rectangle(nullcanvas,[100,100],color=(255,33,40))
    text = K_Widget.Text(nullcanvas,"Text",color = (0,0,255))
    button =K_Widget.Button(nullcanvas,text="Button",textcolor = (255,0,255),thickness=1)
    button2 = K_Widget.Button(nullcanvas,text="SAVE IMG",textcolor = (0,0,255),thickness = 1)
    
    rectangle.place(100,150)
    text.place(100,250)
    button.place(100,350)
    button2.place(300,150)
    
    t = 0
    deathtime = 100000000000

    while t < deathtime:

        cv2.imshow("sample frame",nullcanvas)
        #buttonobject activate
        button.active("sample frame",function,function2,functino3,function2 = "Text2",functino3 = (10,4)) 
        button2.active("sample frame",function4,function4 = nullcanvas)
        cv2.setMouseCallback("sample frame", K_Widget.mousecallevent,(button,button2))
        key = cv2.waitKey(10) & 0xFF
        if key == ord('s'):
            
            cv2.destroyAllWindows()
            break        
if __name__ == '__main__':
    main()
