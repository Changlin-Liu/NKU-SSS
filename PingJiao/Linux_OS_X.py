#coding=GBK
import httplib
import re
import os
from wx import *

class MyFrame(Frame):
    def __init__(self, parent, ID, title, pos=DefaultPosition,
                 size=(280, 380), style=DEFAULT_FRAME_STYLE):
        Frame.__init__(self, parent, ID, title, pos, size, style)
        self.panel = Panel(self, -1)
        
        label_id=StaticText(self.panel,1008,"Student ID:")
        label_id.SetPosition(Point(15, 15))
        label_psw=StaticText(self.panel,1009,"Password:")
        label_psw.SetPosition(Point(15, 65))
        label_val=StaticText(self.panel,1010,"Validate Code:")
        label_val.SetPosition(Point(15, 165))
        
        self.text_id=TextCtrl(self.panel,1005)
        self.text_id.SetPosition(Point(120, 15))
        self.text_psw=TextCtrl(self.panel,1006)
        self.text_psw.SetPosition(Point(120, 65))
        self.text_val=TextCtrl(self.panel,1007)
        self.text_val.SetPosition(Point(120, 165))
        
        button = Button(self.panel, 1003, u"�˳�")
        button.SetPosition(Point(120, 215))
        EVT_BUTTON(self, 1003, self.OnCloseMe)
        EVT_CLOSE(self, self.OnCloseWindow)

        self.button = Button(self.panel, 1004, u"����")
        self.button.SetPosition(Point(30, 215))
        EVT_BUTTON(self, 1004, self.OnPressMe)

        #get cookie
        conn=httplib.HTTPConnection("222.30.32.10")
        conn.request("GET","/")
        res=conn.getresponse()
        self.cookie=res.getheader("Set-Cookie")
        conn.close()
        self.headers= {"Content-Type":"application/x-www-form-urlencoded","Cookie":self.cookie}
        #get ValidateCode
        conn=httplib.HTTPConnection("222.30.32.10")
        conn.request("GET","/ValidateCode","",self.headers)
        res=conn.getresponse()
        f=open("ValidateCode.jpg","w+b")
        f.write(res.read())
        f.close()
        conn.close()

        image=Image("ValidateCode.jpg",BITMAP_TYPE_JPEG)
        val=StaticBitmap(self.panel,bitmap=image.ConvertToBitmap())
        val.SetPosition(Point(15, 115))

        self.label_status=StaticText(self.panel,1099,"Modified By NKUCodingCat\nto compatible ubuntu")
        self.label_status.SetPosition(Point(20, 340))

    def OnCloseMe(self, event):
        self.Close(True)

    def OnPressMe(self, event):
        #��ʾ���Ժ�
        self.button.SetLabel(u"���Ժ�")
        
        stu_id=self.text_id.GetValue()
        psw=self.text_psw.GetValue()
        val=self.text_val.GetValue()
        params="operation=&usercode_text="+stu_id+"&userpwd_text="+psw+"&checkcode_text="+val+"&submittype=%C8%B7+%C8%CF"
        conn=httplib.HTTPConnection("222.30.32.10")
        conn.request("POST","/stdloginAction.do",params,self.headers);
        res=conn.getresponse()
        conn.close()
        conn=httplib.HTTPConnection("222.30.32.10")
        conn.request("GET","/evaluate/stdevatea/queryCourseAction.do","",self.headers);
        res=conn.getresponse()
        content=res.read().decode("GBK")
        num=int(re.findall(u"�� ([0-9]*) ��",content)[0])
        conn.close()
        failcount=0
        for i in range(num):
            conn=httplib.HTTPConnection("222.30.32.10")
            conn.request("GET","/evaluate/stdevatea/queryTargetAction.do?operation=target&index="+str(i),"",self.headers);
            res=conn.getresponse()
            content=res.read().decode("GBK")
            content=content.replace(u"�ý�ʦ���������ӡ��",u"�ý�ʦ���������ӡ��10��")
            #��������
            item=re.findall(u"��([0-9]*)��",content)
            conn.close()
            #submit
            conn=httplib.HTTPConnection("222.30.32.10")
            params="operation=Store"
            
            for j in range(len(item)):  params+=("&array["+str(j)+"]="+item[j])
            params+="&opinion="
            self.headers= {"Content-Type":"application/x-www-form-urlencoded"
                  ,"Cookie":self.cookie,"Referer":"http://222.30.32.10/evaluate/stdevatea/queryTargetAction.do?operation=target&index="+str(i)}
            conn.request("POST","/evaluate/stdevatea/queryTargetAction.do",params,self.headers);
            rescontent=conn.getresponse().read()
            if -1==rescontent.find("�ɹ����棡"):failcount+=1
            conn.close()
        #��ʾ�ɹ�
        s=u"���!\n�ܹ�: %d\n�ɹ�: %d" % (num,num-failcount)
        self.label_status=StaticText(self.panel,1008,s)
        self.label_status.SetPosition(Point(50, 265))    
        os.remove("ValidateCode.jpg")
        
    def OnCloseWindow(self, event):
        self.Destroy()

class MyApp(App):
    def OnInit(self):
        frame = MyFrame(None, -1, u"һ������ by Jeff")
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

app = MyApp(0)
app.MainLoop()
