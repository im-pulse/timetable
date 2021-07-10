import tkinter
import tkinter.font
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
import math
import sys
import os
from tkinter import *

# 설치후 최초 실행시 발생하는 오류 수정
f=open('202101.txt', 'a')
f.close()

# 메인 창 실행하는 코드
class App(tkinter.Tk) :
    def __init__(self) :
        tkinter.Tk.__init__(self)
        self._frame = None
        self.switch_frame(PageOne)
        self.title("홍익대학교 학습지원 프로그램")
        self.geometry("620x300")
        self.resizable(False, False)
        self.overrideredirect(False)

    def switch_frame(self, frame_class) :
        new_frame = frame_class(self)
        if self._frame is not None :
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


# 수강 목록 페이지
class PageOne(tkinter.Frame) :    
    def __init__(self, master) :
        Frame.__init__(self, master)
        Frame.configure(self)

        # 폰트 설정
        font_settings = tkinter.font.Font(size = 12)

        # 상단 탭 버튼 설정
        page_one_button = Button(self, width = 12, height = 1, pady = 5, text = "수강 목록", bd = 0, bg = "#04B3CE", fg = "#FFFFFF", font = font_settings, command = lambda : master.switch_frame(PageOne))
        page_one_button.grid(row = 1, column = 1, sticky = "w")
        
        page_two_button = Button(self, width = 12, height = 1, pady = 5, text = "학점 계산기", bd = 0, bg = "#7F7F7F", fg = "#FFFFFF", font = font_settings, command = lambda : master.switch_frame(PageTwo))
        page_two_button.place(x = 116)

        page_three_button = Button(self, width = 12, height = 1, pady = 5, text = "시간표", bd = 0, bg = "#7F7F7F", fg = "#FFFFFF", font = font_settings, command = lambda : master.switch_frame(PageThree))
        page_three_button.place(x = 232)



        # 과목 트리뷰 생성
        style = ttk.Style()
        style.configure("mystyle.Treeview", font=(12))
        style.configure("mystyle.Treeview.Heading", font=(12))
        style.layout("mystyle.Treeview", [("mystyle.Treeview.treearea", {"sticky": "nswe"})])    

        subject_treeview = tkinter.ttk.Treeview(self, columns =["#1", "#2", "#3", "#4", "#5", "#6"], height = 10, selectmode = "browse", style = "mystyle.Treeview")
        subject_treeview.grid(row = 2, column = 1, columnspan = 3)

        subject_treeview.column("#0", width = 0, stretch = False)
        subject_treeview.heading("#0", text = "", anchor = W)
        subject_treeview.column("#1", width = 240, stretch = False)
        subject_treeview.heading("#1", text = "과목명", anchor = W)
        subject_treeview.column("#2", width = 120, stretch = False)
        subject_treeview.heading("#2", text = "교수명", anchor = W)
        subject_treeview.column("#3", width = 40, stretch = False)
        subject_treeview.heading("#3", text = "학점", anchor = W)
        subject_treeview.column("#4", width = 80, stretch = False)
        subject_treeview.heading("#4", text = "이수구분", anchor = W)
        subject_treeview.column("#5", width = 120, stretch = False)
        subject_treeview.heading("#5", text = "시간", anchor = W)
        subject_treeview.column("#6", width = 0, stretch = False)
        subject_treeview.heading("#6", text = "평점", anchor = W)


        # 데이터 불러오기
        def open_data() :
            file = open(file = "202101.txt", mode = "r", encoding = "utf-8")
            lines = len(file.readlines())
            file.close()

            file = open(file = "202101.txt", mode = "r", encoding = "utf-8")
            for i in range(0, int(lines / 6)) :
                data = (file.readline().rstrip("\n"), 
                        file.readline().rstrip("\n"),
                        file.readline().rstrip("\n"),
                        file.readline().rstrip("\n"),
                        file.readline().rstrip("\n"),
                        file.readline().rstrip("\n"))

                subject_treeview.insert(parent = "", index = "end", text = "", values = data)

        open_data() # 프로그램 실행 시 자동으로 데이터를 불러옴

        # 데이터 저장하기
        def save_data() :
            file = open(file = "202101.txt", mode = "w", encoding = "utf-8")
            for i in range(1, 100) :
                index_number = "I" + format(i, "03")
                if subject_treeview.exists(index_number) == True :
                    data = subject_treeview.item("I" + format(i, "03"), "values")
                    for j in range(0, 6) : 
                        file.write(data[j] + "\n")
            file.close()

        # 과목 추가하기
        def add_subject() :
            number_of_items = len(subject_treeview.get_children())

            if number_of_items > 15 :
                tkinter.messagebox.showwarning("", "더 이상 추가할 수 없습니다.")
            # 15과목 이상은 입력할수 없게 처리함

            else :
                add_screen = Tk()
                add_screen.title("과목 추가")
                add_screen.resizable(False, False)

                # 과목명 항목
                subject_label = Label(add_screen, text = "과목명", font = font_settings)
                subject_label.grid(row = 1, column = 0, sticky = W, padx = 10, pady = 10)
                subject = Entry(add_screen, width = 20, bd = 0, font = font_settings)
                subject.grid(row = 1, column = 1, sticky = N+E+W+S, padx = 10, pady = 10)

                # 교수명 항목
                professor_label = Label(add_screen, text = "교수명", font = font_settings)
                professor_label.grid(row = 2, column = 0, sticky = W, padx = 10, pady = 10)
                professor = Entry(add_screen, width = 20, bd = 0, font = font_settings)
                professor.grid(row = 2, column = 1, sticky = N+E+W+S, padx = 10, pady = 10)

                # 학점 항목
                credit_label = Label(add_screen, text = "학점", font = font_settings)
                credit_label.grid(row = 3, column = 0, sticky = W, padx = 10, pady = 10)
                credit = tkinter.ttk.Combobox(add_screen, state = "readonly", height = 5, values = [1, 2, 3, 4, 5], font = font_settings)
                credit.grid(row = 3, column = 1, sticky = N+E+W+S, padx = 10, pady = 10)

                # 이수구분 항목
                type_label = Label(add_screen, text = "이수구분", font = font_settings)
                type_label.grid(row = 4, column = 0, sticky = W, padx = 10, pady = 10)
                type = tkinter.ttk.Combobox(add_screen, state = "readonly", height = 3, values = ["전공", "MSC교과", "교양"], font = font_settings)
                type.grid(row = 4, column = 1, sticky = N+E+W+S, padx = 10, pady = 10)

                # 시간 항목
                time_label = Label(add_screen, text = "시간", font = font_settings)
                time_label.grid(row = 6, column = 0, sticky = W+S, padx = 10, pady = 4)

                # 잘못 입력했을 시 초기화할수 있도록 빈 선택지도 추가
                days_list = ["","월요일", "화요일", "수요일", "목요일", "금요일"]
                period_list = ["","1교시", "2교시", "3교시", "4교시", "5교시", "6교시", "7교시", "8교시", "9교시", "10교시", "11교시", "12교시"]

                time_1_days = tkinter.ttk.Combobox(add_screen, state = "readonly", height = 6, width = 8, values = days_list, font = font_settings)
                time_1_days.grid(row = 6, column = 1, sticky = W+S, padx = 10)
                time_1_period = tkinter.ttk.Combobox(add_screen, state = "readonly", height = 13, width = 8, values = period_list, font = font_settings)
                time_1_period.grid(row = 6, column = 2, sticky = E+S, padx = 10)

                time_2_days = tkinter.ttk.Combobox(add_screen, state = "readonly", height = 6, width = 8, values = days_list, font = font_settings)
                time_2_days.grid(row = 7, column = 1, sticky = W, padx = 10)
                time_2_period = tkinter.ttk.Combobox(add_screen, state = "readonly", height = 13, width = 8, values = period_list, font = font_settings)
                time_2_period.grid(row = 7, column = 2, sticky = E, padx = 10)

                time_3_days = tkinter.ttk.Combobox(add_screen, state = "readonly", height = 6, width = 8, values = days_list, font = font_settings)
                time_3_days.grid(row = 8, column = 1, sticky = W, padx = 10)
                time_3_period = tkinter.ttk.Combobox(add_screen, state = "readonly", height = 13, width = 8, values = period_list, font = font_settings)
                time_3_period.grid(row = 8, column = 2, sticky = E, padx = 10)

                time_4_days = tkinter.ttk.Combobox(add_screen, state = "readonly", height = 6, width = 8, values = days_list, font = font_settings)
                time_4_days.grid(row = 9, column = 1, sticky = W, padx = 10)
                time_4_period = tkinter.ttk.Combobox(add_screen, state = "readonly", height = 13, width = 8, values = period_list, font = font_settings)
                time_4_period.grid(row = 9, column = 2, sticky = E, padx = 10)

                time_5_days = tkinter.ttk.Combobox(add_screen, state = "readonly", height = 6, width = 8, values = days_list, font = font_settings)
                time_5_days.grid(row = 10, column = 1, sticky = W, padx = 10)
                time_5_period = tkinter.ttk.Combobox(add_screen, state = "readonly", height = 13, width = 8, values = period_list, font = font_settings)
                time_5_period.grid(row = 10, column = 2, sticky = E, padx = 10)

                time_6_days = tkinter.ttk.Combobox(add_screen, state = "readonly", height = 6, width = 8, values = days_list, font = font_settings)
                time_6_days.grid(row = 11, column = 1, sticky = W, padx = 10)
                time_6_period = tkinter.ttk.Combobox(add_screen, state = "readonly", height = 13, width = 8, values = period_list, font = font_settings)
                time_6_period.grid(row = 11, column = 2, sticky = E, padx = 10)



                # 모든 항목 정상적으로 입력 여부 확인
                def add_subject_ok() :
                    time = []

                    if time_1_days.get() != "" and time_1_period.get() != "" :
                        time_1 = str(time_1_days.get()[0]) + str(time_1_period.get()).replace("교시", "")
                        time.append(time_1)

                    if time_2_days.get() != "" and time_2_period.get() != "" :
                        time_2 = str(time_2_days.get()[0]) + str(time_2_period.get()).replace("교시", "")
                        time.append(time_2)

                    if time_3_days.get() != "" and time_3_period.get() != "" :
                        time_3 = str(time_3_days.get()[0]) + str(time_3_period.get()).replace("교시", "")
                        time.append(time_3)

                    if time_4_days.get() != "" and time_4_period.get() != "" :
                        time_4 = str(time_4_days.get()[0]) + str(time_4_period.get()).replace("교시", "")
                        time.append(time_4)

                    if time_5_days.get() != "" and time_5_period.get() != "" :
                        time_5 = str(time_5_days.get()[0]) + str(time_5_period.get()).replace("교시", "")
                        time.append(time_5)

                    if time_6_days.get() != "" and time_6_period.get() != "" :
                        time_6 = str(time_6_days.get()[0]) + str(time_6_period.get()).replace("교시", "")
                        time.append(time_6)

                    time = tuple(time)

                    if subject.get() == "" :
                        tkinter.messagebox.showwarning("", "과목명을 입력하세요.")
                    elif professor.get() == "" :
                        tkinter.messagebox.showwarning("", "교수명을 입력하세요.")
                    elif credit.get() == "" :
                        tkinter.messagebox.showwarning("", "학점을 선택하세요.")
                    elif type.get() == "" :
                        tkinter.messagebox.showwarning("", "이수구분을 선택하세요.")
                    elif time == "" :
                        tkinter.messagebox.showwarning("", "시간을 선택하세요.")
                    else :
                        subject_treeview.insert(parent = "", index = "end", text = "", values = (subject.get(), professor.get(), credit.get(), type.get(), time, "0"))

                        save_data() # 과목 입력 후 자동으로 저장
                        add_screen.destroy()
                    


                # 확인 버튼
                ok_button = Button(add_screen, text = "확인", bd = 0, bg = "#002C62", fg = "#FFFFFF", command = add_subject_ok, font = font_settings)
                ok_button.grid(row = 13, column = 0, columnspan = 2, sticky = N+E+W+S, padx = 10, pady = 10)

                add_screen.mainloop()



        # 과목 삭제하기
        def delete_subject() :
            subject_treeview.delete(subject_treeview.selection()[0])

            save_data() # 과목 삭제 후 자동으로 저장

        # 과목 수정하기(보완 예정)
        def modify_subject():
            delete_subject()
            add_subject() 
            
        # 과목 추가 버튼
        add_subject_button = Button(self, text = "추가", bd = 0, bg = "#002C62", fg = "#FFFFFF", width = 10, height = 1, pady = 5, font = font_settings, command = add_subject)
        add_subject_button.place(x = 308, y = 256)

        # 과목 삭제 버튼
        delete_subject_button = Button(self, text = "삭제", bd = 0, bg = "#002C62", fg = "#FFFFFF", width = 10, height = 1, pady = 5, font = font_settings, command = delete_subject)
        delete_subject_button.grid(row = 3, column = 3, sticky = "e")
        
        # 과목 수정 버튼
        modify_subject_button = Button(self, text = "수정", bd = 0, bg = "#002C62", fg = "#FFFFFF", width = 10, height = 1, pady = 5, font = font_settings, command = modify_subject)
        modify_subject_button.place(x = 406, y=256)



