from bs4 import BeautifulSoup
from shutil import copy2
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter.filedialog import askdirectory
import copy
import os
import re
import shutil
import tkinter as tk
from PIL import Image, ImageDraw, ImageFont, ImageColor

LARGEFONT = ("Verdana", 35)

faculty = ""
course_name = ""
course_title = ""
course_intro = ""
resources = []
topics = 0
quiz_num_items = {}
val = 0
quiz_questions = {}

class tkinterApp(tk.Tk):
    #The main application window
    def __init__(self, *args, **kwargs):
        #Initialize the application window
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, CourseInfoPage, CourseIntroPage, ResourcePage, TopicsPage, UploadTopicsPage, QuizMakerPage, NumQuestionsPage, QuestionsPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        #Show the specified frame
        frame = self.frames[cont]
        frame.update()
        frame.tkraise()

class StartPage(tk.Frame):
    #The start page of the application
    def __init__(self, parent, controller):
        #Initialize the start page
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = ttk.Label(self, text="Startpage", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        button1 = ttk.Button(self, text="Course Info",
                             command=lambda: controller.show_frame(CourseInfoPage))
        button1.grid(row=1, column=1, padx=10, pady=10)

        button2 = ttk.Button(self, text="Course Intro",
                             command=lambda: controller.show_frame(CourseIntroPage))
        button2.grid(row=2, column=1, padx=10, pady=10)

        button3 = ttk.Button(self, text="Resources",
                             command=lambda: controller.show_frame(ResourcePage))
        button3.grid(row=3, column=1, padx=10, pady=10)

        button4 = ttk.Button(self, text="Topics",
                             command=lambda: controller.show_frame(TopicsPage))
        button4.grid(row=4, column=1, padx=10, pady=10)

        button5 = ttk.Button(self, text="Upload Topics",
                             command=lambda: self.refresh_upload_topics(controller))
        button5.grid(row=5, column=1, padx=10, pady=10)

        button6 = ttk.Button(self, text="Create Quiz",
                             command=lambda: self.refresh_quiz_maker(controller))
        button6.grid(row=6, column=1, padx=10, pady=10)

    def refresh_upload_topics(self,controller):
        global topics
        controller.frames[UploadTopicsPage].refresh(controller)
        controller.show_frame(UploadTopicsPage)

    def refresh_quiz_maker(self,controller):
        global topics
        controller.frames[QuizMakerPage].refresh(controller)
        controller.show_frame(QuizMakerPage)

class CourseInfoPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Course Information", font=LARGEFONT)
        label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.clicked = tk.StringVar()
        faculty_label = ttk.Label(self, text="Faculty:")
        faculty_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        faculty_option = ttk.Combobox( self , state='readonly', width=27, textvariable=self.clicked)
        faculty_option['values'] = (
            "Faculty of Education",
            "Faculty of Information and Communication Studies",
            "Faculty of Management and Development Studies",
        )
        faculty_option.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        faculty_option.current()

        course_name_label = ttk.Label(self, text="Course Name:")
        course_name_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.course_name_entry = ttk.Entry(self)
        self.course_name_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        course_title_label = ttk.Label(self, text="Course Title:")
        course_title_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.course_title_entry = ttk.Entry(self)
        self.course_title_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        button = ttk.Button(self, text="Next",
                            command=lambda: self.save_course_info(controller))
        button.grid(row=4, column=1, padx=10, pady=10)
        
    def save_course_info(self, controller):
        global faculty, course_name, course_title
        faculty = self.clicked.get()
        course_name = self.course_name_entry.get()
        course_title = self.course_title_entry.get()

        html_report_part1 = open('Interactive Offline Course/CMSC 206/introduction.html','r')
        soup = BeautifulSoup(html_report_part1, 'html.parser')
        soup_new = copy.deepcopy(soup)
        first_link = soup_new.h2
        first_link.string = course_name + ' - ' + course_title
        soup_new.h2.string
        with open("Interactive Offline Course/CMSC 206/introduction.html", "w") as file:
            file.write(str(soup_new))

        html_report_part2 = open('Interactive Offline Course/CMSC 206/template/register_template.html','r')
        soup = BeautifulSoup(html_report_part2, 'html.parser')
        soup_new = copy.deepcopy(soup)
        for tag in soup_new.find_all(string=re.compile(".*#Course Name#.*")):
            if isinstance(tag, str):
                tag.replace_with(tag.replace("#Course Name#", course_name))
        for tag in soup_new.find_all(string=re.compile(".*#Course Title#.*")):
            if isinstance(tag,str):
                tag.replace_with(tag.replace("#Course Title#", course_title))
        html_output = soup_new.prettify(formatter="html")
        with open("Interactive Offline Course/CMSC 206/register.html", "w", encoding="utf-8") as file:
            file.write(html_output)
        
        html_report_part3 = open('Interactive Offline Course/CMSC 206/template/profile_template.html','r')
        soup = BeautifulSoup(html_report_part3, 'html.parser')
        soup_new = copy.deepcopy(soup)
        first_link = soup_new.findAll("p", class_=faculty)
        first_link.string=faculty
        for tag in soup_new.find_all(string=re.compile(".*#Course#.*")):
            if isinstance(tag,str):
                tag.replace_with(tag.replace("#Course#", course_name + ' - ' + course_title))
        html_output = soup_new.prettify(formatter="html")
        with open("Interactive Offline Course/CMSC 206/profile.html", "w", encoding="utf-8") as file:
            file.write(html_output)
        
        file = ""
        match (faculty):
            case "Faculty of Education":
                file = "Interactive Offline Course/CMSC 206/template/Logos/FoE.png"
            case "Faculty of Information and Communication Studies":
                file = "Interactive Offline Course/CMSC 206/template/Logos/FICS.png"
            case "Faculty of Management and Development Studies":
                file = "Interactive Offline Course/CMSC 206/template/Logos/FMDS.png"
        img = Image.open(file)
        W, H = img.size
        font_name = ImageFont.truetype('Interactive Offline Course/CMSC 206/template/lovtony.ttf', 350)
        font_title = ImageFont.truetype('Interactive Offline Course/CMSC 206/template/Sansus Webissimo-Regular.otf', 100)
        
        draw = ImageDraw.Draw(img)
        _, _, w_name, h_name = draw.textbbox((0, 0), course_name, font=font_name)
        draw.text(((720+W-w_name)/2, ((H-h_name)/2)-100), course_name, font=font_name, fill='#8a1538')
        _, _, w_title, h_title = draw.textbbox((0, 0), course_title, font=font_title)
        draw.text(((720+W-w_title)/2, ((350+H-h_title)/2)), course_title, font=font_title, fill='#8a1538')

        img.save(r'Interactive Offline Course/CMSC 206/img/Logo.png')
        controller.show_frame(StartPage)

class CourseIntroPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Course Introduction", font=LARGEFONT)
        label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Configure row and column weights
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.course_intro_text = tk.Text(self, width=50, height=10)
        self.course_intro_text.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")

        # Add a vertical scroll bar
        scrollbar = ttk.Scrollbar(self, command=self.course_intro_text.yview)
        scrollbar.grid(row=1, column=2, sticky="ns")
        self.course_intro_text.config(yscrollcommand=scrollbar.set)

        button1 = ttk.Button(self, text="Select File",
                             command=self.select_file)
        button1.grid(row=2, column=1, padx=10, pady=10)

        button2 = ttk.Button(self, text="Next",
                            command=lambda: self.save_course_intro(controller))
        button2.grid(row=3, column=1, padx=10, pady=10)

    def save_course_intro(self, controller):
        global course_intro
        course_intro = self.course_intro_text.get("1.0",'end-1c')
        # breaks=course_intro.count('\n')  # Number of line breaks ( except last one ) 
        # char_numbers=len(course_intro)-breaks # total chars excluding line breaks
        words = course_intro.split('\n')
        html_report_part1 = open('Interactive Offline Course/CMSC 206/introduction.html','r')
        soup = BeautifulSoup(html_report_part1, 'html.parser')
        soup_new = copy.deepcopy(soup)
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
        with open("Interactive Offline Course/CMSC 206/introduction.html", "w") as file:
            file.write(str(soup_new))

        # Navigate to the next page
        controller.show_frame(StartPage)

    def select_file(self):
        source = filedialog.askopenfilename(initialdir="/", title="Select file",
                                            filetype=(("PDF", "*.pdf"), ("All Files", "*.*")))
        if source:
            target = 'Interactive Offline Course/CMSC 206/modules'
            dir_parts = list(os.path.split(source))
            target_dir = os.path.join(target, 'CourseGuide.pdf')
            copy2(source, target_dir)

class ResourcePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Topics", font=LARGEFONT)
        label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        button1 = ttk.Button(self, text="Add Resources Folder",
                             command=self.select_folder)
        button1.grid(row=1, column=1, padx=10, pady=10)

        button2 = ttk.Button(self, text="Add File",
                             command=self.select_file)
        button2.grid(row=2, column=1, padx=10, pady=10)

        button3 = ttk.Button(self, text="Next",
                            command=lambda: self.append_file(controller))
        button3.grid(row=3, column=1, padx=10, pady=10)

    def select_folder(self):
        soup_new = BeautifulSoup()          
        path = '{}'.format(askdirectory(title='My Title'))
        resourceName = path.split('/')[-1]      
        dir = r'Interactive Offline Course/CMSC 206/resources/'+resourceName
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
        dir = r'Interactive Offline Course/CMSC 206/resources/'+resourceName
        shutil.copy(source, dir)
        li_tag = soup_new.new_tag("li")
        a_tag = soup_new.new_tag("a", href="resources/"+resourceName)
        a_tag.string = resourceName
        li_tag.append(a_tag)
       
        global resources
        resources.append(li_tag)

    def append_file(self,controller):
        html_report_part1 = open('Interactive Offline Course/CMSC 206/template/resources_template.html','r')
        soup = BeautifulSoup(html_report_part1, 'html.parser')
        soup_new = copy.deepcopy(soup)

        global resources
        ol_tag = soup_new.find("ol")
        for resource in resources:
            ol_tag.append(resource)

        html_output = soup_new.prettify(formatter="html")
        with open("Interactive Offline Course/CMSC 206/resources.html", "w", encoding="utf-8") as file:
            file.write(html_output)

        # Navigate to the next page
        controller.show_frame(StartPage)

class TopicsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Topics", font=LARGEFONT)
        label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        numTopics_label = ttk.Label(self, text="Number of topics:")
        numTopics_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.numTopics_entry = ttk.Entry(self)
        self.numTopics_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        button2 = ttk.Button(self, text="Next",
                            command=lambda: self.save_numTopic(controller))
        button2.grid(row=3, column=1, padx=10, pady=10)

    def save_numTopic(self, controller):
        global topics
        topics = int(self.numTopics_entry.get())

        html_report_part1 = open('Interactive Offline Course/CMSC 206/template/course_template.html','r')
        soup = BeautifulSoup(html_report_part1, 'html.parser')
        soup_new = copy.deepcopy(soup)

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
        
        html_output = soup_new.prettify(formatter="html")
        with open("Interactive Offline Course/CMSC 206/course.html", "w", encoding="utf-8") as file:
            file.write(html_output)

        shutil.copy2("Interactive Offline Course/CMSC 206/template/course.js", "Interactive Offline Course/CMSC 206/js/course.js")
        with open('Interactive Offline Course/CMSC 206/js/course.js','r') as f:
            lines = f.read()
        lines = lines.replace('case "#X#":', 'case ' +str(topics+1)+':')
        with open('Interactive Offline Course/CMSC 206/js/course.js','w') as f:
            f.write(lines)
        
        shutil.copy2("Interactive Offline Course/CMSC 206/template/register.js", "Interactive Offline Course/CMSC 206/js/register.js")
        with open('Interactive Offline Course/CMSC 206/js/register.js','r') as f:
            lines = f.read()

        lines = lines.replace('for (var i = 1; i <= "#X#" ; i++) {', 'for (var i = 1; i <= '+str(topics)+' ; i++) {')
        with open("Interactive Offline Course/CMSC 206/js/register.js",'w') as f:
            f.write(lines)

        shutil.copy2("Interactive Offline Course/CMSC 206/template/course.css", "Interactive Offline Course/CMSC 206/css/course.css")
        with open('Interactive Offline Course/CMSC 206/css/course.css','r') as f:
            lines = f.read()

        lines = lines.replace('#module_content li:nth-of-type("#X#"){', '#module_content li:nth-of-type('+str(topics+2)+'){')
        with open('Interactive Offline Course/CMSC 206/css/course.css','w') as f:
            f.write(lines)

        global quiz_num_items, quiz_questions
        temp = []
        for x in range(topics):
            temp.append(x+1)
        quiz_num_items = dict.fromkeys(temp)
        quiz_questions = dict.fromkeys(temp)

        # Navigate to the next page
        controller.show_frame(StartPage)

class UploadTopicsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.label = ttk.Label(self, text="Upload Topics", font=LARGEFONT)
        self.label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    def refresh(self, controller):
        global topics
        self.clear_buttons()

        for x in range(int(topics)):
            button_text = "Upload Topic " + str(x + 1) + " PDF"
            button = tk.Button(self, text=button_text, command=lambda value=x + 1: self.button_click(value))
            button.grid(row=x + 1, column=0, padx=10, pady=5, sticky="w")

        button6 = ttk.Button(self, text="Next",
                             command=lambda: controller.show_frame(StartPage))
        button6.grid(row=int(topics)+1, column=1, padx=10, pady=10)

    def clear_buttons(self):
        for widget in self.winfo_children():
            widget.destroy()

    def button_click(self, value):
        source = filedialog.askopenfilename(initialdir="/", title="Select file",
                                            filetypes=(("PDF", "*.pdf"), ("All Files", "*.*")))
        if source:
            target = 'Interactive Offline Course/CMSC 206/modules'
            dir_parts = list(os.path.split(source))
            target_dir = os.path.join(target, 'Module'+str(value)+'.pdf')
            copy2(source, target_dir)

class QuizMakerPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.label = ttk.Label(self, text="Upload Topics", font=LARGEFONT)
        self.label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    def refresh(self, controller):
        global topics
        self.clear_buttons()

        for x in range(int(topics)):
            button_text = "Create Quiz " + str(x + 1)
            button = tk.Button(self, text=button_text, command=lambda value=x + 1: self.button_click(controller, value))
            button.grid(row=x + 1, column=0, padx=10, pady=5, sticky="w")

        button6 = ttk.Button(self, text="Next",
                             command=lambda: controller.show_frame(StartPage))
        button6.grid(row=int(topics)+1, column=1, padx=10, pady=10)

    def clear_buttons(self):
        for widget in self.winfo_children():
            widget.destroy()

    def button_click(self, controller, value):
        global val
        val = value
        self.refresh_quiz_maker(controller)

    def refresh_quiz_maker(self,controller):
        global topics
        controller.frames[NumQuestionsPage].refresh(controller)
        controller.show_frame(NumQuestionsPage)

class NumQuestionsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.label = ttk.Label(self, text="Number of Questions", font=LARGEFONT)
        self.label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    def refresh(self, controller):
        global val, quiz_num_items
        print(val, quiz_num_items)

        num_questions_label = ttk.Label(self, text="Number of Questions:")
        num_questions_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.num_questions_entry = ttk.Entry(self)
        self.num_questions_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        button = ttk.Button(self, text="Next",
                            command=lambda: self.save_num_questions(controller))
        button.grid(row=4, column=1, padx=10, pady=10)

    def save_num_questions(self, controller):
        global quiz_num_items, val
        quiz_num_items[val] = int(self.num_questions_entry.get())
        # print(quiz_num_items)
        controller.frames[QuestionsPage].refresh(controller)
        controller.show_frame(QuestionsPage)

class QuestionsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.label = ttk.Label(self, text="Questions", font=LARGEFONT)
        self.label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.canvas = tk.Canvas(self,height=300)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)

        self.frame_container = ttk.Frame(self.canvas)
        self.frame_container.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.frame_container, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.grid(row=1, column=0, columnspan=2, sticky="nsew")
        self.scrollbar.grid(row=1, column=2, sticky="ns")  # Adjusted padx value

        self.questions = [] 

    def refresh(self, controller):
        global quiz_num_items, val
        self.clear_all()
        value = quiz_num_items[val]

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
            scrollbar1.pack(side="right", fill="y", padx=(0, 5))  # Adjusted padx value
            text1.configure(yscrollcommand=scrollbar1.set)

            correct_label = ttk.Label(question_frame, text="Correct Answer(s)")
            correct_label.grid(row=3, column=0)
            text_frame2 = ttk.Frame(question_frame)
            text_frame2.grid(row=4, column=0, columnspan=2, sticky="w")
            text2 = tk.Text(text_frame2, width=50, height=5)
            text2.pack(side="left", fill="both", expand=True)
            scrollbar2 = ttk.Scrollbar(text_frame2, orient="vertical", command=text2.yview)
            scrollbar2.pack(side="right", fill="y", padx=(0, 5))  # Adjusted padx value
            text2.configure(yscrollcommand=scrollbar2.set)

            # Save question and answers when the button is clicked
            save_button = ttk.Button(question_frame, text="Save",
                                     command=lambda q=entry1, o=text1, a=text2: self.save_question(q, o, a))
            save_button.grid(row=5, column=1)

        button = ttk.Button(self, text="Next",
                            command=lambda: self.print(controller))
        button.grid(row=x+1, column=1, padx=10, pady=10)

    def clear_all(self):
        for widget in self.frame_container.winfo_children():
            widget.destroy()

    def save_question(self, question_entry, options_text, answer_entry):
        question = question_entry.get()
        options = options_text.get("1.0", "end-1c").split('\n')
        answer = answer_entry.get("1.0", "end-1c").split('\n')

        self.questions.append({
            'label': question,
            'options': options,
            'answer': answer
        })
        # # Clear the entry and text widgets after saving
        # question_entry.delete(0, tk.END)
        # options_text.delete("1.0", tk.END)
        # answer_entry.delete(0, tk.END)

    def print(self,controller):
        # for i in self.questions:
        #     print(i)
        global val, quiz_num_items
        html_report_part1 = open('Interactive Offline Course/CMSC 206/template/quiz_template.html','r')
        soup = BeautifulSoup(html_report_part1, 'html.parser')
        soup_new = copy.deepcopy(soup)
        new_title = soup_new.find('title')
        new_title.string = "Topic "+str(val)+" Quiz"
        new_h2 = soup_new.find("h2")
        new_h2.string = "Topic "+str(val)+" Quiz"
        new_script = soup_new.find_all('script')[-1].getText()
        # print(type(new_script))
        new_script = new_script.replace('ITEM_COUNT = "#X#"', 'ITEM_COUNT = ' + str(quiz_num_items[val]))
        questions = "var questions =["
        for i in self.questions:
            questions += str(i)+","
        questions += '];'
        new_script = new_script.replace('var questions="#X#"',questions)
        script_tag = soup_new.find_all("script")[-1]
        # print(new_script)
        script_tag.string = new_script
        # print(script_tag.string)
        # print(soup_new.prettify())
        html_output = soup_new.prettify(formatter="html")
        with open("Interactive Offline Course/CMSC 206/quiz/quiz"+str(val)+ ".html", "w", encoding="utf-8") as file:
            file.write(html_output)

        # print(soup_new.prettify())
        controller.frames[QuizMakerPage].refresh(controller)
        controller.show_frame(QuizMakerPage)
        
    
app = tkinterApp()  
app.mainloop()