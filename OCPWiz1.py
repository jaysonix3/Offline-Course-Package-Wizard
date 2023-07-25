import base64
import copy
import json
import os
import random
import re
import shutil
import sys
import tkinter as tk
from bs4 import BeautifulSoup
from tkinter import filedialog
from tkinter import ttk

class CourseManagementApp:
    def __init__(self, root):
        self.root = root
        self.faculty = ""
        self.course_no = ""
        self.course_title = ""
        self.course_intro=[]
        self.course_guide_dir = ""
        self.resources_dir=[]
        self.num_topics = 0
        self.topics_dir = {}
        self.num_questions = {}
        self.questions = {}
        
        self.template_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))

        self.options_frame = tk.Frame(root,bg="#8A1538")
        self.options_frame.pack(side=tk.LEFT)
        self.options_frame.pack_propagate(False)
        self.options_frame.configure(width=150,height=450)

        self.buttons_frame = tk.Frame(self.options_frame,bg="#8A1538")
        self.buttons_frame.pack(side=tk.RIGHT)

        self.course_info_nd = tk.Label(self.buttons_frame,height=2,bg="#8A1538")
        self.course_info_nd.grid(row=1, column=1,pady=10)

        self.course_intro_nd = tk.Label(self.buttons_frame,height=2,bg="#8A1538")
        self.course_intro_nd.grid(row=2, column=1,pady=10)

        self.resources_nd = tk.Label(self.buttons_frame,height=2,bg="#8A1538")
        self.resources_nd.grid(row=3, column=1,pady=10)

        self.num_topics_nd = tk.Label(self.buttons_frame,height=2,bg="#8A1538")
        self.num_topics_nd.grid(row=4, column=1,pady=10)

        self.upload_topics_nd = tk.Label(self.buttons_frame,height=2,bg="#8A1538")
        self.upload_topics_nd.grid(row=5, column=1,pady=10)

        self.create_quiz_nd = tk.Label(self.buttons_frame,height=2,bg="#8A1538")
        self.create_quiz_nd.grid(row=6, column=1,pady=10)

        self.create_ocp_nd = tk.Label(self.buttons_frame,height=2,bg="#8A1538")
        self.create_ocp_nd.grid(row=7, column=1,pady=10)

        self.course_info_btn = tk.Button(self.buttons_frame,
                                    text="Course Information",width=15,height=1,font=('Helvetica', 10),bg="#8A1538",fg="#EEEEEE",activebackground='#975361',
                                    borderwidth=0,anchor="w",
                                    command=lambda: self.indicate(self.course_info_nd, self.course_info_page))
        self.course_info_btn.grid(row=1, column=2, columnspan=2,pady=10)

        self.course_intro_btn = tk.Button(self.buttons_frame,
                                    text="Course Intro",width=15,height=1,font=('Helvetica', 10),bg="#8A1538",fg="#EEEEEE",activebackground='#975361',
                                    borderwidth=0,anchor="w",state="disabled",
                                    command=lambda: self.indicate(self.course_intro_nd, self.course_intro_page))
        self.course_intro_btn.grid(row=2, column=2, columnspan=2,pady=10)

        self.resources_btn = tk.Button(self.buttons_frame,
                                    text="Resources",width=15,height=1,font=('Helvetica', 10),bg="#8A1538",fg="#EEEEEE",activebackground='#975361',
                                    borderwidth=0,anchor="w",state="disabled",
                                    command=lambda: self.indicate(self.resources_nd,self.resources_page))
        self.resources_btn.grid(row=3, column=2, columnspan=2,pady=10)

        self.num_topics_btn = tk.Button(self.buttons_frame,
                                    text="Number of Topics",width=15,height=1,font=('Helvetica', 10),bg="#8A1538",fg="#EEEEEE",activebackground='#975361',
                                    borderwidth=0,anchor="w",state="disabled",
                                    command=lambda: self.indicate(self.num_topics_nd,self.num_topics_page))
        self.num_topics_btn.grid(row=4, column=2, columnspan=2,pady=10)

        self.upload_topics_btn = tk.Button(self.buttons_frame,
                                    text="Upload Topics PDF",width=15,height=1,font=('Helvetica', 10),bg="#8A1538",fg="#EEEEEE",activebackground='#975361',
                                    borderwidth=0,anchor="w",state="disabled",
                                    command=lambda: self.indicate(self.upload_topics_nd,self.upload_topics_page))
        self.upload_topics_btn.grid(row=5, column=2, columnspan=2,pady=10)

        self.create_quiz_btn = tk.Button(self.buttons_frame,
                                    text="Create Quiz",width=15,height=1,font=('Helvetica', 10),bg="#8A1538",fg="#EEEEEE",activebackground='#975361',
                                    borderwidth=0,anchor="w",state="disabled",
                                    command=lambda: self.indicate(self.create_quiz_nd,self.create_quiz_page))
        self.create_quiz_btn.grid(row=6, column=2, columnspan=2,pady=10)

        self.create_ocp_btn = tk.Button(self.buttons_frame,
                                    text="Create OCP",width=15,height=1,font=('Helvetica', 10),bg="#8A1538",fg="#EEEEEE",activebackground='#975361',
                                    borderwidth=0,anchor="w",
                                    command=lambda: self.indicate(self.create_ocp_nd,self.create_ocp_page))
        self.create_ocp_btn.grid(row=7, column=2, columnspan=2,pady=10)

        self.main_frame = tk.Frame(root,highlightbackground='black',highlightthickness=2)
        self.main_frame.pack_propagate(False)
        self.main_frame.configure(width=600,height=450)
        self.main_frame.pack(side=tk.LEFT)

    def indicate(self,nd,page):
        self.not_indicate()
        nd.config(bg="#00573F")
        page()

    def enable_btn(self,type):
        if type=="course_info":
            self.course_intro_btn.config(state="normal")
            self.resources_btn.config(state="normal")
            self.num_topics_btn.config(state="normal")
        if type=="topics":
            self.upload_topics_btn.config(state="normal")
            self.create_quiz_btn.config(state="normal")

    def not_indicate(self):
        self.course_info_nd.config(bg="#8A1538")
        self.course_intro_nd.config(bg="#8A1538")
        self.resources_nd.config(bg="#8A1538")
        self.num_topics_nd.config(bg="#8A1538")
        self.upload_topics_nd.config(bg="#8A1538")
        self.create_quiz_nd.config(bg="#8A1538")
        self.create_ocp_nd.config(bg="#8A1538")

        for x in self.main_frame.winfo_children():
            x.destroy()

    def course_info_page(self):
        course_info_page=tk.Frame(self.main_frame)
        course_info_page.place(relx=.5, rely=.5,anchor= tk.CENTER)

        faculty_label=tk.Label(course_info_page, text="Faculty:",font=('Helvtica',12))
        faculty_label.grid(row=1,column=1,sticky=tk.W,pady=10)

        clicked = tk.StringVar()
        
        faculty_cb=ttk.Combobox(course_info_page,state='readonly',textvariable=clicked,font=('Helvtica',12),width=27)
        faculty_cb.grid(row=1,column=2,sticky=tk.E,pady=10)

        faculty_cb['values'] = (
                "Faculty of Education",
                "Faculty of Information and Communication Studies",
                "Faculty of Management and Development Studies",
            )
        faculty_cb.current()

        course_no_label=tk.Label(course_info_page, text="Course No:",font=('Helvtica',12))
        course_no_label.grid(row=2,column=1,sticky=tk.W,pady=10)

        course_no_entry=tk.Entry(course_info_page,font=('Helvtica',12),width=29,bg="#00573F",fg="#EEEEEE")
        course_no_entry.grid(row=2,column=2,sticky=tk.E,pady=10)

        course_title_label=tk.Label(course_info_page, text="Course Title:",font=('Helvtica',12))
        course_title_label.grid(row=3,column=1,sticky=tk.W,pady=10)

        course_title_entry=tk.Entry(course_info_page,font=('Helvtica',12),width=29,bg="#00573F",fg="#EEEEEE")
        course_title_entry.grid(row=3,column=2,sticky=tk.E,pady=10)

        if self.faculty != "":
            clicked.set(self.faculty)
        if self.course_no != "":
            course_no_entry.insert(0,self.course_no)
        if self.course_title != "":
            course_title_entry.insert(0,self.course_title)

        save_btn=tk.Button(course_info_page,text="Save", font=('Helvetica',12),width=14,bg="#8A1538",fg="#EEEEEE",activebackground='#975361',
                        command=lambda: save())
        save_btn.grid(row=4,column=2,sticky=tk.E,pady=10)

        def save():
            if clicked.get() == "" or course_no_entry.get() == "" or course_title_entry.get() == "":
                tk.messagebox.showerror('Error', 'Error: Missing fields')
            else:
                self.faculty = clicked.get()
                self.course_no=course_no_entry.get()
                self.course_title=course_title_entry.get()
                self.enable_btn("course_info")

    def course_intro_page(self):
        course_intro_page=tk.Frame(self.main_frame)
        course_intro_page.place(relx=.5, rely=.5,anchor= tk.CENTER)

        course_intro_label=tk.Label(course_intro_page, text="Course Introduction:",font=('Helvtica',12))
        course_intro_label.grid(row=1,column=1,sticky=tk.W,pady=10)

        text_frame=tk.Frame(course_intro_page)

        scrollbar=tk.Scrollbar(text_frame)

        course_intro_text=tk.Text(text_frame,yscrollcommand = scrollbar.set,width=45,height=10,font=('Helvtica',12),bg="#00573F",fg="#EEEEEE")
        course_intro_text.grid(row=0,column=0)

        scrollbar.grid(row=0,column=1,sticky="NS")
        scrollbar.config( command = course_intro_text.yview )

        text_frame.grid(row=2, column=1, pady=10)

        if self.course_intro:
            for x in range(len(self.course_intro)):
                if x+1 != len(self.course_intro):
                    course_intro_text.insert(tk.END, self.course_intro[x] + "\n")
                else:
                    course_intro_text.insert(tk.END, self.course_intro[x])

        save_btn=tk.Button(course_intro_page,text="Save", font=('Helvetica',12),width=14,bg="#8A1538",fg="#EEEEEE",activebackground='#975361',
                        command=lambda: save())
        save_btn.grid(row=3,column=1,sticky=tk.E,pady=10)

        def save():
            temp=course_intro_text.get("1.0", 'end-1c').strip()
            course_intro_temp = [temp1.strip() for temp1 in temp.split('\n') if temp1.strip()]
            if not course_intro_temp:
                msg_box = tk.messagebox.askokcancel("Empty", "No Course Information\nAre you sure?")
                if msg_box:
                    self.course_intro =course_intro_temp
            else:
                self.course_intro=course_intro_temp

    def resources_page(self):
        resources_page=tk.Frame(self.main_frame)
        resources_page.place(relx=.5, rely=.5,anchor= tk.CENTER)

        course_guide_btn = tk.Button(resources_page,text="Upload Course Guide", font=('Helvetica',12),width=30,bg="#8A1538",fg="#EEEEEE",activebackground='#975361',
                        command=lambda: course_guide_save())
        course_guide_btn.grid(row=1,column=1,sticky=tk.W,pady=10)

        if self.course_guide_dir != "":
            course_guide_btn.config(text="Change Course Guide")

        resources_btn = tk.Button(resources_page,text="Add Folders", font=('Helvetica',12),width=30,bg="#8A1538",fg="#EEEEEE",activebackground='#975361',
                        command=lambda: folder_save())
        resources_btn.grid(row=2,column=1,sticky=tk.W,pady=10)

        files_btn = tk.Button(resources_page,text="Add Files", font=('Helvetica',12),width=30,bg="#8A1538",fg="#EEEEEE",activebackground='#975361',
                        command=lambda: file_save())
        files_btn.grid(row=3,column=1,sticky=tk.W,pady=10)

        files_btn = tk.Button(resources_page,text="Remove Resources", font=('Helvetica',12),width=30,bg="#8A1538",fg="#EEEEEE",activebackground='#975361',
                        command=lambda: remove_resources())
        files_btn.grid(row=4,column=1,sticky=tk.W,pady=10)
        
        def course_guide_save():
            source = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                filetype=(("PDF", "*.pdf"), ("All Files", "*.*")))
            if source:
                self.course_guide_dir=source
                course_guide_btn.config(text="Change Course Guide")
            else:
                tk.messagebox.showerror("Error", "No file selected")

        def folder_save():
            path = '{}'.format(filedialog.askdirectory(title='Select Folder'))
            if path:
                if path in self.resources_dir:
                    tk.messagebox.showerror("Error", "Folder already added")
                else:
                    self.resources_dir.append([path, 0])
            else:
                tk.messagebox.showerror("Error", "No folder selected")

        def file_save():
            source = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                filetypes=(("All Files", ""),))
            if source:
                if source in self.resources_dir:
                    tk.messagebox.showerror("Error", "File already added")
                else:
                    self.resources_dir.append([source,1])
            else:
                tk.messagebox.showerror("Error", "No file selected")

        def remove_resources():
            if len(self.resources_dir) == 0:
                tk.messagebox.showerror("Error", "No resources available")
            else:
                self.remove_resources_page()

    def remove_resources_page(self):
        for x in self.main_frame.winfo_children():
            x.destroy()

        remove_resources_page=tk.Frame(self.main_frame)
        remove_resources_page.place(relx=.5, rely=.5,anchor= tk.CENTER)

        lb = tk.Listbox(remove_resources_page,width=45,font=('Helvetica',12))

        for x in range(0,len(self.resources_dir)):
            lb.insert(x, self.resources_dir[x])
        
        lb.grid(row=1,column=1,sticky="EW",pady=10)

        delete_btn=tk.Button(remove_resources_page,text="Delete",font=('Helvetica',12),width=14,bg="#8A1538",fg="#EEEEEE",activebackground='#975361',
                                    command=lambda: delete())
        delete_btn.grid(row=2,column=1,sticky=tk.E)
        
        def delete():
            selection = lb.curselection()
            lb.delete(selection[0])
            del(self.resources_dir[selection[0]])
            
            if lb.size()==0:
                self.indicate(self.resources_nd,self.resources_page)

    def num_topics_page(self):
        num_topics_page=tk.Frame(self.main_frame)
        num_topics_page.place(relx=.5, rely=.5,anchor= tk.CENTER)

        num_topics_label=tk.Label(num_topics_page, text="No of Topics:",font=('Helvtica',12))
        num_topics_label.grid(row=1,column=1,sticky=tk.W,pady=10)

        num_topics_entry=tk.Entry(num_topics_page,justify=tk.CENTER,font=('Helvtica',12),width=29,bg="#00573F",fg="#EEEEEE")
        num_topics_entry.grid(row=1,column=2,sticky=tk.E,pady=10)

        if self.num_topics > 0:
            num_topics_entry.insert(0,self.num_topics)

        save_btn=tk.Button(num_topics_page,text="Save", font=('Helvetica',12),width=14,bg="#8A1538",fg="#EEEEEE",activebackground='#975361',
                        command=lambda: save())
        save_btn.grid(row=2,column=2,sticky=tk.E,pady=10)

        def save():
            if self.num_topics == 0:
                if num_topics_entry.get().isdigit() == True:
                    if int(num_topics_entry.get()) < 1:
                        tk.messagebox.showerror("Error","Please enter a valid number.")
                    else:
                        self.num_topics = int(num_topics_entry.get())
                        temp = []
                        for x in range(self.num_topics):
                            temp.append(x+1)
                        self.topics_dir = dict.fromkeys(temp)
                        self.num_questions = dict.fromkeys(temp)
                        self.num_questions["final"] = None
                        self.questions = dict.fromkeys(temp)
                        self.questions["final"]=None
                        self.enable_btn("topics")
                else:
                    tk.messagebox.showerror("Error","Please enter only digits as no of topics!")
            elif int(num_topics_entry.get()) != self.num_topics:
                msg_box = tk.messagebox.askokcancel("Warning", "Changing the number of topics will remove the uploaded PDFs and Questions\nContinue?")
                if msg_box:
                    self.topics_dir.clear()
                    self.num_questions.clear()
                    self.questions.clear()
                    if num_topics_entry.get().isdigit() == True:
                        if int(num_topics_entry.get()) < 1:
                            tk.messagebox.showerror("Error","Please enter a valid number.")
                        else:
                            self.num_topics = int(num_topics_entry.get())
                            temp = []
                            for x in range(self.num_topics):
                                temp.append(x+1)
                            self.topics_dir = dict.fromkeys(temp)
                            self.num_questions = dict.fromkeys(temp)
                            self.num_questions["final"] = None
                            self.questions = dict.fromkeys(temp)
                            self.questions["final"]=None
                            self.enable_btn("topics")
                    else:
                        tk.messagebox.showerror("Error","Please enter only digits as no of topics!")
            else:
                self.enable_btn("topics")
    
    def upload_topics_page(self):
        upload_topics_page=tk.Frame(self.main_frame)
        upload_topics_page.place(relx=.5, rely=.5,anchor= tk.CENTER)
        
        canvas = tk.Canvas(upload_topics_page)
        canvas.grid(row=1,column=1, pady=10)
        scrollbar = tk.Scrollbar(upload_topics_page, orient="vertical", command=canvas.yview)
        scrollbar.grid(row=1, column=2, sticky="NS")
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        for x in range(self.num_topics):
            button_text = ""
            if bool(self.topics_dir) and self.topics_dir[x+1] != None:
                button_text = "Change Topic " + str(x+1) + " PDF"
            else:
                button_text = "Upload Topic " + str(x+1) + " PDF"
            button = tk.Button(scrollable_frame, text=button_text,font=('Helvetica',12),width=30,bg="#8A1538",fg="#EEEEEE",activebackground='#975361',
                            command=lambda value=x+1: button_click(value))
            button.grid(row=x+1,column=1,sticky=tk.E,pady=10)
            
        def button_click(value):
            if bool(self.topics_dir):
                source = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                filetype=(("PDF", "*.pdf"), ("All Files", "*.*")))
                if source:
                    if self.topics_dir[value] == None:
                        self.topics_dir[value] = source
                    else:
                        # print(topics_dir[value])
                        msg_box = tk.messagebox.askyesno("Replace Topic " + str(value+1) + " PDF", "Replace")
                        if msg_box == 'yes':
                            self.topics_dir[value] = source
                    self.indicate(self.upload_topics_nd, self.upload_topics_page)
                else:
                    tk.messagebox.showerror("Error", "No file selected")

    def create_quiz_page(self):
        create_quiz_page=tk.Frame(self.main_frame)
        create_quiz_page.place(relx=.5, rely=.5,anchor= tk.CENTER)
        
        canvas = tk.Canvas(create_quiz_page)
        canvas.grid(row=1,column=1, pady=10)
        scrollbar = tk.Scrollbar(create_quiz_page, orient="vertical", command=canvas.yview)
        scrollbar.grid(row=1, column=2, sticky="NS")
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        for x in range(self.num_topics):
            button_text = ""
            if bool(self.num_questions) and self.num_questions[x+1] != None:
                button_text = "Change Quiz " + str(x+1)
            else:
                button_text = "Create Quiz " + str(x+1)
            button = tk.Button(scrollable_frame, text=button_text,font=('Helvetica',12),width=30,bg="#8A1538",fg="#EEEEEE",activebackground='#975361',
                            command=lambda value=x+1: button_click(value))
            button.grid(row=x+1,column=1,sticky=tk.E,pady=10)
            button_text_final = ""
            if bool(self.num_questions) and self.num_questions[x+1] != None:
                button_text_final = "Change Final Quiz" 
            else:
                button_text_final = "Create Final Quiz"
            button_final = tk.Button(scrollable_frame, text=button_text_final, font=('Helvetica',12),width=30,bg="#8A1538",fg="#EEEEEE",activebackground='#975361',
                                    command=lambda value="final": button_click(value))
            button_final.grid(row=self.num_topics+2,column=1,sticky=tk.E,pady=10)

        def button_click(quiz_no):
            self.num_questions_page(quiz_no)

    def num_questions_page(self,quiz_no):
        for x in self.main_frame.winfo_children():
            x.destroy()
        
        num_questions_page=tk.Frame(self.main_frame)
        num_questions_page.place(relx=.5, rely=.5,anchor= tk.CENTER)

        num_questions_label=tk.Label(num_questions_page, text="No of Questions: ",font=('Helvtica',12))
        num_questions_label.grid(row=1,column=1,sticky=tk.W,pady=10)

        num_questions_entry=tk.Entry(num_questions_page,justify=tk.CENTER,font=('Helvtica',12),width=29,bg="#00573F",fg="#EEEEEE")
        num_questions_entry.grid(row=1,column=2,sticky=tk.E,pady=10)

        if self.num_questions[quiz_no] != None:
            num_questions_entry.insert(0,str(self.num_questions[quiz_no]))

        save_btn=tk.Button(num_questions_page,text="Save", font=('Helvetica',12),width=14,bg="#8A1538",fg="#EEEEEE",activebackground='#975361',
                        command=lambda: save(quiz_no))
        save_btn.grid(row=2,column=2,sticky=tk.E,pady=10)

        def save(quiz_no):
            num = int(num_questions_entry.get())
            if self.num_questions[quiz_no] != None:
                if self.num_questions[quiz_no] != num:
                    msg_box = tk.messagebox.askokcancel("Warning", "Changing the number of questions will delete the previous quiz\nContinue?")
                    if msg_box:
                        self.num_questions[quiz_no] = num
                        self.questions[quiz_no] = None
                        self.questionnaire_page(quiz_no,num)
                else:
                    self.questionnaire_page(quiz_no, num)
            else:
                self.questionnaire_page(quiz_no, num)

    def questionnaire_page(self,quiz_no,num_questions):
        for x in self.main_frame.winfo_children():
            x.destroy()

        questionnaire_page=tk.Frame(self.main_frame)
        questionnaire_page.place(relx=.5, rely=.5,anchor= tk.CENTER)
        
        canvas = tk.Canvas(questionnaire_page)
        canvas.grid(row=1,column=1, pady=10)
        scrollbar = tk.Scrollbar(questionnaire_page, orient="vertical", command=canvas.yview)
        scrollbar.grid(row=1, column=2, sticky="NS")
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        for x in range(num_questions):
            question_frame = tk.Frame(scrollable_frame,highlightbackground='black',highlightthickness=2)
            question_frame.pack(pady=5)
            #QUESTIONS ------------------------------------------------------------------------------------------------
            question_label = tk.Label(question_frame, text=f"Question {x+1}",font=('Helvtica',12))
            question_label.grid(row=1,column=1,sticky=tk.W,pady=10)

            text_frame1=tk.Frame(question_frame)

            scrollbar1=tk.Scrollbar(text_frame1)

            question_text=tk.Text(text_frame1,yscrollcommand = scrollbar1.set,width=39,height=3,font=('Helvtica',12),bg="#00573F",fg="#EEEEEE")
            question_text.grid(row=0,column=0)

            scrollbar1.grid(row=0,column=1,sticky="NS")
            scrollbar1.config( command = question_text.yview )

            text_frame1.grid(row=2, column=1, pady=10)
            #CHOICES ------------------------------------------------------------------------------------------------
            choices_label = tk.Label(question_frame, text="Choices",font=('Helvtica',12))
            choices_label.grid(row=3,column=1,sticky=tk.W,pady=10)

            text_frame2=tk.Frame(question_frame)

            scrollbar2=tk.Scrollbar(text_frame2)

            choices_text=tk.Text(text_frame2,yscrollcommand = scrollbar2.set,width=39,height=3,font=('Helvtica',12),bg="#00573F",fg="#EEEEEE")
            choices_text.grid(row=0,column=0)

            scrollbar2.grid(row=0,column=1,sticky="NS")
            scrollbar2.config( command = choices_text.yview )

            text_frame2.grid(row=4, column=1, pady=10)
            #ANSWERS ------------------------------------------------------------------------------------------------
            answers_label = tk.Label(question_frame, text="Correct Answer(s)",font=('Helvtica',12))
            answers_label.grid(row=5,column=1,sticky=tk.W,pady=10)

            text_frame3=tk.Frame(question_frame)

            scrollbar3=tk.Scrollbar(text_frame3)

            answers_text=tk.Text(text_frame3,yscrollcommand = scrollbar3.set,width=39,height=3,font=('Helvtica',12),bg="#00573F",fg="#EEEEEE")
            answers_text.grid(row=0,column=0)

            scrollbar3.grid(row=0,column=1,sticky="NS")
            scrollbar3.config( command = choices_text.yview )

            text_frame3.grid(row=6, column=1, pady=10)

            if self.questions[quiz_no] != None:
                if self.questions[quiz_no][x]['label']:
                    question_text.insert(tk.END, self.questions[quiz_no][x]['label'])
                if self.questions[quiz_no][x]['options']:
                    for y in range(len(self.questions[quiz_no][x]['options'])):
                        if y+1 != len(self.questions[quiz_no][x]['options']):
                            choices_text.insert(tk.END, self.questions[quiz_no][x]['options'][y] + "\n")
                        else:
                            choices_text.insert(tk.END, self.questions[quiz_no][x]['options'][y])
                if self.questions[quiz_no][x]['answer']:
                    for y in range(len(self.questions[quiz_no][x]['answer'])):
                        if y+1 != len(self.questions[quiz_no][x]['answer']):
                            answers_text.insert(tk.END, self.questions[quiz_no][x]['answer'][y] + "\n")
                        else:
                            answers_text.insert(tk.END, self.questions[quiz_no][x]['answer'][y])

        save_btn=tk.Button(scrollable_frame,text="Save", font=('Helvetica',12),width=14,bg="#8A1538",fg="#EEEEEE",activebackground='#975361',
                        command=lambda: save(quiz_no, num_questions))
        save_btn.pack(side=tk.RIGHT,pady=10)

        def save(quiz_no, num):
            list_question = []
            for x in range(num):
                question_frame = scrollable_frame.winfo_children()[x]
                question=question_frame.winfo_children()[1].winfo_children()[1].get("1.0", 'end-1c').strip()
                choices_temp=question_frame.winfo_children()[3].winfo_children()[1].get("1.0", 'end-1c').strip()
                choices = [choice.strip() for choice in choices_temp.split('\n') if choice.strip()]
                random.shuffle(choices)
                answers_temp=question_frame.winfo_children()[5].winfo_children()[1].get("1.0", 'end-1c').strip()
                answers = [answer.strip() for answer in answers_temp.split('\n') if answer.strip()]
                if question == "" or not choices or not answers:
                    tk.messagebox.showerror('Error','Please fill all fields.\nMissing Field on Question '+str(x+1))
                    break
                if len(choices) == 1:
                    msg_box = tk.messagebox.askokcancel('Warning', "Only one choice for Question " + str(x+1) + ".\nContinue?")
                    if not msg_box:
                        break
                if set(answers).issubset(set(choices)) != True:
                    tk.messagebox.showerror('Error', 'Correct Answer(s) for Question '+str(x+1)+' not in Choices.\nPlease check spelling and Caps')
                    break
                list_question.append(
                    {
                        'label':question,
                        'options':choices,
                        'answer':answers
                    }
                )
            self.num_questions[quiz_no] = num
            self.questions[quiz_no] = list_question

    def create_ocp_page(self):
        create_ocp_page=tk.Frame(self.main_frame)
        create_ocp_page.place(relx=.5, rely=.5,anchor= tk.CENTER)
        
        canvas = tk.Canvas(create_ocp_page)
        canvas.grid(row=1,column=1, pady=10)
        scrollbar1 = tk.Scrollbar(create_ocp_page, orient="vertical", command=canvas.yview)
        scrollbar1.grid(row=1, column=2, sticky="NS")
        scrollbar2 = tk.Scrollbar(create_ocp_page, orient="horizontal", command=canvas.xview)
        scrollbar2.grid(row=2, column=1, sticky="EW")
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar1.set, xscrollcommand=scrollbar2.set)
      
        row_cnt=1
        # Faculty Label
        faculty_label = tk.Label(scrollable_frame, text="Faculty: ", font=('Helvtica', 12))
        faculty_label.grid(row=row_cnt, column=1, pady=10, sticky=tk.W)
        faculty_data = tk.Label(scrollable_frame, text=self.faculty, font=('Helvtica', 12),fg="#8A1538")
        faculty_data.grid(row=row_cnt, column=2, pady=10,sticky=tk.W)
        row_cnt+=1
        # Course No Label
        course_no_label = tk.Label(scrollable_frame, text="Course No: ", font=('Helvtica', 12))
        course_no_label.grid(row=row_cnt, column=1, pady=10, sticky=tk.W)
        course_no_data = tk.Label(scrollable_frame, text=self.course_no, font=('Helvtica', 12),fg="#8A1538")
        course_no_data.grid(row=row_cnt, column=2, pady=10,sticky=tk.W)
        row_cnt+=1
        # Course Title Label
        course_title_label = tk.Label(scrollable_frame, text="Course Title: ", font=('Helvtica', 12))
        course_title_label.grid(row=row_cnt, column=1, pady=10, sticky=tk.W)
        course_title_data = tk.Label(scrollable_frame, text=self.course_title, font=('Helvtica', 12),fg="#8A1538")
        course_title_data.grid(row=row_cnt, column=2, pady=10,sticky=tk.W)
        row_cnt+=1
        # Course Intro Label
        course_intro_label = tk.Label(scrollable_frame, text="Course Intro: ", font=('Helvtica', 12))
        course_intro_label.grid(row=row_cnt, column=1, sticky=tk.W)
        if self.course_intro:
            for i in range(len(self.course_intro)):
                if i+1 == len(self.course_intro):
                    course_intro_data = tk.Label(scrollable_frame,text=self.course_intro[i], font=('Helvtica', 12),fg="#8A1538")
                    course_intro_data.grid(row=row_cnt, column=2, pady=(0,10),sticky=tk.W)
                    row_cnt+=1
                else:
                    course_intro_data = tk.Label(scrollable_frame,text=self.course_intro[i], font=('Helvtica', 12),fg="#8A1538")
                    course_intro_data.grid(row=row_cnt, column=2, sticky=tk.W)
                    row_cnt+=1
        else: 
            row_cnt+=1
        
        # Course Dir Label
        course_guide_dir_label = tk.Label(scrollable_frame, text="Course Guide: ", font=('Helvtica', 12))
        course_guide_dir_label.grid(row=row_cnt, column=1, pady=10, sticky=tk.W)
        course_guide_dir_data = tk.Label(scrollable_frame, text=self.course_guide_dir, font=('Helvtica', 12),fg="#8A1538")
        course_guide_dir_data.grid(row=row_cnt, column=2, pady=10,sticky=tk.W)
        row_cnt+=1

        #Resources
        resources_dir_label = tk.Label(scrollable_frame, text="Resources: ", font=('Helvtica', 12))
        resources_dir_label.grid(row=row_cnt, column=1, sticky=tk.W)
        if self.resources_dir:
            for i in range(len(self.resources_dir)):
                if i+1 == len(self.resources_dir):
                    resources_dir_data = tk.Label(scrollable_frame,text=self.resources_dir[i][0], font=('Helvtica', 12),fg="#8A1538")
                    resources_dir_data.grid(row=row_cnt, column=2, pady=(0,10),sticky=tk.W)
                    row_cnt+=1
                else:
                    resources_dir_data = tk.Label(scrollable_frame,text=self.resources_dir[i][0], font=('Helvtica', 12),fg="#8A1538")
                    resources_dir_data.grid(row=row_cnt, column=2, sticky=tk.W)
                    row_cnt+=1
        else:
            row_cnt+=1

        #Topic Dir
        if bool(self.topics_dir) != False:
            temp=list(self.topics_dir.keys())
            for i in range(len(temp)):
                if i+1 == len(temp):
                    topics_dir_label = tk.Label(scrollable_frame,text="Topic " + str(int(temp[i])) + " Dir", font=('Helvtica', 12))
                    topics_dir_label.grid(row=row_cnt, column=1, pady=(0,10),sticky=tk.W)

                    topics_dir_data = tk.Label(scrollable_frame,text=self.topics_dir[int(temp[i])], font=('Helvtica', 12),fg="#8A1538")
                    topics_dir_data.grid(row=row_cnt, column=2, pady=(0,10),sticky=tk.W)

                    row_cnt+=1
                else:
                    topics_dir_label = tk.Label(scrollable_frame,text="Topic " + str(int(temp[i])) + " Dir", font=('Helvtica', 12))
                    topics_dir_label.grid(row=row_cnt, column=1,sticky=tk.W)

                    topics_dir_data = tk.Label(scrollable_frame,text=self.topics_dir[int(temp[i])], font=('Helvtica', 12),fg="#8A1538")
                    topics_dir_data.grid(row=row_cnt, column=2, sticky=tk.W)

                    row_cnt+=1
        else:
            row_cnt+=1

        #Quiz
        for x in range(self.num_topics):
            button_text = "View Quiz " + str(x+1)
            button = tk.Button(scrollable_frame, text=button_text,font=('Helvetica',12),width=30,bg="#8A1538",fg="#EEEEEE",activebackground='#975361',
                            command=lambda value=x+1: check_quiz(value))
            button.grid(row=row_cnt+1,column=1,sticky=tk.W,pady=10,columnspan=2)
            row_cnt+=1
        row_cnt+=1
        button = tk.Button(scrollable_frame, text="View Final Quiz",font=('Helvetica',12),width=30,bg="#8A1538",fg="#EEEEEE",activebackground='#975361',
                            command=lambda value='final': check_quiz(value))
        button.grid(row=row_cnt,column=1,sticky=tk.W,pady=10,columnspan=2)
        row_cnt+=1

        save_btn=tk.Button(scrollable_frame,text="Save", font=('Helvetica',12),width=14,bg="#8A1538",fg="#EEEEEE",activebackground='#975361',
                        command=lambda: change_files())
        save_btn.grid(row=row_cnt,column=2,sticky=tk.W,pady=10)

        def check_quiz(value):
            if self.questions[value] == None:
                tk.messagebox.showerror("Error", "No quiz created")
            else:
                self.questionnaire_page(value, len(self.questions[value]))

        def change_files():
            print("Faculty: ", self.faculty, 
                "\nCourse No: ", self.course_no, 
                "\nCourse Title: ", self.course_title,
                "\nCourse Intro: ", self.course_intro,
                "\nCourse Guide Dir: ", self.course_guide_dir,
                "\nResources Dir: " , self.resources_dir,
                "\nNum Topics: ", self.num_topics,
                "\nTopics Dir: ", self.topics_dir,
                "\nNum Questions: ", self.num_questions,
                "\nQuestions",self.questions,
                "\n----------------------------------------------------------")
            
            no_topics = False
            for  key, value in self.topics_dir.items() :
                if self.topics_dir[key] == None:
                    print(key,value)
                    no_topics = True
                    break

            no_quiz = False

            if self.faculty == "" or self.course_no == "" or self.course_title=="":
                tk.messagebox.showerror('Error','Faculty, Course No, or Course Title is empty.')
            elif self.course_guide_dir == "":
                tk.messagebox.showerror('Error','No Course Guide Uploaded')
            elif self.num_topics <= 0:
                tk.messagebox.showerror('Error',"Number of Topics should be greater than zero")
            elif no_topics:
                tk.messagebox.showerror('Error', "Missing topics PDF")
            elif [self.num_questions[key] == None for key, value in self.num_questions.items()]:
                tk.messagebox.showerror('Error', 'Missing quizes')
            else:
                #introduction.html ---------------------------------------------------------------------------------------------------------------------
                if self.course_guide_dir:
                        target = os.path.join(os.path.dirname(__file__),'Interactive Offline Course/Offline Course/modules')
                        dir_parts = list(os.path.split(self.course_guide_dir))
                        target_dir = os.path.join(target, 'CourseGuide.pdf')
                        shutil.copy2(self.course_guide_dir, target_dir)
                
                soup_new = createSoup(os.path.join(os.path.dirname(__file__), 'Interactive Offline Course/Offline Course/introduction.html'))
                h2 = soup_new.h2
                h2.string = self.course_no + ' - ' + self.course_title
                if self.course_intro:
                    for p in soup_new.find_all('p', class_=False):
                        p.decompose()
                    p_tag = soup_new.new_tag('p')
                    p_tag.string = self.course_intro[0]
                    soup_new.hr.insert_after(p_tag)
                    for course_intro_word in self.course_intro[1:]:
                        next_p = soup_new.find_all('p', class_=False)[-1]
                        p_tag = soup_new.new_tag('p')
                        p_tag.string = course_intro_word
                        next_p.insert_after(p_tag)
        
                write_to_html(os.path.join(os.path.dirname(__file__),"Interactive Offline Course/Offline Course/introduction.html"), 
                        soup_new.prettify(formatter="html"))
                
                #course.html ---------------------------------------------------------------------------------------------------------------------
                soup_new = createSoup(os.path.join(os.path.dirname(__file__),'Interactive Offline Course/Offline Course/template/HTML/course_template.html'))
                to_append = []
                for x in range(int(self.num_topics)):
                    li_tag = soup_new.new_tag('li')
                    a_tag = soup_new.new_tag('a', href="#")
                    a_tag['data-value']=x+1
                    a_tag.string = "Topic " + str(x+1)
                    li_tag.append(a_tag)
                    to_append.append(li_tag)
                li_tag = soup_new.new_tag("li")
                a_tag = soup_new.new_tag("a", href="#")
                a_tag['data-value']=self.num_topics+1
                a_tag.string = "Final Exam"
                li_tag.append(a_tag)
                to_append.append(li_tag)
                for x in to_append:
                    ul_tag = soup_new.find("ul")
                    ul_tag.append(x)

                write_to_html(os.path.join(os.path.dirname(__file__),"Interactive Offline Course/Offline Course/course.html"), 
                        soup_new.prettify(formatter="html"))
                
                #profile.html ---------------------------------------------------------------------------------------------------------------------
                soup_new = createSoup(os.path.join(
                            os.path.dirname(__file__),'Interactive Offline Course/Offline Course/template/HTML/profile_template.html'))
                        
                first_link = soup_new.find('p', class_='faculty')
                first_link.string=self.faculty
                
                tag_replace(soup_new, "#Course#", self.course_no + ' - ' + self.course_title)
            
                write_to_html(os.path.join(os.path.dirname(__file__),"Interactive Offline Course/Offline Course/profile.html"), 
                    soup_new.prettify(formatter="html"))
                
                #register.html ---------------------------------------------------------------------------------------------------------------------
                soup_new = createSoup(os.path.join(
                            os.path.dirname(__file__),'Interactive Offline Course/Offline Course/template/HTML/register_template.html'))
                        
                tag_replace(soup_new,"#Course Name#", self.course_no)
                tag_replace(soup_new,"#Course Title#", self.course_title)
                
                write_to_html(os.path.join(os.path.dirname(__file__),"Interactive Offline Course/Offline Course/register.html"), 
                    soup_new.prettify(formatter="html"))
                
                #resources.html ---------------------------------------------------------------------------------------------------------------------
                if self.resources_dir:
                    temp = []
                    for src in self.resources_dir:
                        resourceName = src[0].split('/')[-1]
                        dir = os.path.join(os.path.dirname(__file__),'Interactive Offline Course/Offline Course/resources/'+resourceName)
                        if src[1] == 0:
                            shutil.copytree(src[0], dir)
                            hasPDF = False
                            for root, dirs, files in os.walk(dir):
                                for file in files:
                                    if file.endswith(".pdf"):
                                        hasPDF = True
                            li_tag = soup_new.new_tag("li")
                            a_tag = ""
                            if hasPDF == True:
                                a_tag = soup_new.new_tag("a", href="resources/"+resourceName, id="manual")
                            else:
                                a_tag = soup_new.new_tag("a", href="resources/"+resourceName)
                            a_tag.string = resourceName
                            li_tag.append(a_tag)
                            temp.append(li_tag)
                        else:
                            shutil.copy(src[0], dir)
                            li_tag = soup_new.new_tag("li")
                            a_tag = soup_new.new_tag("a", href="resources/"+resourceName)
                            a_tag.string = resourceName
                            li_tag.append(a_tag)
                            temp.append(li_tag)

                    soup_new = createSoup(os.path.join(
                            os.path.dirname(__file__),'Interactive Offline Course/Offline Course/template/HTML/resources_template.html'))
                    ol_tag = soup_new.find("ol")
                    for resource in temp:
                        ol_tag.append(resource)

                    write_to_html(os.path.join(os.path.dirname(__file__),"Interactive Offline Course/Offline Course/resources.html"), 
                        soup_new.prettify(formatter="html"))
                
                #JS FILES ---------------------------------------------------------------------------------------------------------------------
                copy_file(os.path.join(os.path.dirname(__file__),"Interactive Offline Course/Offline Course/template/JS/course.js"), 
                            os.path.join(os.path.dirname(__file__),"Interactive Offline Course/Offline Course/js/course.js"),
                            'case "#X#":', 'case ' +str(self.num_topics+1)+':')
                
                copy_file(os.path.join(os.path.dirname(__file__),"Interactive Offline Course/Offline Course/template/JS/register.js"), 
                            os.path.join(os.path.dirname(__file__),"Interactive Offline Course/Offline Course/js/register.js"),
                            'for (var i = 1; i <= "#X#" ; i++) {', 'for (var i = 1; i <= '+str(self.num_topics)+' ; i++) {')
                
                #CSS FILES ---------------------------------------------------------------------------------------------------------------------
                copy_file(os.path.join(os.path.dirname(__file__),"Interactive Offline Course/Offline Course/template/CSS/course.css"), 
                            os.path.join(os.path.dirname(__file__),"Interactive Offline Course/Offline Course/css/course.css"),
                            '#module_content li:nth-of-type("#X#"){', '#module_content li:nth-of-type('+str(self.num_topics+2)+'){')
                
                #quiz_htmls ---------------------------------------------------------------------------------------------------------------------
                for key,value in self.questions.items():
                    if value != 'final':
                        soup_new = createSoup(os.path.join(
                            os.path.dirname(__file__),'Interactive Offline Course/Offline Course/template/HTML/quiz_template.html'))
                        new_title = soup_new.find('title')
                        new_title.string = "Topic "+str(key)+" Quiz"
                        new_h2 = soup_new.find("h2")
                        new_h2.string = "Topic "+str(key)+" Quiz"
                        print(value)
                        write_script(soup_new, value)
                        write_to_html(os.path.join(os.path.dirname(__file__),"Interactive Offline Course/Offline Course/quiz/quiz"+str(key)+ ".html"), 
                            soup_new.prettify(formatter="html"))
                    else:
                        soup_new = createSoup(os.path.join(
                            os.path.dirname(__file__),'Interactive Offline Course/Offline Course/template/HTML/final-exam_template.html'))
                        write_script(soup_new, value)
                        write_to_html(os.path.join(os.path.dirname(__file__),"Interactive Offline Course/Offline Course/quiz/final-exam.html"), 
                            soup_new.prettify(formatter="html"))
                
        def write_script(soup_new, value):
                new_script = soup_new.find_all('script')[-1].getText()
                new_script = new_script.replace('ITEM_COUNT = "#X#"', 'ITEM_COUNT = ' + str(len(value)))
                questions_json = json.dumps(value)
                encoded_questions = base64.b64encode(questions_json.encode()).decode()
                new_script = new_script.replace('var questions="#X#"','var encryptedQuestions="'
                                                +encoded_questions+'"\nvar questions = JSON.parse(atob(encryptedQuestions));')
                script_tag = soup_new.find_all("script")[-1]
                script_tag.string = new_script

        def copy_file(template, dir, to_replace, replace):
            shutil.copy2(template, dir)
            with open(dir,'r') as f:
                lines = f.read()
            lines = lines.replace(to_replace, replace)
            with open(dir,'w') as f:
                f.write(lines)

        def tag_replace(soup_new,to_replace,replace):
            for tag in soup_new.find_all(string=re.compile(".*"+to_replace+".*")):
                if isinstance(tag, str):
                    tag.replace_with(tag.replace(to_replace, replace))

        def createSoup(dir):
            html_report_part= open(dir,'r')
            soup = BeautifulSoup(html_report_part, 'html.parser')
            return copy.deepcopy(soup)

        def write_to_html(html_file, html_output):
            with open(html_file, "w", encoding="utf-8") as file:
                file.write(html_output)

if __name__ == "__main__":
    root = tk.Tk()
    app = CourseManagementApp(root)
    root.mainloop()