# 학점 계산기 페이지
class PageTwo(tkinter.Frame) :    
    def __init__(self, master) :
        Frame.__init__(self, master)
        Frame.configure(self)

        # PageOne과 동일
        font_settings = tkinter.font.Font(size = 12)

        page_one_button = Button(self, width = 12, height = 1, pady = 5, text = "수강 목록", bd = 0, bg = "#7F7F7F", fg = "#FFFFFF", font = font_settings, command = lambda : master.switch_frame(PageOne))
        page_one_button.grid(row = 1, column = 1, sticky = "w")
        
        page_two_button = Button(self, width = 12, height = 1, pady = 5, text = "학점 계산기", bd = 0, bg = "#04B3CE", fg = "#FFFFFF", font = font_settings, command = lambda : master.switch_frame(PageTwo))
        page_two_button.place(x = 116)

        page_three_button = Button(self, width = 12, height = 1, pady = 5, text = "시간표", bd = 0, bg = "#7F7F7F", fg = "#FFFFFF", font = font_settings, command = lambda : master.switch_frame(PageThree))
        page_three_button.place(x = 232)



        # PageOne과 동일
        style = ttk.Style()
        style.configure("mystyle.Treeview", font=(12))
        style.configure("mystyle.Treeview.Heading", font=(12))
        style.layout("mystyle.Treeview", [("mystyle.Treeview.treearea", {"sticky": "nswe"})])    

        subject_treeview = tkinter.ttk.Treeview(self, columns =["#1", "#2", "#3", "#4", "#5", "#6"], height = 10, selectmode = "browse", style = "mystyle.Treeview")
        subject_treeview.grid(row = 2, column = 1, columnspan = 3)

        subject_treeview.column("#0", width = 0, stretch = False)
        subject_treeview.heading("#0", text = "", anchor = W)
        subject_treeview.column("#1", width = 240, stretch = False)
        subject_treeview.heading("#1", text = "과목명", anchor = W)
        subject_treeview.column("#2", width = 120, stretch = False)
        subject_treeview.heading("#2", text = "교수명", anchor = W)
        subject_treeview.column("#3", width = 40, stretch = False)
        subject_treeview.heading("#3", text = "학점", anchor = W)
        subject_treeview.column("#4", width = 80, stretch = False)
        subject_treeview.heading("#4", text = "이수구분", anchor = W)
        subject_treeview.column("#5", width = 0, stretch = False)
        subject_treeview.heading("#5", text = "시간", anchor = W)
        subject_treeview.column("#6", width = 120, stretch = False)
        subject_treeview.heading("#6", text = "평점", anchor = W)



        # PageOne과 동일
        def open_data() :
            file = open(file = "202101.txt", mode = "r", encoding = "utf-8")
            lines = len(file.readlines())
            file.close()

            file = open(file = "202101.txt", mode = "r", encoding = "utf-8")
            for i in range(0, int(lines / 6)) :
                data = (file.readline().rstrip("\n"), 
                        file.readline().rstrip("\n"),
                        file.readline().rstrip("\n"),
                        file.readline().rstrip("\n"),
                        file.readline().rstrip("\n"),
                        file.readline().rstrip("\n"))

                subject_treeview.insert(parent = "", index = "end", text = "", values = data)


        # PageOne과 동일
        open_data()


        # PageOne과 동일
        def save_data() :
            file = open(file = "202101.txt", mode = "w", encoding = "utf-8")

            number_of_items = len(subject_treeview.get_children())

            for i in range(1, number_of_items + 1) :
                data = subject_treeview.item("I" + format(i, "03"), "values")

                file.write(data[0] + "\n")
                file.write(data[1] + "\n")
                file.write(data[2] + "\n")
                file.write(data[3] + "\n")
                file.write(data[4] + "\n")
                file.write(data[5])

                if i != number_of_items :
                    file.write("\n")

            file.close()



        # 평점 입력하기
        def add_score() :
            if subject_treeview.focus() != "" :
                add_screen = Tk()
                add_screen.title("과목 추가")
                add_screen.resizable(False, False)

                # 선택된 항목의 과목명을 불러옴
                selected_data = subject_treeview.item(subject_treeview.focus(), "values")
                selected_subject = selected_data[0]

                # 평점 항목
                subject_label = Label(add_screen, text = selected_subject, font = font_settings)
                subject_label.grid(row = 1, column = 0, sticky = W, padx = 10, pady = 10)
                score_label = Label(add_screen, text = "평점", font = font_settings)
                score_label.grid(row = 2, column = 0, sticky = W, padx = 10, pady = 10)
                score = tkinter.ttk.Combobox(add_screen, state = "readonly", height = 10, values = ["A+", "A", "B+", "B", "C+", "C", "D+", "D", "F", "P"], font = font_settings)
                score.grid(row = 2, column = 1, sticky = N+E+W+S, padx = 10, pady = 10)
                
                def add_score_ok() :
                    if score.get() == "" :
                        tkinter.messagebox.showwarning("", "시간을 선택하세요.")
                    else :
                        subject_treeview.item(subject_treeview.focus(), text = "", values = (selected_data[0], selected_data[1], selected_data[2], selected_data[3], selected_data[4], score.get()))
                        
                        save_data()
                        add_screen.destroy()

                ok_button = Button(add_screen, text = "확인", bd = 0, bg = "#002C62", fg = "#FFFFFF", command = add_score_ok, font = font_settings)
                ok_button.grid(row = 3, column = 0, columnspan = 2, sticky = N+E+W+S, padx = 10, pady = 10)

            else :
                tkinter.messagebox.showwarning("", "과목을 선택하세요.") # 선택된 항목이 없으면 경고 표시

        # 평점을 계산하는 부분 
        def calc_score() :
            file = open(file = "202101.txt", mode = "r", encoding = "utf-8")
            lines = len(file.readlines())
            file.close()
        # 배열 관련된 부분은 추후 최적화할 예정
            score=[]
            number=[]
            major=[]
            mnumber=[]
            pnumber=[]

            file = open(file = "202101.txt", mode = "r", encoding = "utf-8")
            for i in range(0, int(lines / 6)) :
                data = (file.readline().rstrip("\n"), 
                        file.readline().rstrip("\n"),
                        file.readline().rstrip("\n"),
                        file.readline().rstrip("\n"),
                        file.readline().rstrip("\n"),
                        file.readline().rstrip("\n"))
                if data[5]=="A+":
                    if data[3]=="전공":
                        major.append(4.5*int(data[2]))
                        mnumber.append(int(data[2]))
                    score.append(4.5*int(data[2]))
                    number.append(int(data[2]))
                elif data[5]=="A":
                    if data[3]=="전공":
                        major.append(4.0*int(data[2]))
                        mnumber.append(int(data[2]))                       
                    score.append(4.0*int(data[2]))
                    number.append(int(data[2]))
                elif data[5]=="B+":
                    if data[3]=="전공":
                        major.append(3.5*int(data[2]))
                        mnumber.append(int(data[2]))                       
                    score.append(3.5*int(data[2]))
                    number.append(int(data[2]))
                elif data[5]=="B":
                    if data[3]=="전공":
                        major.append(3.0*int(data[2]))
                        mnumber.append(int(data[2]))                       
                    score.append(3*int(data[2]))
                    number.append(int(data[2]))
                elif data[5]=="C+":
                    if data[3]=="전공":
                        major.append(2.5*int(data[2]))
                        mnumber.append(int(data[2]))                      
                    score.append(2.5*int(data[2]))
                    number.append(int(data[2]))
                elif data[5]=="C":
                    if data[3]=="전공":
                        major.append(2.0*int(data[2]))
                        mnumber.append(int(data[2]))                       
                    score.append(2*int(data[2]))
                    number.append(int(data[2]))
                elif data[5]=="D+":
                    if data[3]=="전공":
                        major.append(1.5*int(data[2]))
                        mnumber.append(int(data[2]))                       
                    score.append(1.5*int(data[2]))  
                    number.append(int(data[2])) 
                elif data[5]=="D":
                    if data[3]=="전공":
                        major.append(1.0*int(data[2]))
                        mnumber.append(int(data[2]))                       
                    score.append(1.0*int(data[2]))
                    number.append(int(data[2]))
                elif data[5]=="P":
                        pnumber.append(int(data[2]))
                else:
                    if data[3]=="전공":
                        major.append(0)
                        mnumber.append(int(data[2]))                    
                    score.append(0)
                    number.append(int(data[2]))          
            if sum(number)==0:
                average=0
            else:    
                average=((sum(score)/sum(number)))
            average=round(average,2)
            if sum(mnumber)==0:
                maverage=0
            else:
                maverage=((sum(major)/sum(mnumber)))
            maverage=round(maverage,2)                             
            msgbox.showinfo("평점", "총평점: "+str(average) + " 전공평점: " +str(maverage) + " 학점수: " +str(sum(number)+sum(pnumber))) 


        # 평점 입력 버튼
        add_score_button = Button(self, text = "평점 입력", bd = 0, bg = "#002C62", fg = "#FFFFFF", width = 10, height = 1, pady = 5, font = font_settings, command = add_score)
        calc_score_button = Button(self, text = "학점 계산", bd = 0, bg = "#002C62", fg = "#FFFFFF", width = 10, height = 1, pady = 5, font = font_settings, command = calc_score)
        add_score_button.grid(row = 3, column = 3, sticky = "e")
        calc_score_button.place(x = 406, y = 256) 

