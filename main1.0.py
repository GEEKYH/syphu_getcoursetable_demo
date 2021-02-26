import re
import datetime
import time
from bs4 import BeautifulSoup
#import ics
from ics import Calendar,Event

def printInfo():
        print('使用须知:')
        print('使用本脚本之前，你需要先将HTML文件名修改为\'课程表.html\'，且放置在脚本所在目录，并且使用编辑器编辑本脚本以修改学期开始日期。')
        print('导入时，请务必确认时间正确，以避免不必要的麻烦。')
        print('\n')

def is_number(s):
    try:
        float(s)
        return True
    except :
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False

class generator:
    soup = None
    c = Calendar()
    info = []
    map = [1,2,3,4,5,6,7]

    start_h = (8,10,13,15,18,19,21,22,15,16,17,18,19,20)
    end_h = (10,12,15,17,19,21,22,23,16,17,18,19,20,21)
    start_m = (30,20,30,20,00,40,20,50,25,20,15,30,25,20)
    end_m = (10,00,10,00,30,10,10,40,50,5,0,15,10,5)

    ## revise the date here
    term_start_time = datetime.datetime.strptime('2021-03-07 00:00:00+0800',
                                             '%Y-%m-%d %H:%M:%S%z')

    def __init__(self):
        with open("课程表.html", "rb") as f:
            html = f.read().decode("gbk")
            f.close()
        self.soup = BeautifulSoup(html, "html.parser")
        
    #表格处理
    def parser(self):
        position=[
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(4) > td:nth-of-type(2)',
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(4) > td:nth-child(3)',
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(4) > td:nth-child(4)',
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(4) > td:nth-child(5)',
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(4) > td:nth-child(6)',
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(4) > td:nth-child(7)',
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(4) > td:nth-child(8)',
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(5) > td:nth-child(2)',
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(5) > td:nth-child(3)',
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(5) > td:nth-child(4)',
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(5) > td:nth-child(5)',
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(5) > td:nth-child(6)',
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(5) > td:nth-child(7)',
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(5) > td:nth-child(8)',
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(6) > td:nth-child(2)',
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(6) > td:nth-child(3)',
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(6) > td:nth-child(4)',
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(6) > td:nth-child(5)',
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(6) > td:nth-child(6)',
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(6) > td:nth-child(7)',
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(6) > td:nth-child(8)',
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(7) > td:nth-child(2)',
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(7) > td:nth-child(3)',
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(7) > td:nth-child(4)',
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(7) > td:nth-child(5)',
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(7) > td:nth-child(6)',
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(7) > td:nth-child(7)',
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(7) > td:nth-child(8)',
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(8) > td:nth-child(2)',
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(8) > td:nth-child(3)',
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(8) > td:nth-child(4)',
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(8) > td:nth-child(5)',
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(8) > td:nth-child(6)',
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(8) > td:nth-child(7)',
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(8) > td:nth-child(8)',
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(9) > td:nth-child(2)',
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(9) > td:nth-child(3)',
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(9) > td:nth-child(4)',
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(9) > td:nth-child(5)',
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(9) > td:nth-child(6)',
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(9) > td:nth-child(7)',
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(9) > td:nth-child(8)',
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(10) > td:nth-child(2)',
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(10) > td:nth-child(3)',
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(10) > td:nth-child(4)',
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(10) > td:nth-child(5)',
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(10) > td:nth-child(6)',
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(10) > td:nth-child(7)',
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(10) > td:nth-child(8)',
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(11) > td:nth-child(2)',
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(11) > td:nth-child(3)',
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(11) > td:nth-child(4)',
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(11) > td:nth-child(5)',
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(11) > td:nth-child(6)',
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(11) > td:nth-child(7)',
                    'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(11) > td:nth-child(8)',
                    ]
        weekday = 0
        count = 0
        row = 0
        
        #下面的大循环一次处理一个“格子”，一个格子里有好几门课
        for posit in position:
                count = count + 1
                
                #变量row指明当前在哪一行

                #定位
                spt = str(self.soup.select(posit))
                #各种替换
                pattern = re.compile(r'<[^>]+>',re.S)
                pattern1 = re.compile(r'cutcut',re.S)
                pattern2 = re.compile(r'2节',re.S)
                result = pattern.sub('cut', spt)
                result = pattern1.sub('cut', result)
                result = pattern2.sub('off', result)
                result = result[4:-7]
                result = result.replace(" ","")
                resultlist = result.split("offcut")

                #self.info.append({count:count})
                
                for course in resultlist:
                        #course = course.replace(" ","")
                        courseinfo = course.split("cut")
                        course_dict = {}
                        if len(courseinfo) == 4:
                                course_dict['course_name'] = courseinfo[0]
                                course_dict['teacher_name'] = courseinfo[1]
                                course_dict['place'] = courseinfo[2]
                                course_dict['time'] = courseinfo[3]
                                course_dict['clip'] = count
                                self.info.append(course_dict)
                        elif len(courseinfo) == 3:
                                course_dict['course_name'] = courseinfo[0]
                                course_dict['place'] = courseinfo[1]
                                course_dict['time'] = courseinfo[2]
                                course_dict['clip'] = count
                                self.info.append(course_dict)
                        else:
                                self.info.append({'没有课':"None","clip":"0"})
                                
                                
                                #continue
                
                
                #由于是横向扫描，当处理完7个格子就需要换行
                '''                
                if count > 6:
                        row = row + 1
                        weekday = 0
                        count = 0
                course_time[weekday][row] = info
                weekday = weekday + 1
                '''
        #print(self.info)


        '''
        for row in rows:
            columns = row.findAll('tr')
            for column in columns:
                courses = column.findAll('td')
                for course in courses:
                    course = str(course)
                    self.info.append(course)
                    #course = course.lstrip(str(re.search(r'<td>|<td rowspan=\"\d\">',course))).rstrip('</td>')
                    #print(course)
            '''

    #写入日历文件
    def write_into_ics(self):
            count = 0
            for course in self.info:
                    
                    #print(self.info)
                    if course.get("没有课") == "None":
                            continue
                    else:
                            
                            weeks = course["time"][0:-1]
                            weekday = course.get("clip") % 7
                            time_cur = int(course.get("clip") / 7)#第几节
                            if course.get("clip") % 7 == 0:
                                    weekday = 7
                                    time_cur = int(course.get("clip") /7) - 1
                            time_end = time_cur
                            #第一节
                            temp = sorted(self.info,key = lambda x:x['clip']!=course["clip"])
                            #print(temp)
                            for next_course in temp:
                                    if next_course["clip"] == course["clip"]:
                                            if next_course["course_name"] == course.get('course_name') and next_course["time"] == course.get('time'):
                                                    next_course["没有课"]="None"
                                                    
                                                    if next_course.get("teacher_name") != None and next_course.get("teacher_name") not in course.get('teacher_name'):
                                                            course["teacher_name"] = course.get("teacher_name") + "、" + next_course.get("teacher_name")
                                                    if next_course.get("place") not in course.get('place'):
                                                            course["place"] = course.get("place") + "、" + next_course.get("place")
                                    else:
                                            break

                            temp = sorted(self.info,key = lambda x:x["clip"]!=int(course["clip"]) + 7)
                            samecourse_pass = 0
                            for next_course in temp:
                                    if next_course["clip"] == int(course["clip"]) + 7:
                                            
                                            if next_course["course_name"] == course.get('course_name') and next_course["time"] == course.get('time'):
                                                    if next_course["course_name"] == course.get('course_name') and samecourse_pass == 1:
                                                            next_course["没有课"]="None"
                                                            continue
                                                    else:        
                                                            next_course["没有课"]="None"
                                                            time_end = time_cur + 1
                                                            self.add_course(course,weekday,time_cur,time_end,weeks)
                                                            samecourse_pass = 1
                                                    
                                            
                                            else:
                                                    continue
                                    else:
                                            break
                            if time_end == time_cur:
                                    self.add_course(course,weekday,time_cur,time_end,weeks)

                                    
                            '''
                            #第二节
                            temp = sorted(self.info,key = lambda x:x["clip"]!=int(course["clip"]) + 7)
                            for next_course in temp:
                                    if next_course["clip"] == int(course["clip"]) + 7 and next_course["course_name"] == course.get('course_name') and next_course["time"] == course.get('time'):
                                            next_course["没有课"]="None"
                                            #第三节
                                            temp2 = sorted(self.info,key = lambda x:x["clip"]!=int(course["clip"]) + 14)
                                            for next_course in temp2:
                                                    
                                                    if next_course["clip"] == int(course["clip"]) + 14 and next_course["course_name"] == course.get('course_name') and next_course["time"] == course.get('time'):
                                                            #第四节
                                                            next_course["没有课"]="None"
                                                            temp3 = sorted(self.info,key = lambda x:x["clip"]!=int(course["clip"]) + 21)
                                                            for next_course in temp3:
                                                                    if next_course["clip"] == int(course["clip"]) + 21 and next_course["course_name"] == course.get('course_name') and next_course["time"] == course.get('time'):
                                                                            time_end = time_cur + 3
                                                                            next_course["没有课"]="None"
                                                                            print(next_course)
                                                                            self.add_course(course,weekday,time_cur,time_end,weeks)
                                                                            break
                                                                    else:
                                                                            time_end = time_cur + 2
                                                                            self.add_course(course,weekday,time_cur,time_end,weeks)
                                                                            break
                                                                                  
                                                            
                                                    else:
                                                            time_end = time_cur + 1
                                        
                                                            self.add_course(course,weekday,time_cur,time_end,weeks)
                                                            break
                                    break
          
                                            
                            if time_end == time_cur:
                                    self.add_course(course,weekday,time_cur,time_end,weeks)
          

                            '''                
                            '''
                            #以下代码确认是不是同一个课程不同老师
                            try:
                                    #course_index_cur = self.info.index(2)
                                    #course_index_end = self.info.index(3)
                                    #ls_course = self.info[course_index_cur:course_index_end]
                                    
                                    
                                    for last_course in self.info[course_index_cur+1:course_index_end-1]:
                                            for key in last_course:
                                                    #print(last_course,key)
                                                    pass
                                    
                                    for last_course in self.info[course_index_cur+1:course_index_end-1]:
                                            print(last_course)
                                            if last_course["course_name"] == course.get('course_name') and last_course["place"] == course.get('place') and last_course["time"] == course.get('time') and last_course["teacher_name"] != course.get('teacher_name'):
                                                    course["teacher_name"] = course.get("teacher_name") + "、" + last_course.get("teacher_name")
                                                    #time_end = time_cur + 1

                                                    #print("tttttttt")
                                                    #print(a)
                                                    #print(str(self.info[a]))
                                                    
                                                    #print("doon")
                                                    
                                                    #self.info.pop(a)
                                                    #self.info.insert(a,"没有课")
                                                    #print("non")
                                                   # self.add_course(course,weekday,time_cur,time_end,weeks)
                                            #a = int(self.info.index(last_course))
                                            #self.info[a] = "没有课"
                                            
     
                            except Exception as e:
                                    #time_end = time_cur
                                    
                                    #self.add_course(course,weekday,time_cur,time_end,weeks)
                                    print(e)
                                    

                            #以下代码是确认下面一节大课是否相同
                            course_index = (int(time_cur) + 1) * 7 + weekday
                            try:
                                    course_index_cur = self.info.index(course_index)
                                    course_index_end = self.info.index(course_index + 1)
                            
                                    for last_course in self.info[course_index_cur+1:course_index_end-1]:
                                            if last_course["course_name"] == course.get('course_name') and last_course["place"] == course.get('place') and last_course["time"] == course.get('time') and last_course["teacher_name"] != course.get('teacher_name'):
                                                    course["teacher_name"] = course.get("teacher_name") + "、" + last_course.get("teacher_name")
                                                    time_end = time_cur + 1
                                                    self.info[self.info.index(last_course)] = "没有课"
                                                    self.add_course(course,weekday,time_cur,time_end,weeks)
                            except:
                                    time_end = time_cur
                                    self.add_course(course,weekday,time_cur,time_end,weeks)
                            
                    '''
                            
                    
        #创建日历文件
            with open('syphu.ics', 'w', encoding='utf-8') as my_file:
                    my_file.writelines(self.c) 
               
    #写入日历文件
    def add_course(self,course,weekday,time_cur,time_end,weeks):
        #print(course)               
                
        
        
        
        local = course['place']
        #print(weeks)
        
        #for key in course:
        e = Event()
        
        #if("." in weeks):
        if True:
                weeks = weeks.split('.')
                for week in weeks:
                        if("-" in week):
                                week = week.split('-')
                                week_cur = int(week[0])
                                week_end = int(week[1])
                                while week_cur <= week_end:
                                        e = Event()
                                        e.name = course.get('course_name')
                                        e.location = local
                                        if str(course.get("teacher_name")) != "None":
                                                e.description = str(course.get('teacher_name'))
                                        offset = datetime.timedelta(days=(week_cur-1)*7+weekday,hours=self.start_h[int(time_cur)],minutes=self.start_m[int(time_cur)])
                                        e.begin = self.term_start_time + offset
                                        offset = datetime.timedelta(days=(week_cur-1)*7+weekday,hours=self.end_h[int(time_end)],minutes=self.end_m[int(time_end)])
                                        e.end = self.term_start_time + offset
                                        week_cur+=1
                                        self.c.events.add(e)
                        else:
                                
                                e = Event()
                                e.name = course.get('course_name')
                                e.location = local
                                if str(course.get("teacher_name")) != "None":
                                        e.description = str(course.get('teacher_name'))
                                offset = datetime.timedelta(days=(int(week)-1)*7+weekday,hours=self.start_h[int(time_cur)],minutes=self.start_m[int(time_cur)])
                                e.begin = self.term_start_time + offset
                                offset = datetime.timedelta(days=(int(week)-1)*7+weekday,hours=self.end_h[int(time_end)],minutes=self.end_m[int(time_end)])
                                e.end = self.term_start_time + offset
                                self.c.events.add(e)
                                
                
        #week = self.info[start+2].lstrip('</td>第').rstrip('周</td>')
        #remark = self.info[start+3].lstrip('</td>').rstrip('</td>')
        '''
        e = Event()
        e.name = course.get(course_name)
        e.location = local
        e.description = str(course.get(teacher_name) + course.get(place))
        
        offset = datetime.timedelta(days=2*7+weekday,hours=8,minutes=30)
        e.begin = self.term_start_time + offset
        offset = datetime.timedelta(days=2*7+weekday,hours=8,minutes=30)
        e.end = self.term_start_time + offset
        #week_cur+=1
        self.c.events.add(e)
        '''

        '''
        e = Event()
        if('-' in week):
            week = week.split('-')
            #print(week)
            week_cur = int(week[0])
            week_end = int(week[1])
            while week_cur <= week_end:
                e = Event()
                e.name = course_name
                e.location = local
                e.description = remark
                offset = datetime.timedelta(days=(week_cur-1)*7+weekday,hours=self.start_h[int(time[0])],minutes=self.start_m[int(time[0])])
                e.begin = self.term_start_time + offset
                offset = datetime.timedelta(days=(week_cur-1)*7+weekday,hours=self.end_h[int(time[1])],minutes=self.end_m[int(time[1])])
                e.end = self.term_start_time + offset
                week_cur+=1
                self.c.events.add(e)
        else:
            week = week.split(',')
            #print(week)
            for we in week:
                e = Event()
                e.name = course_name
                e.location = local
                e.description = remark
                offset = datetime.timedelta(days=(int(we)-1)*7+weekday,hours=self.start_h[int(time[0])],minutes=self.start_m[int(time[0])])
                e.begin = self.term_start_time + offset
                offset = datetime.timedelta(days=(int(we)-1)*7+weekday,hours=self.end_h[int(time[1])],minutes=self.end_m[int(time[1])])
                e.end = self.term_start_time + offset
                self.c.events.add(e)
        '''

def main():
    printInfo()
    #a = input('确认后输入1以继续...')
    a = "1"
    if a=='1':
        g = generator()
        g.parser()
        g.write_into_ics()

if __name__ == '__main__':
    main()
