from bs4 import BeautifulSoup
from shutil import copy2
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter.filedialog import askdirectory
from PIL import Image, ImageDraw, ImageFont
import copy
import os
import re
import shutil
import tkinter as tk
import json
import base64
import random
import tkinter.font as tkfont
import sys


LARGEFONT = ("Verdana", 20)
faculty = ""
course_name = ""
course_title = ""
course_intro = ""
resources = []
topics = 0
quiz_num_items = {}
val = 0
quiz_questions = {}

extra_files_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))

class tkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("700x450")
        container = tk.Frame(self)
        container.pack(side="right", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        
        for F in (MainMenuPage,
                  CourseInfoPage, 
                  CourseIntroPage, 
                  ResourcePage, 
                  TopicsPage, 
                  UploadTopicsPage, 
                  QuizMakerPage, 
                  NumQuestionsPage, 
                  QuestionsPage
                  ):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(MainMenuPage)
    
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.update()
        frame.tkraise()

class MainMenuPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.controller = controller
        self.configure(bg="#eeeeee")
        button_font = tkfont.Font(size=20)

        button1 = tk.Button(self, text="Create New",bg="#8A1538", fg="#eeeeee",
                            command=lambda: [controller.show_frame(CourseInfoPage),
                                             controller.frames[CourseInfoPage].refresh_sidebar(controller)])
        button1.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
        button2 = tk.Button(self, text="Edit Template",
                            bg="#8A1538",fg="#eeeeee")
        button2.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
        
        button1['font'] = button_font
        button2['font'] = button_font

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(7, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

class Sidebar(tk.Frame):
    def __init__(self, parent,controller):
        tk.Frame.__init__(self, parent, bg="#8A1538")  # Add background color
        # self.configure(width=200)
        button_frame = tk.Frame(self, width=20,bg="#8A1538")
        button_frame.grid(row=1,column=1)
        self.button1 = tk.Button(button_frame, text="Course Info", height=1, bg="#8A1538", fg="#eeeeee",
                             command=lambda: [controller.show_frame(CourseInfoPage),
                                              controller.frames[CourseInfoPage].refresh_sidebar(controller)])
        self.button1.grid(row=1, column=1, pady=10, sticky="nsew")
        
        self.button2 = tk.Button(button_frame, text="Course Intro", height=1, bg="#8A1538", fg="#eeeeee",
                             command=lambda: [controller.show_frame(CourseIntroPage), 
                                              controller.frames[CourseIntroPage].refresh_sidebar(controller)])
        self.button2.grid(row=2, column=1, pady=10, sticky="nsew")
        
        self.button3 = tk.Button(button_frame, text="Resources", height=1, bg="#8A1538", fg="#eeeeee",
                             command=lambda: [controller.show_frame(ResourcePage), 
                                              controller.frames[ResourcePage].refresh_sidebar(controller)])
        self.button3.grid(row=3, column=1, pady=10, sticky="nsew")
        
        self.button4 = tk.Button(button_frame, text="Topics", height=1, bg="#8A1538", fg="#eeeeee",
                             command=lambda: [controller.show_frame(TopicsPage), 
                                              controller.frames[TopicsPage].refresh_sidebar(controller)])
        self.button4.grid(row=4, column=1,pady=10, sticky="nsew")
        
        self.button5 = tk.Button(button_frame, text="Upload Topics", height=1, bg="#8A1538", fg="#eeeeee",
                             command=lambda: [self.refresh_upload_topics(controller), 
                                              controller.frames[UploadTopicsPage].refresh_sidebar(controller)])
        self.button5.grid(row=5, column=1,pady=10, sticky="nsew")
        
        self.button6 = tk.Button(button_frame, text="Create Quiz", height=1, bg="#8A1538", fg="#eeeeee",
                             command=lambda: [self.refresh_quiz_maker(controller), 
                                              controller.frames[QuizMakerPage].refresh_sidebar(controller)])
        self.button6.grid(row=6, column=1, pady=10, sticky="nsew")
        
        self.button7 = tk.Button(button_frame, text="Create OCP", height=1, bg="#00573F", fg="#eeeeee",
                             command=lambda: self.create_ocp())
        self.button7.grid(row=7, column=1, pady=10, sticky="nsew")
        
        self.button8 = tk.Button(button_frame, text="Back", height=1, bg="#8A1538", fg="#eeeeee",
                             command=lambda: controller.show_frame(MainMenuPage))
        self.button8.grid(row=8, column=1, pady=10, sticky="nsew")
        
        self.button2["state"]=DISABLED
        self.button3["state"]=DISABLED
        self.button4["state"]=DISABLED
        self.button5["state"]=DISABLED
        self.button6["state"]=DISABLED
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(9, weight=1)
        self.grid_columnconfigure(0,weight=1)
        self.grid_columnconfigure(2,weight=1)

    def refresh(self,controller):
        if faculty != "" and course_name != "" and course_title != "":
            self.button2.configure(state=tk.NORMAL)
            self.button3.configure(state=tk.NORMAL)
            self.button4.configure(state=tk.NORMAL)
        else:
            self.button2.configure(state=tk.DISABLED)
            self.button3.configure(state=tk.DISABLED)
            self.button4.configure(state=tk.DISABLED)
        
        if int(topics) != 0:
            self.button5.configure(state=tk.NORMAL)
            self.button6.configure(state=tk.NORMAL)
        else:
            self.button5.configure(state=tk.DISABLED)
            self.button6.configure(state=tk.DISABLED)

    def refresh_upload_topics(self,controller):
        controller.frames[UploadTopicsPage].refresh(controller)
        controller.show_frame(UploadTopicsPage)

    def refresh_quiz_maker(self,controller):
        controller.frames[QuizMakerPage].refresh(controller)
        controller.show_frame(QuizMakerPage)

    def create_ocp(self):
        global course_title
        path = '{}'.format(askdirectory(title='My Title'))
        # source_dir_prompt = '{}'.format(askdirectory(title='My Title'))
        # destination_dir_prompt = '{}'.format(askdirectory(title='My Title'))
        try:
            #if path already exists, remove it before copying with copytree()
            if os.path.exists(str(path+'/'+course_name)):
                shutil.rmtree(str(path+'/'+course_name))
                shutil.copytree(os.path.join(os.path.dirname(__file__), 'Interactive Offline Course/CMSC 206'), str(path+'/'+course_name))
        except OSError as e:
                print('Directory not copied. Error: %s' % e)
                os.rename(path,course_name)

class CourseInfoPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.sidebar = Sidebar(self, controller)
        self.sidebar.pack(side="left", fill="y", ipadx=20)
        # # Add main content to a separate frame
        self.content_frame = tk.Frame(self)
        self.content_frame.pack(side="left", fill="both", expand=True)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)
    
        self.clicked = tk.StringVar()
        
        faculty_label = tk.Label(self.content_frame, text="Faculty:")
        faculty_label.grid(row=1, column=1, padx=10, pady=5, sticky="e")
        
        faculty_option = ttk.Combobox(self.content_frame , state='readonly', width=27, textvariable=self.clicked)
        faculty_option['values'] = (
            "Faculty of Education",
            "Faculty of Information and Communication Studies",
            "Faculty of Management and Development Studies",
        )
        faculty_option.grid(row=1, column=2, padx=10, pady=5, sticky="w")
        faculty_option.current()
        
        course_name_label = ttk.Label(self.content_frame, text="Course Name:")
        course_name_label.grid(row=2, column=1, padx=10, pady=5, sticky="e")
        
        self.course_name_entry = ttk.Entry(self.content_frame,width=30, validate="key",
                                           validatecommand=(self.content_frame.register(self.validate_entry), "%S"))
        self.course_name_entry.grid(row=2, column=2, padx=10, pady=5, sticky="w")
        
        course_title_label = ttk.Label(self.content_frame, text="Course Title:")
        course_title_label.grid(row=3, column=1, padx=10, pady=5, sticky="e")
        
        self.course_title_entry = ttk.Entry(self.content_frame,width=30)
        self.course_title_entry.grid(row=3, column=2, padx=10, pady=5, sticky="w")
        
        button = ttk.Button(self.content_frame, text="Save",
                            command=lambda: self.save_course_info(controller))
        button.grid(row=4, column=2, padx=10, pady=10, sticky="e")

        self.content_frame.columnconfigure(0, weight=1)  # column on left
        self.content_frame.columnconfigure(3, weight=1)  # column on right
        self.content_frame.rowconfigure(0, weight=1)     # row above
        self.content_frame.rowconfigure(5, weight=1)     # row below

    def validate_entry(self, text):
        allowed_characters = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ")
        return all(char in allowed_characters for char in text)
    
    def tag_replace(self, soup_new,to_replace,replace):
        for tag in soup_new.find_all(string=re.compile(".*"+to_replace+".*")):
            if isinstance(tag, str):
                tag.replace_with(tag.replace(to_replace, replace))

    def save_course_info(self, controller):
        global faculty, course_name, course_title
        
        faculty = self.clicked.get()
        course_name = self.course_name_entry.get()
        course_title = self.course_title_entry.get()
        if faculty == "" or course_name == "" or course_title == "":
            msg_box=tk.messagebox.showerror('Error', 'Error: Missing fields')
        else:
            soup_new = createNewSoup(os.path.join(os.path.dirname(__file__), 'Interactive Offline Course/CMSC 206/introduction.html'))
            
            first_link = soup_new.h2
            first_link.string = course_name + ' - ' + course_title
            
            soup_new.h2.string
            
            write(os.path.join(os.path.dirname(__file__),"Interactive Offline Course/CMSC 206/introduction.html"), 
                soup_new.prettify(formatter="html"))
            
            soup_new = createNewSoup(os.path.join(
                os.path.dirname(__file__),'Interactive Offline Course/CMSC 206/template/register_template.html'))
            
            self.tag_replace(soup_new,"#Course Name#", course_name)
            self.tag_replace(soup_new,"#Course Title#", course_title)
            
            write(os.path.join(os.path.dirname(__file__),"Interactive Offline Course/CMSC 206/register.html"), 
                soup_new.prettify(formatter="html"))
            
            soup_new = createNewSoup(os.path.join(
                os.path.dirname(__file__),'Interactive Offline Course/CMSC 206/template/profile_template.html'))
            
            first_link = soup_new.find("p", class_="faculty")
            first_link.string=faculty
            
            self.tag_replace(soup_new, "#Course#", course_name + ' - ' + course_title)
            
            write(os.path.join(os.path.dirname(__file__),"Interactive Offline Course/CMSC 206/profile.html"), 
                soup_new.prettify(formatter="html"))
            
            file = ""
            match (faculty):
                case "Faculty of Education":
                    file = os.path.join(os.path.dirname(__file__),"Interactive Offline Course/CMSC 206/template/Logos/FoE.png")
                case "Faculty of Information and Communication Studies":
                    file = os.path.join(os.path.dirname(__file__),"Interactive Offline Course/CMSC 206/template/Logos/FICS.png")
                case "Faculty of Management and Development Studies":
                    file = os.path.join(os.path.dirname(__file__),"Interactive Offline Course/CMSC 206/template/Logos/FMDS.png")
            
            img = Image.open(file)
            W, H = img.size
            font_name = ImageFont.truetype(os.path.join(
                os.path.dirname(__file__),'Interactive Offline Course/CMSC 206/template/lovtony.ttf'), 350)
            font_title = ImageFont.truetype(os.path.join(
                os.path.dirname(__file__),'Interactive Offline Course/CMSC 206/template/Sansus Webissimo-Regular.otf'), 100)
            draw = ImageDraw.Draw(img)
            _, _, w_name, h_name = draw.textbbox((0, 0), course_name, font=font_name)
            draw.text(((720+W-w_name)/2, ((H-h_name)/2)-100), course_name, font=font_name, fill='#8a1538')
            _, _, w_title, h_title = draw.textbbox((0, 0), course_title, font=font_title)
            draw.text(((720+W-w_title)/2, ((350+H-h_title)/2)), course_title, font=font_title, fill='#8a1538')
            img.save(os.path.join(os.path.dirname(__file__),'Interactive Offline Course/CMSC 206/img/Logo.png'))

        controller.frames[CourseInfoPage].refresh_sidebar(controller)

    def refresh_sidebar(self,controller):
        self.sidebar.refresh(controller)
        
class CourseIntroPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.sidebar = Sidebar(self, controller)
        self.sidebar.pack(side="left", fill="y", ipadx=20)
        # # Add main content to a separate frame
        self.content_frame = tk.Frame(self)
        self.content_frame.pack(side="left", fill="both", expand=True)
        
        text_label = tk.Label(self.content_frame, text="Course Introduction")
        text_label.grid(row=1, column=1, pady=5, sticky="w")

        text_frame = tk.Frame(self.content_frame)
        text_frame.grid(row=2, column=1, pady=1,columnspan=2,sticky="nsew")
        
        self.course_intro_text = tk.Text(text_frame, width=50, height=10, wrap="none")
        self.course_intro_text.grid(row=0, column=0, sticky="nsew")
        
        scrollbar1 = ttk.Scrollbar(text_frame, command=self.course_intro_text.yview)
        scrollbar1.grid(row=0, column=1, sticky="ns")
        scrollbar2 = ttk.Scrollbar(text_frame, command=self.course_intro_text.xview, orient='horizontal')
        scrollbar2.grid(row=1, column=0, columnspan=2, sticky="ew")
        
        self.course_intro_text.config(yscrollcommand=scrollbar1.set)
        self.course_intro_text.config(xscrollcommand=scrollbar2.set)

        button2 = ttk.Button(self.content_frame, text="Save",
                            command=lambda: self.save_course_intro(controller))
        button2.grid(row=3, column=2, padx=10, pady=10, sticky="e")

        button1 = ttk.Button(self.content_frame, text="Upload Course Guide",
                             command=self.select_file, width=50)
        button1.grid(row=4, column=1, columnspan=2, pady=10, sticky="nesw")

        self.content_frame.columnconfigure(0, weight=1)  # column on left
        self.content_frame.columnconfigure(3, weight=1)  # column on right
        self.content_frame.rowconfigure(0, weight=1)     # row above
        self.content_frame.rowconfigure(5, weight=1)     # row below

    def save_course_intro(self, controller):
        global course_intro
        
        course_intro = self.course_intro_text.get("1.0",'end-1c')
        words = course_intro.split('\n')
        if len(words) == 1 and words[0]=='':
            msg_box=tk.messagebox.askokcancel("No Course Info","Are you sure?")
            if msg_box != 'yes':
                pass
            else:
                self.save(words)
        else:
            self.save(words)

    def save(self,words):
        soup_new = createNewSoup(os.path.join(os.path.dirname(__file__),'Interactive Offline Course/CMSC 206/introduction.html'))
        for p in soup_new.find_all("p", class_=False):
            p.decompose()
        tag = soup_new.new_tag("p")
        tag.string = words[0]
        soup_new.hr.insert_after(tag)
        for word in words[1:]:
            last_p = soup_new.find_all("p",class_=False)[-1]
            tag = soup_new.new_tag("p")
            tag.string = word
            last_p.insert_after(tag)
        write(os.path.join(os.path.dirname(__file__),"Interactive Offline Course/CMSC 206/introduction.html"), 
              soup_new.prettify(formatter="html"))
        
        # controller.show_frame(StartPage)

    def select_file(self):
        source = filedialog.askopenfilename(initialdir="/", title="Select file",
                                            filetype=(("PDF", "*.pdf"), ("All Files", "*.*")))
        if source:
            target = os.path.join(os.path.dirname(__file__),'Interactive Offline Course/CMSC 206/modules')
            dir_parts = list(os.path.split(source))
            target_dir = os.path.join(target, 'CourseGuide.pdf')
            copy2(source, target_dir)

    def refresh_sidebar(self,controller):
        self.sidebar.refresh(controller)

class ResourcePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.sidebar = Sidebar(self, controller)
        self.sidebar.pack(side="left", fill="y", ipadx=20)
        # # Add main content to a separate frame
        self.content_frame = tk.Frame(self)
        self.content_frame.pack(side="left", fill="both", expand=True)
        
        button1 = ttk.Button(self.content_frame, text="Add Resources Folder",
                             command=self.select_folder, width=50)
        button1.grid(row=1, column=1, columnspan=2, pady=10, sticky="nesw")
        button2 = ttk.Button(self.content_frame, text="Add File",
                             command=self.select_file)    
        button2.grid(row=2, column=1, columnspan=2, pady=10, sticky="nesw")

        button3 = ttk.Button(self.content_frame, text="Save",
                            command=lambda: self.append_file(controller))
        button3.grid(row=3, column=2,padx=10,pady=10, sticky="e")

        self.content_frame.columnconfigure(0, weight=1)  # column on left
        self.content_frame.columnconfigure(3, weight=1)  # column on right
        self.content_frame.rowconfigure(0, weight=1)     # row above
        self.content_frame.rowconfigure(4, weight=1)     # row below
        
    def select_folder(self):
        soup_new = BeautifulSoup()          
        path = '{}'.format(askdirectory(title='My Title'))
        resourceName = path.split('/')[-1]      
        dir = os.path.join(os.path.dirname(__file__),'Interactive Offline Course/CMSC 206/resources/'+resourceName)
        shutil.copytree(path, dir)
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
        global resources
        resources.append(li_tag)

    def select_file(self):
        soup_new = BeautifulSoup()
        source = filedialog.askopenfilename(initialdir="/", title="Select file",
                                            filetypes=(("All Files", ""),))
        resourceName = source.split('/')[-1]      
        dir = os.path.join(os.path.dirname(__file__),'Interactive Offline Course/CMSC 206/resources/'+resourceName)
        shutil.copy(source, dir)
        li_tag = soup_new.new_tag("li")
        a_tag = soup_new.new_tag("a", href="resources/"+resourceName)
        a_tag.string = resourceName
        li_tag.append(a_tag)
        global resources
        resources.append(li_tag)

    def append_file(self,controller):
        soup_new = createNewSoup(os.path.join(
            os.path.dirname(__file__),'Interactive Offline Course/CMSC 206/template/resources_template.html'))
        global resources
        ol_tag = soup_new.find("ol")
        for resource in resources:
            ol_tag.append(resource)
        write(os.path.join(os.path.dirname(__file__),"Interactive Offline Course/CMSC 206/resources.html"), 
              soup_new.prettify(formatter="html"))
        
    def refresh_sidebar(self,controller):
        self.sidebar.refresh(controller)

class TopicsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.sidebar = Sidebar(self, controller)
        self.sidebar.pack(side="left", fill="y", ipadx=20)
        # # Add main content to a separate frame
        self.content_frame = tk.Frame(self)
        self.content_frame.pack(side="left", fill="both", expand=True)

        numTopics_label = ttk.Label(self.content_frame, text="Number of topics:")
        numTopics_label.grid(row=1, column=1, padx=10, pady=5, sticky="e")
        
        self.numTopics_entry = ttk.Entry(self.content_frame,width=30, validate="key", 
                                         validatecommand=(self.content_frame.register(self.validate_entry), "%S"))
        self.numTopics_entry.grid(row=1, column=2, padx=10, pady=5, sticky="w")
        
        button2 = ttk.Button(self.content_frame, text="Save",
                            command=lambda: self.save_numTopic(controller))
        button2.grid(row=2, column=2,padx=10, pady=10, sticky="e")

        self.content_frame.columnconfigure(0, weight=1)  # column on left
        self.content_frame.columnconfigure(3, weight=1)  # column on right
        self.content_frame.rowconfigure(0, weight=1)     # row above
        self.content_frame.rowconfigure(3, weight=1)     # row below

    def validate_entry(self, text):
        return text.isdecimal()

    def copy_file(self, template, dir, to_replace, replace):
        shutil.copy2(template, dir)
        with open(dir,'r') as f:
            lines = f.read()
        lines = lines.replace(to_replace, replace)
        with open(dir,'w') as f:
            f.write(lines)

    def save_numTopic(self, controller):
        global topics
        topics = int(self.numTopics_entry.get())
        soup_new = createNewSoup(os.path.join(
            os.path.dirname(__file__),'Interactive Offline Course/CMSC 206/template/course_template.html'))
        to_append = []
        for x in range(int(topics)):
            li_tag = soup_new.new_tag("li")
            a_tag = soup_new.new_tag("a", href="#")
            a_tag['data-value']=x+1
            a_tag.string = "Topic " + str(x+1) 
            li_tag.append(a_tag)
            to_append.append(li_tag)
        li_tag = soup_new.new_tag("li")
        a_tag = soup_new.new_tag("a", href="#")
        a_tag['data-value']=topics+1
        a_tag.string = "Final Exam"
        li_tag.append(a_tag)
        to_append.append(li_tag)
        for x in to_append:
            ul_tag = soup_new.find("ul")
            ul_tag.append(x)
        write(os.path.join(os.path.dirname(__file__),"Interactive Offline Course/CMSC 206/course.html"), 
              soup_new.prettify(formatter="html"))
        self.copy_file(os.path.join(os.path.dirname(__file__),"Interactive Offline Course/CMSC 206/template/course.js"), 
                       os.path.join(os.path.dirname(__file__),"Interactive Offline Course/CMSC 206/js/course.js"),
                       'case "#X#":', 'case ' +str(topics+1)+':')
        self.copy_file(os.path.join(os.path.dirname(__file__),"Interactive Offline Course/CMSC 206/template/register.js"), 
                       os.path.join(os.path.dirname(__file__),"Interactive Offline Course/CMSC 206/js/register.js"),
                       'for (var i = 1; i <= "#X#" ; i++) {', 'for (var i = 1; i <= '+str(topics)+' ; i++) {')
        self.copy_file(os.path.join(os.path.dirname(__file__),"Interactive Offline Course/CMSC 206/template/course.css"), 
                       os.path.join(os.path.dirname(__file__),"Interactive Offline Course/CMSC 206/css/course.css"),
                       '#module_content li:nth-of-type("#X#"){', '#module_content li:nth-of-type('+str(topics+2)+'){')
        global quiz_num_items, quiz_questions
        temp = []
        for x in range(topics):
            temp.append(x+1)
        quiz_num_items = dict.fromkeys(temp)
        quiz_num_items["final"] = None
        quiz_questions = dict.fromkeys(temp)
        quiz_questions["final"] = None
        self.sidebar.refresh(controller)
    
    def refresh_sidebar(self,controller):
        self.sidebar.refresh(controller)

class UploadTopicsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

    def refresh(self, controller):
        global topics
        clearChildren(self)

        self.sidebar = Sidebar(self, controller)
        self.sidebar.pack(side="left", fill="y", ipadx=20)
        # # Add main content to a separate frame
        self.content_frame = tk.Frame(self)
        self.content_frame.pack(side="left", fill="both", expand=True)

        self.controller = controller

        self.canvas = tk.Canvas(self.content_frame, height=450, width=550,)
        self.scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=self.canvas.yview)
        self.frame_container = tk.Frame(self.canvas)

        self.frame_container.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((280, 0), window=self.frame_container, anchor="center")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left",fill="y",expand=True)
        self.scrollbar.pack(side="right", fill="y")  # Adjusted padx value
        
        for x in range(int(topics)):
            button_text = "Upload Topic " + str(x + 1) + " PDF"
            button = ttk.Button(self.frame_container, text=button_text, command=lambda value=x + 1: self.button_click(value), width=50)
            # Place the button with the calculated padding
            button.grid(row=x + 1, column=1, columnspan=2,pady=10)

        self.canvas.create_window((280, 0), window=self.frame_container, anchor="center")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left",fill="y",expand=True)
        self.scrollbar.pack(side="right", fill="y")  # Adjusted padx value

    def button_click(self, value):
        source = filedialog.askopenfilename(initialdir="/", title="Select file",
                                            filetypes=(("PDF", "*.pdf"), ("All Files", "*.*")))
        if source:
            target = os.path.join(os.path.dirname(__file__),'Interactive Offline Course/CMSC 206/modules')
            dir_parts = list(os.path.split(source))
            target_dir = os.path.join(target, 'Module'+str(value)+'.pdf')
            copy2(source, target_dir)

    def refresh_sidebar(self,controller):
        self.sidebar.refresh(controller)

class QuizMakerPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # self.label = ttk.Label(self.content_frame, text="Upload Topics", font=LARGEFONT)
        # self.label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    def refresh(self, controller):
        global topics
        clearChildren(self)
        self.controller = controller

        self.sidebar = Sidebar(self, controller)
        self.sidebar.pack(side="left", fill="y", ipadx=20)
        # # Add main content to a separate frame
        self.content_frame = tk.Frame(self)
        self.content_frame.pack(side="left", fill="both", expand=True)

        self.canvas = tk.Canvas(self.content_frame, height=450, width=550,)
        self.scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=self.canvas.yview)
        self.frame_container = tk.Frame(self.canvas)

        self.frame_container.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((280, 0), window=self.frame_container, anchor="center")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left",fill="y",expand=True)
        self.scrollbar.pack(side="right", fill="y")  # Adjusted padx value

        for x in range(int(topics)):
            button_text = "Create Quiz " + str(x + 1)
            button = ttk.Button(self.frame_container, text=button_text, 
                                command=lambda value=x + 1: self.button_click(controller, value),width=50)
            button.grid(row=x + 1, column=1,  columnspan=2, pady=10)
        button_final = ttk.Button(self.frame_container, text="Create Final Quiz", 
                                  command=lambda value="final": self.button_click(controller, value),width=50) 
        button_final.grid(row=int(topics)+2, column=1,  columnspan=2, pady=10)
    
    def button_click(self, controller, value):
        global val
        val = value
        self.refresh_quiz_maker(controller)

    def refresh_quiz_maker(self,controller):
        # controller.frames[NumQuestionsPage].refresh(controller)
        controller.frames[NumQuestionsPage].refresh_sidebar(controller)
        controller.show_frame(NumQuestionsPage)

    def refresh_sidebar(self,controller):
        self.sidebar.refresh(controller)

class NumQuestionsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.sidebar = Sidebar(self, controller)
        self.sidebar.pack(side="left", fill="y", ipadx=20)
        # # Add main content to a separate frame
        self.content_frame = tk.Frame(self)
        self.content_frame.pack(side="left", fill="both", expand=True)

        global val, quiz_num_items
        # print(val, quiz_num_items)

        num_questions_label = ttk.Label(self.content_frame, text="Number of Questions:")
        num_questions_label.grid(row=1, column=1, padx=10, pady=5, sticky="e")
        
        self.num_questions_entry = ttk.Entry(self.content_frame,width=30, validate="key", validatecommand=(self.content_frame.register(self.validate_entry), "%S"))
        self.num_questions_entry.grid(row=1, column=2, padx=10, pady=5, sticky="w")
        
        button2 = ttk.Button(self.content_frame, text="Next",
                            command=lambda: self.save_num_questions(controller))
        button2.grid(row=2, column=2,padx=10, pady=10, sticky="e")

        self.content_frame.columnconfigure(0, weight=1)  # column on left
        self.content_frame.columnconfigure(3, weight=1)  # column on right
        self.content_frame.rowconfigure(0, weight=1)     # row above
        self.content_frame.rowconfigure(3, weight=1)     # row below

    def validate_entry(self, text):
        return text.isdecimal()
    
    def save_num_questions(self, controller):
        global quiz_num_items, val
        quiz_num_items[val] = int(self.num_questions_entry.get())
        print(quiz_num_items)

        controller.frames[QuestionsPage].refresh(controller)
        controller.frames[QuestionsPage].refresh_sidebar(controller)
        controller.show_frame(QuestionsPage)

    def refresh_sidebar(self,controller):
        self.sidebar.refresh(controller)

class QuestionsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.questions = []
        self.next_button = None

    def refresh(self, controller):
        global quiz_num_items, val
        clearChildren(self)
        
        self.sidebar = Sidebar(self, controller)
        self.sidebar.pack(side="left", fill="y", ipadx=20)
        # # Add main content to a separate frame
        self.content_frame = tk.Frame(self)
        self.content_frame.pack(side="left", fill="both", expand=True)

        self.canvas = tk.Canvas(self.content_frame, height=450, width=550)
        self.scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=self.canvas.yview)
        self.frame_container = ttk.Frame(self.canvas)
        self.frame_container.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        self.canvas.create_window((0, 0), window=self.frame_container, anchor="center")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.grid(row=1, column=0, columnspan=2, sticky="nsew")
        self.scrollbar.grid(row=1, column=2, sticky="ns")  # Adjusted padx value

        value = quiz_num_items[val]
        # print(value)
        for x in range(value):
            question_frame = ttk.Frame(self.frame_container, padding=10)
            question_frame.grid(row=x, column=0, columnspan=3, sticky="w")
            
            question_label = ttk.Label(question_frame, text=f"Question {x+1}")
            question_label.grid(row=0, column=0)
            
            entry1 = ttk.Entry(question_frame)
            entry1.grid(row=0, column=1)
            
            answers_label = ttk.Label(question_frame, text=f"Answers")
            answers_label.grid(row=1, column=0)
            
            text_frame1 = ttk.Frame(question_frame)
            text_frame1.grid(row=2, column=0, columnspan=2, sticky="w")
            
            text1 = tk.Text(text_frame1, width=50, height=5)
            text1.pack(side="left", fill="both", expand=True)
            
            scrollbar1 = ttk.Scrollbar(text_frame1, orient="vertical", command=text1.yview)
            scrollbar1.pack(side="right", fill="y", padx=(0, 5))
            
            text1.configure(yscrollcommand=scrollbar1.set)
            correct_label = ttk.Label(question_frame, text="Correct Answer(s)")
            correct_label.grid(row=3, column=0)
            
            text_frame2 = ttk.Frame(question_frame)
            text_frame2.grid(row=4, column=0, columnspan=2, sticky="w")
            
            text2 = tk.Text(text_frame2, width=50, height=5)
            text2.pack(side="left", fill="both", expand=True)
            
            scrollbar2 = ttk.Scrollbar(text_frame2, orient="vertical", command=text2.yview)
            scrollbar2.pack(side="right", fill="y", padx=(0, 5))
            
            text2.configure(yscrollcommand=scrollbar2.set)
            
            save_button = ttk.Button(question_frame, text="Save",
                                command=lambda q=entry1, o=text1, a=text2: self.save_question(q, o, a))
            save_button.grid(row=5, column=1)
        if self.next_button is not None:
            self.next_button.destroy()  # Destroy the previous "Next" button
        
        self.next_button = ttk.Button(self.frame_container, text="Next",
                            command=lambda: self.print(controller))
        self.next_button.grid(row=value+1, column=0, columnspan=3, padx=10, pady=10, sticky="s")
        

        self.scrollbar.grid(row=1, column=2, sticky="ns")

    def save_question(self, question_entry, options_text, answer_entry):
        question = question_entry.get()
        options = options_text.get("1.0", "end-1c").split('\n')
        random.shuffle(options)
        answer = answer_entry.get("1.0", "end-1c").split('\n')
        if set(answer).issubset(set(options)) == True:
            self.questions.append({
                'label': question,
                'options': options,
                'answer': answer
            })
        else:
            print("No Answer")

    def write_script(self, soup_new):
        new_script = soup_new.find_all('script')[-1].getText()
        new_script = new_script.replace('ITEM_COUNT = "#X#"', 'ITEM_COUNT = ' + str(quiz_num_items[val]))
        questions_json = json.dumps(self.questions)
        encoded_questions = base64.b64encode(questions_json.encode()).decode()
        new_script = new_script.replace('var questions="#X#"','var encryptedQuestions="'
                                        +encoded_questions+'"\nvar questions = JSON.parse(atob(encryptedQuestions));')
        script_tag = soup_new.find_all("script")[-1]
        script_tag.string = new_script

    def print(self,controller):
        global val, quiz_num_items
        
        if val != "final":
            soup_new = createNewSoup(os.path.join(
                os.path.dirname(__file__),'Interactive Offline Course/CMSC 206/template/quiz_template.html'))
            new_title = soup_new.find('title')
            new_title.string = "Topic "+str(val)+" Quiz"
            new_h2 = soup_new.find("h2")
            new_h2.string = "Topic "+str(val)+" Quiz"
            self.write_script(soup_new)
            write(os.path.join(os.path.dirname(__file__),"Interactive Offline Course/CMSC 206/quiz/quiz"+str(val)+ ".html"), 
                  soup_new.prettify(formatter="html"))
        else:
            soup_new = createNewSoup(os.path.join(
                os.path.dirname(__file__),'Interactive Offline Course/CMSC 206/template/final-exam_template.html'))
            self.write_script(soup_new)
            write(os.path.join(os.path.dirname(__file__),"Interactive Offline Course/CMSC 206/quiz/final-exam.html"), 
                  soup_new.prettify(formatter="html"))
        
        controller.frames[QuizMakerPage].refresh(controller)
        controller.frames[QuizMakerPage].refresh_sidebar(controller)
        controller.show_frame(QuizMakerPage)
    
    def refresh_sidebar(self,controller):
        self.sidebar.refresh(controller)

def createNewSoup(dir):
    html_report_part1 = open(dir,'r')
    soup = BeautifulSoup(html_report_part1, 'html.parser')
    return copy.deepcopy(soup)

def write(html_file,html_output):
    with open(html_file, "w", encoding="utf-8") as file:
        file.write(html_output)

def clearChildren(self):
    for widget in self.winfo_children():
            widget.destroy()

app = tkinterApp()  
app.mainloop()