class PageThree(tkinter.Frame) :    
    def __init__(self, master) :
        Frame.__init__(self, master)
        Frame.configure(self)

        # PageOne과 동일
        font_settings = tkinter.font.Font(size = 12)

        page_one_button = Button(self, width = 12, height = 1, pady = 5, text = "수강 목록", bd = 0, bg = "#7F7F7F", fg = "#FFFFFF", font = font_settings, command = lambda : master.switch_frame(PageOne))
        page_one_button.grid(row = 1, column = 1, sticky = "w")
        
        page_two_button = Button(self, width = 12, height = 1, pady = 5, text = "학점 계산기", bd = 0, bg = "#04B3CE", fg = "#FFFFFF", font = font_settings, command = lambda : master.switch_frame(PageTwo))
        page_two_button.place(x = 116)

        page_three_button = Button(self, width = 12, height = 1, pady = 5, text = "시간표", bd = 0, bg = "#7F7F7F", fg = "#FFFFFF", font = font_settings, command = lambda : master.switch_frame(PageThree))
        page_three_button.place(x = 232)

        style = ttk.Style()
        style.configure("mystyle.Treeview", font=(12))
        style.configure("mystyle.Treeview.Heading", font=(12))
        style.layout("mystyle.Treeview", [("mystyle.Treeview.treearea", {"sticky": "nswe"})])    

        subject_treeview = tkinter.ttk.Treeview(self, columns =["#1", "#2"], height = 10, selectmode = "browse", style = "mystyle.Treeview")
        subject_treeview.grid(row = 2, column = 1, columnspan = 3)
        def open_data() :
            file = open(file = "202101.txt", mode = "r", encoding = "utf-8")
            lines = len(file.readlines())
            file.close()

            file = open(file = "202101.txt", mode = "r", encoding = "utf-8")
            for i in range(0, int(lines)) :
                if i%6==1:
                    data = (file.readline().rstrip("\n"))
                else:
                    continue

        open_data()
        root= Tk()
        root.title("시간표입니다")
        root.geometry("640x480+100+300") 
        root.resizable(True, True)
        row_title_label1 =  Label(root, text = '월', font = ('돋움',10),bg='#002C62', fg = '#FFFFFF',
                                relief = 'ridge', width = 14)
        row_title_label2 =  Label(root, text = '화', font = ('돋움',10),bg='#002C62', fg = '#FFFFFF',
                                relief = 'ridge', width = 14)
        row_title_label3 =  Label(root, text = '수', font = ('돋움',10),bg='#002C62', fg = '#FFFFFF',
                                relief = 'ridge', width = 14)
        row_title_label4 =  Label(root, text = '목', font = ('돋움',10),bg='#002C62', fg = '#FFFFFF',
                                relief = 'ridge', width = 14)
        row_title_label5 =  Label(root, text = '금', font = ('돋움',10),bg='#002C62', fg = '#FFFFFF',
                                relief = 'ridge', width = 14)
    
        col_title_label1 = Label(root, text = '1교시', font = ('돋움',10),bg='#002C62', fg = '#FFFFFF',
                                relief = 'ridge', width = 6, height = 2)
        col_title_label2 = Label(root, text = '2교시', font = ('돋움',10),bg='#002C62', fg = '#FFFFFF',
                                relief = 'ridge', width = 6, height = 2)
        col_title_label3 = Label(root, text = '3교시', font = ('돋움',10),bg='#002C62', fg = '#FFFFFF',
                                relief = 'ridge', width = 6, height = 2)
        col_title_label4 = Label(root, text = '4교시', font = ('돋움',10),bg='#002C62', fg = '#FFFFFF',
                                relief = 'ridge', width = 6, height = 2)
        col_title_label5 = Label(root, text = '5교시', font = ('돋움',10),bg='#002C62', fg = '#FFFFFF',
                                relief = 'ridge', width = 6, height = 2)
        col_title_label6 = Label(root, text = '6교시', font = ('돋움',10),bg='#002C62', fg = '#FFFFFF',
                                relief = 'ridge', width = 6, height = 2)
        col_title_label7 = Label(root, text = '7교시', font = ('돋움',10),bg='#002C62', fg = '#FFFFFF',
                                relief = 'ridge', width = 6, height = 2)
        col_title_label8 = Label(root, text = '8교시', font = ('돋움',10),bg='#002C62', fg = '#FFFFFF',
                                relief = 'ridge', width = 6, height = 2)
        col_title_label9 = Label(root, text = '9교시', font = ('돋움',10),bg='#002C62', fg = '#FFFFFF',
                                relief = 'ridge', width = 6, height = 2)
        col_title_label10 = Label(root, text = '10교시', font = ('돋움',10),bg='#002C62', fg = '#FFFFFF',
                                relief = 'ridge', width = 6, height = 2)
 
        text_1 = Text(root, width = 14, height = 2)
        text_2 = Text(root, width = 14, height = 2)
        text_3 = Text(root, width = 14, height = 2)
        text_4 = Text(root, width = 14, height = 2)
        text_5 = Text(root, width = 14, height = 2)
        text_6 = Text(root, width = 14, height = 2)
        text_7 = Text(root, width = 14, height = 2)
        text_8 = Text(root, width = 14, height = 2)
        text_9 = Text(root, width = 14, height = 2)
        text_10 = Text(root, width = 14, height = 2)

        text_11 = Text(root, width = 14, height = 2)
        text_12 = Text(root, width = 14, height = 2)
        text_13 = Text(root, width = 14, height = 2)
        text_14 = Text(root, width = 14, height = 2)
        text_15 = Text(root, width = 14, height = 2)
        text_16 = Text(root, width = 14, height = 2)
        text_17 = Text(root, width = 14, height = 2)
        text_18 = Text(root, width = 14, height = 2)
        text_19 = Text(root, width = 14, height = 2)
        text_20 = Text(root, width = 14, height = 2)
    
        text_21 = Text(root, width = 14, height = 2)
        text_22 = Text(root, width = 14, height = 2)
        text_23 = Text(root, width = 14, height = 2)
        text_24 = Text(root, width = 14, height = 2)
        text_25 = Text(root, width = 14, height = 2)
        text_26 = Text(root, width = 14, height = 2)
        text_27 = Text(root, width = 14, height = 2)
        text_28 = Text(root, width = 14, height = 2)
        text_29 = Text(root, width = 14, height = 2)
        text_30 = Text(root, width = 14, height = 2)

        text_31 = Text(root, width = 14, height = 2)
        text_32 = Text(root, width = 14, height = 2)
        text_33 = Text(root, width = 14, height = 2)
        text_34 = Text(root, width = 14, height = 2)
        text_35 = Text(root, width = 14, height = 2)
        text_36 = Text(root, width = 14, height = 2)
        text_37 = Text(root, width = 14, height = 2)
        text_38 = Text(root, width = 14, height = 2)
        text_39 = Text(root, width = 14, height = 2)
        text_40 = Text(root, width = 14, height = 2)

        text_41 = Text(root, width = 14, height = 2)
        text_42 = Text(root, width = 14, height = 2)
        text_43 = Text(root, width = 14, height = 2)
        text_44 = Text(root, width = 14, height = 2)
        text_45 = Text(root, width = 14, height = 2)
        text_46 = Text(root, width = 14, height = 2)
        text_47 = Text(root, width = 14, height = 2)
        text_48 = Text(root, width = 14, height = 2)
        text_49 = Text(root, width = 14, height = 2)
        text_50 = Text(root, width = 14, height = 2)

        row_title_label1.grid(column = 1, row = 0)
        row_title_label2.grid(column = 2, row = 0)
        row_title_label3.grid(column = 3, row = 0)
        row_title_label4.grid(column = 4, row = 0)
        row_title_label5.grid(column = 5, row = 0)
    
        col_title_label1.grid(column = 0, row = 1)
        col_title_label2.grid(column = 0, row = 2)
        col_title_label3.grid(column = 0, row = 3)
        col_title_label4.grid(column = 0, row = 4)
        col_title_label5.grid(column = 0, row = 5)
        col_title_label6.grid(column = 0, row = 6)
        col_title_label7.grid(column = 0, row = 7)
        col_title_label8.grid(column = 0, row = 8)
        col_title_label9.grid(column = 0, row = 9)
        col_title_label10.grid(column = 0, row = 10)
    

        text_1.grid(column = 1, row = 1)
        text_2.grid(column = 1, row = 2)
        text_3.grid(column = 1, row = 3)
        text_4.grid(column = 1, row = 4)
        text_5.grid(column = 1, row = 5)
        text_6.grid(column = 1, row = 6)
        text_7.grid(column = 1, row = 7)
        text_8.grid(column = 1, row = 8)
        text_9.grid(column = 1, row = 9)
        text_10.grid(column = 1, row = 10)

        text_11.grid(column = 2, row = 1)
        text_12.grid(column = 2, row = 2)
        text_13.grid(column = 2, row = 3)
        text_14.grid(column = 2, row = 4)
        text_15.grid(column = 2, row = 5)
        text_16.grid(column = 2, row = 6)
        text_17.grid(column = 2, row = 7)
        text_18.grid(column = 2, row = 8)
        text_19.grid(column = 2, row = 9)
        text_20.grid(column = 2, row = 10)

        text_21.grid(column = 3, row = 1)
        text_22.grid(column = 3, row = 2)
        text_23.grid(column = 3, row = 3)
        text_24.grid(column = 3, row = 4)
        text_25.grid(column = 3, row = 5)
        text_26.grid(column = 3, row = 6)
        text_27.grid(column = 3, row = 7)
        text_28.grid(column = 3, row = 8)
        text_29.grid(column = 3, row = 9)
        text_30.grid(column = 3, row = 10)

        text_31.grid(column = 4, row = 1)
        text_32.grid(column = 4, row = 2)
        text_33.grid(column = 4, row = 3)
        text_34.grid(column = 4, row = 4)
        text_35.grid(column = 4, row = 5)
        text_36.grid(column = 4, row = 6)
        text_37.grid(column = 4, row = 7)
        text_38.grid(column = 4, row = 8)
        text_39.grid(column = 4, row = 9)
        text_40.grid(column = 4, row = 10)

        text_41.grid(column = 5, row = 1)
        text_42.grid(column = 5, row = 2)
        text_43.grid(column = 5, row = 3)
        text_44.grid(column = 5, row = 4)
        text_45.grid(column = 5, row = 5)
        text_46.grid(column = 5, row = 6)
        text_47.grid(column = 5, row = 7)
        text_48.grid(column = 5, row = 8)
        text_49.grid(column = 5, row = 9)
        text_50.grid(column = 5, row = 10)
        
        filename="시간표.txt"
        def open_data() :
            if os.path.isfile(filename):
                with open(filename, "r", encoding="utf8") as file:
                    line=file.readline()
                    text_1.insert("end",line)
                    line=file.readline()
                    text_2.insert("end",line)
                    line=file.readline()
                    text_3.insert("end",line)
                    line=file.readline()
                    text_4.insert("end",line)
                    line=file.readline()
                    text_5.insert("end",line)
                    line=file.readline()
                    text_6.insert("end",line)
                    line=file.readline()
                    text_7.insert("end",line)
                    line=file.readline()
                    text_8.insert("end",line)
                    line=file.readline()
                    text_9.insert("end",line)
                    line=file.readline()
                    text_10.insert("end",line)
                    line=file.readline()
                    text_11.insert("end",line)
                    line=file.readline()
                    text_12.insert("end",line)
                    line=file.readline()
                    text_13.insert("end",line)
                    line=file.readline()
                    text_14.insert("end",line)
                    line=file.readline()
                    text_15.insert("end",line)
                    line=file.readline()
                    text_16.insert("end",line)
                    line=file.readline()
                    text_17.insert("end",line)
                    line=file.readline()
                    text_18.insert("end",line)
                    line=file.readline()
                    text_19.insert("end",line)
                    line=file.readline()
                    text_20.insert("end",line)
                    line=file.readline()
                    text_21.insert("end",line)
                    line=file.readline()
                    text_22.insert("end",line)
                    line=file.readline()
                    text_23.insert("end",line)
                    line=file.readline()
                    text_24.insert("end",line)
                    line=file.readline()
                    text_25.insert("end",line)
                    line=file.readline()
                    text_26.insert("end",line)
                    line=file.readline()
                    text_27.insert("end",line)
                    line=file.readline()
                    text_28.insert("end",line)
                    line=file.readline()
                    text_29.insert("end",line)
                    line=file.readline()
                    text_30.insert("end",line)
                    line=file.readline()
                    text_31.insert("end",line)
                    line=file.readline()
                    text_32.insert("end",line)
                    line=file.readline()
                    text_33.insert("end",line) 
                    line=file.readline()
                    text_34.insert("end",line)
                    line=file.readline()
                    text_35.insert("end",line)
                    line=file.readline()
                    text_36.insert("end",line)
                    line=file.readline()
                    text_37.insert("end",line)
                    line=file.readline()
                    text_38.insert("end",line)
                    line=file.readline()
                    text_39.insert("end",line)
                    line=file.readline()
                    text_40.insert("end",line)
                    line=file.readline()
                    text_41.insert("end",line)
                    line=file.readline()
                    text_42.insert("end",line)
                    line=file.readline()
                    text_43.insert("end",line)
                    line=file.readline()
                    text_44.insert("end",line)
                    line=file.readline()
                    text_45.insert("end",line)
                    line=file.readline()
                    text_46.insert("end",line)
                    line=file.readline()
                    text_47.insert("end",line)
                    line=file.readline()
                    text_48.insert("end",line)
                    line=file.readline()
                    text_49.insert("end",line)
                    line=file.readline()
                    text_50.insert("end",line)
            file.close()

        def save_data() :
            with open(filename, "w", encoding="utf8") as file:
                file.write(text_1.get("1.0", "end"))
                file.write(text_2.get("1.0", "end"))
                file.write(text_3.get("1.0", "end"))
                file.write(text_4.get("1.0", "end"))
                file.write(text_5.get("1.0", "end"))
                file.write(text_6.get("1.0", "end"))
                file.write(text_7.get("1.0", "end"))
                file.write(text_8.get("1.0", "end"))
                file.write(text_9.get("1.0", "end"))
                file.write(text_10.get("1.0", "end"))
                file.write(text_11.get("1.0", "end"))
                file.write(text_12.get("1.0", "end"))
                file.write(text_13.get("1.0", "end"))
                file.write(text_14.get("1.0", "end"))
                file.write(text_15.get("1.0", "end"))
                file.write(text_16.get("1.0", "end"))
                file.write(text_17.get("1.0", "end"))
                file.write(text_18.get("1.0", "end"))
                file.write(text_19.get("1.0", "end"))
                file.write(text_20.get("1.0", "end"))  
                file.write(text_21.get("1.0", "end"))
                file.write(text_22.get("1.0", "end"))
                file.write(text_23.get("1.0", "end"))
                file.write(text_24.get("1.0", "end"))
                file.write(text_25.get("1.0", "end"))
                file.write(text_26.get("1.0", "end"))
                file.write(text_27.get("1.0", "end"))
                file.write(text_28.get("1.0", "end"))
                file.write(text_29.get("1.0", "end"))
                file.write(text_30.get("1.0", "end"))  
                file.write(text_31.get("1.0", "end"))
                file.write(text_32.get("1.0", "end"))
                file.write(text_33.get("1.0", "end"))
                file.write(text_34.get("1.0", "end"))
                file.write(text_35.get("1.0", "end"))
                file.write(text_36.get("1.0", "end"))
                file.write(text_37.get("1.0", "end"))
                file.write(text_38.get("1.0", "end"))
                file.write(text_39.get("1.0", "end"))
                file.write(text_40.get("1.0", "end"))  
                file.write(text_41.get("1.0", "end"))
                file.write(text_42.get("1.0", "end"))
                file.write(text_43.get("1.0", "end"))
                file.write(text_44.get("1.0", "end"))
                file.write(text_45.get("1.0", "end"))
                file.write(text_46.get("1.0", "end"))
                file.write(text_47.get("1.0", "end"))
                file.write(text_48.get("1.0", "end"))
                file.write(text_49.get("1.0", "end"))
                file.write(text_50.get("1.0", "end"))          


        open_button = Button(root, text = '불러오기', command=open_data)
        open_button.grid(column = 9, row = 9, padx = 5, pady=5)
        save_button = Button(root, text = '저장하기', command=save_data)
        save_button.grid(column = 9, row = 10, padx = 5, pady=5)
            
App().mainloop()
