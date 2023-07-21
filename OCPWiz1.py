import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

root = tk.Tk()
root.geometry('700x450')
root.title('OCPWizard')
root.resizable(False, False)

faculty=""
course_no = ""
course_title=""
course_intro=[]
course_guide_dir = ""
resources_dir=[]
num_topics = 0
topics_dir = {}
num_questions = {}
questions = {}

def indicate(nd,page):
    not_indicate()
    nd.config(bg="#00573F")
    page()

def course_info_page():
    course_info_page=tk.Frame(main_frame)
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

    course_no_entry=tk.Entry(course_info_page,font=('Helvtica',12),width=29)
    course_no_entry.grid(row=2,column=2,sticky=tk.E,pady=10)

    course_title_label=tk.Label(course_info_page, text="Course Title:",font=('Helvtica',12))
    course_title_label.grid(row=3,column=1,sticky=tk.W,pady=10)

    course_title_entry=tk.Entry(course_info_page,font=('Helvtica',12),width=29)
    course_title_entry.grid(row=3,column=2,sticky=tk.E,pady=10)

    save_btn=tk.Button(course_info_page,text="Save", font=('Helvetica',12),width=14,
                       command=lambda: save())
    save_btn.grid(row=4,column=2,sticky=tk.E,pady=10)

    def save():
        global faculty, course_no, course_title
        if clicked.get() == "" or course_no_entry.get() == "" or course_title_entry.get() == "":
            messagebox.showerror('Error', 'Error: Missing fields')
        else:
            faculty = clicked.get()
            course_no=course_title_entry.get()
            course_title=course_title_entry.get()
            enable_btn("course_info")
        
def course_intro_page():
    course_intro_page=tk.Frame(main_frame)
    course_intro_page.place(relx=.5, rely=.5,anchor= tk.CENTER)

    course_intro_label=tk.Label(course_intro_page, text="Course Introduction:",font=('Helvtica',12))
    course_intro_label.grid(row=1,column=1,sticky=tk.W,pady=10)

    text_frame=tk.Frame(course_intro_page)

    scrollbar=tk.Scrollbar(text_frame)

    course_intro_text=tk.Text(text_frame,yscrollcommand = scrollbar.set,width=45,height=10,font=('Helvtica',12))
    course_intro_text.grid(row=0,column=0)

    scrollbar.grid(row=0,column=1,sticky="NS")
    scrollbar.config( command = course_intro_text.yview )

    text_frame.grid(row=2, column=1, pady=10)

    save_btn=tk.Button(course_intro_page,text="Save", font=('Helvetica',12),width=14,
                       command=lambda: save())
    save_btn.grid(row=3,column=1,sticky=tk.E,pady=10)

    def save():
        global course_intro
        temp=course_intro_text.get("1.0",'end-1c').split('\n')
        if len(temp) == 1 and temp[0]=='':
            msg_box = messagebox.askokcancel("Empty", "No Course Information\nAre you sure?")
            if msg_box:
                course_intro =temp
        else:
            course_intro=temp

def resources_page():
    global course_guide_dir
    
    resources_page=tk.Frame(main_frame)
    resources_page.place(relx=.5, rely=.5,anchor= tk.CENTER)

    course_guide_btn = tk.Button(resources_page,text="Upload Course Guide", font=('Helvetica',12),width=30,
                       command=lambda: course_guide_save())
    course_guide_btn.grid(row=1,column=1,sticky=tk.W,pady=10)

    if course_guide_dir != "":
        course_guide_btn.config(text="Change Course Guide")

    resources_btn = tk.Button(resources_page,text="Add Folders", font=('Helvetica',12),width=30,
                       command=lambda: folder_save())
    resources_btn.grid(row=2,column=1,sticky=tk.W,pady=10)

    files_btn = tk.Button(resources_page,text="Add Files", font=('Helvetica',12),width=30,
                       command=lambda: file_save())
    files_btn.grid(row=3,column=1,sticky=tk.W,pady=10)

    files_btn = tk.Button(resources_page,text="Remove Resources", font=('Helvetica',12),width=30,
                       command=lambda: remove_resources())
    files_btn.grid(row=4,column=1,sticky=tk.W,pady=10)

    print(resources_dir)
    
    def course_guide_save():
        global course_guide_dir
        source = filedialog.askopenfilename(initialdir="/", title="Select file",
                                            filetype=(("PDF", "*.pdf"), ("All Files", "*.*")))
        if source:
            course_guide_dir=source
            course_guide_btn.config(text="Change Course Guide")
        else:
            messagebox.showerror("Error", "No file selected")

    def folder_save():
        global resources_dir
        path = '{}'.format(filedialog.askdirectory(title='Select Folder'))
        if path:
            if path in resources_dir:
                messagebox.showerror("Error", "Folder already added")
            else:
                resources_dir.append(path)
        else:
            messagebox.showerror("Error", "No folder selected")

    def file_save():
        global resources_dir
        source = filedialog.askopenfilename(initialdir="/", title="Select file",
                                            filetypes=(("All Files", ""),))
        if source:
            if source in resources_dir:
                messagebox.showerror("Error", "File already added")
            else:
                resources_dir.append(source)
        else:
            messagebox.showerror("Error", "No file selected")

    def remove_resources():
        global resources_dir
        if len(resources_dir) == 0:
            messagebox.showerror("Error", "No resources available")
        else:
            remove_top = tk.Toplevel()
            
            lb = tk.Listbox(remove_top)
            
            for x in range(0,len(resources_dir)):
                lb.insert(x, resources_dir[x])
            lb.grid(row=1,column=1,sticky="EW")
            
            delete_btn=tk.Button(remove_top,text="Delete",
                                 command=lambda: delete())
            delete_btn.grid(row=2,column=1,sticky=tk.E)
            
            def delete():
                selection = lb.curselection()
                lb.delete(selection[0])
                del(resources_dir[selection[0]])
                
                if lb.size()==0:
                    remove_top.destroy()
                # print(resources_dir)
            remove_top.mainloop()

def num_topics_page():
    num_topics_page=tk.Frame(main_frame)
    num_topics_page.place(relx=.5, rely=.5,anchor= tk.CENTER)

    num_topics_label=tk.Label(num_topics_page, text="No of Topics:",font=('Helvtica',12))
    num_topics_label.grid(row=1,column=1,sticky=tk.W,pady=10)

    num_topics_entry=tk.Entry(num_topics_page,justify=tk.CENTER,font=('Helvtica',12),width=29)
    num_topics_entry.grid(row=1,column=2,sticky=tk.E,pady=10)

    save_btn=tk.Button(num_topics_page,text="Save", font=('Helvetica',12),width=14,
                       command=lambda: save())
    save_btn.grid(row=2,column=2,sticky=tk.E,pady=10)

    def save():
        global num_topics, topics_dir, num_questions, questions
        
        if num_topics == 0:
            if num_topics_entry.get().isdigit() == True:
                if int(num_topics_entry.get()) < 1:
                    messagebox.showerror("Error","Please enter a valid number.")
                else:
                    num_topics = int(num_topics_entry.get())
                    temp = []
                    for x in range(num_topics):
                        temp.append(x+1)
                    topics_dir = dict.fromkeys(temp)
                    num_questions = dict.fromkeys(temp)
                    num_questions["final"] = None
                    questions = dict.fromkeys(temp)
                    questions["final"]=None
                    enable_btn("topics")
            else:
                messagebox.showerror("Error","Please enter only digits as no of topics!")
        else:
            msg_box = messagebox.askokcancel("Change of No of Topics", "Changeing the the number of topics will remove the uploaded PDFs and Questions?\nContinue?")
            if msg_box:
                topics_dir.clear()
                num_questions.clear()
                questions.clear()
                if num_topics_entry.get().isdigit() == True:
                    if int(num_topics_entry.get()) < 1:
                        messagebox.showerror("Error","Please enter a valid number.")
                    else:
                        num_topics = int(num_topics_entry.get())
                        temp = []
                        for x in range(num_topics):
                            temp.append(x+1)
                        topics_dir = dict.fromkeys(temp)
                        num_questions = dict.fromkeys(temp)
                        num_questions["final"] = None
                        questions = dict.fromkeys(temp)
                        questions["final"]=None
                        enable_btn("topics")
                else:
                    messagebox.showerror("Error","Please enter only digits as no of topics!")
        # print(num_topics, topics_dir, num_questions, questions)

def upload_topics_page():
    global num_topics, topics_dir

    upload_topics_page=tk.Frame(main_frame)
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

    for x in range(num_topics):
        button_text = ""
        if bool(topics_dir) and topics_dir[x+1] != None:
            button_text = "Change Topic " + str(x+1) + " PDF"
        else:
            button_text = "Upload Topic " + str(x+1) + " PDF"
        button = tk.Button(scrollable_frame, text=button_text,font=('Helvetica',12),width=30,
                           command=lambda value=x+1: button_click(value))
        button.grid(row=x+1,column=1,sticky=tk.E,pady=10)
        
    def button_click(value):
        global topics_dir
        
        if bool(topics_dir):
            source = filedialog.askopenfilename(initialdir="/", title="Select file",
                                            filetype=(("PDF", "*.pdf"), ("All Files", "*.*")))
            if source:
                if topics_dir[value] == None:
                    topics_dir[value] = source
                else:
                    # print(topics_dir[value])
                    msg_box = messagebox.askyesno("Replace Topic " + str(value+1) + " PDF", "Replace")
                    if msg_box == 'yes':
                        topics_dir[value] = source
            else:
                messagebox.showerror("Error", "No file selected")

def create_quiz_page():
    global num_topics,num_questions

    create_quiz_page=tk.Frame(main_frame)
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

    for x in range(num_topics):
        button_text = ""
        if bool(num_questions) and num_questions[x+1] != None:
            button_text = "Change Quiz " + str(x+1)
        else:
            button_text = "Create Quiz " + str(x+1)
        button = tk.Button(scrollable_frame, text=button_text,font=('Helvetica',12),width=30,
                           command=lambda value=x+1: button_click(value))
        button.grid(row=x+1,column=1,sticky=tk.E,pady=10)

    def button_click(value):
        num_questions_page(value)

def num_questions_page(value):
    pass

def enable_btn(type):
    if type=="course_info":
        course_intro_btn.config(state="normal")
        resources_btn.config(state="normal")
        num_topics_btn.config(state="normal")
    if type=="topics":
        upload_topics_btn.config(state="normal")
        create_quiz_btn.config(state="normal")
        create_final_btn.config(state="normal")

def not_indicate():
    course_info_nd.config(bg="#8A1538")
    course_intro_nd.config(bg="#8A1538")
    resources_nd.config(bg="#8A1538")
    num_topics_nd.config(bg="#8A1538")
    upload_topics_nd.config(bg="#8A1538")
    create_quiz_nd.config(bg="#8A1538")
    create_final_nd.config(bg="#8A1538")
    
    for x in main_frame.winfo_children():
        x.destroy()

options_frame = tk.Frame(root,bg="#8A1538")
options_frame.pack(side=tk.LEFT)
options_frame.pack_propagate(False)
options_frame.configure(width=150,height=450)

buttons_frame = tk.Frame(options_frame,bg="#8A1538")
buttons_frame.pack(side=tk.RIGHT)

course_info_nd = tk.Label(buttons_frame,height=2,bg="#8A1538")
course_info_nd.grid(row=1, column=1,pady=10)

course_intro_nd = tk.Label(buttons_frame,height=2,bg="#8A1538")
course_intro_nd.grid(row=2, column=1,pady=10)

resources_nd = tk.Label(buttons_frame,height=2,bg="#8A1538")
resources_nd.grid(row=3, column=1,pady=10)

num_topics_nd = tk.Label(buttons_frame,height=2,bg="#8A1538")
num_topics_nd.grid(row=4, column=1,pady=10)

upload_topics_nd = tk.Label(buttons_frame,height=2,bg="#8A1538")
upload_topics_nd.grid(row=5, column=1,pady=10)

create_quiz_nd = tk.Label(buttons_frame,height=2,bg="#8A1538")
create_quiz_nd.grid(row=6, column=1,pady=10)

create_final_nd = tk.Label(buttons_frame,height=2,bg="#8A1538")
create_final_nd.grid(row=7, column=1,pady=10)

course_info_btn = tk.Button(buttons_frame,
                            text="Course Information",width=15,height=1,font=('Helvetica', 10),bg="#8A1538",fg="#EEEEEE",
                            borderwidth=0,anchor="w",
                            command=lambda: indicate(course_info_nd, course_info_page))
course_info_btn.grid(row=1, column=2, columnspan=2,pady=10)

course_intro_btn = tk.Button(buttons_frame,
                            text="Course Intro",width=15,height=1,font=('Helvetica', 10),bg="#8A1538",fg="#EEEEEE",
                            borderwidth=0,anchor="w",state="disabled",
                            command=lambda: indicate(course_intro_nd, course_intro_page))
course_intro_btn.grid(row=2, column=2, columnspan=2,pady=10)

resources_btn = tk.Button(buttons_frame,
                            text="Resources",width=15,height=1,font=('Helvetica', 10),bg="#8A1538",fg="#EEEEEE",
                            borderwidth=0,anchor="w",state="disabled",
                            command=lambda: indicate(resources_nd,resources_page))
resources_btn.grid(row=3, column=2, columnspan=2,pady=10)

num_topics_btn = tk.Button(buttons_frame,
                            text="Number of Topics",width=15,height=1,font=('Helvetica', 10),bg="#8A1538",fg="#EEEEEE",
                            borderwidth=0,anchor="w",state="disabled",
                            command=lambda: indicate(num_topics_nd,num_topics_page))
num_topics_btn.grid(row=4, column=2, columnspan=2,pady=10)

upload_topics_btn = tk.Button(buttons_frame,
                            text="Upload Topics PDF",width=15,height=1,font=('Helvetica', 10),bg="#8A1538",fg="#EEEEEE",
                            borderwidth=0,anchor="w",state="disabled",
                            command=lambda: indicate(upload_topics_nd,upload_topics_page))
upload_topics_btn.grid(row=5, column=2, columnspan=2,pady=10)

create_quiz_btn = tk.Button(buttons_frame,
                            text="Create Quiz",width=15,height=1,font=('Helvetica', 10),bg="#8A1538",fg="#EEEEEE",
                            borderwidth=0,anchor="w",state="disabled",
                            command=lambda: indicate(create_quiz_nd,create_quiz_page))
create_quiz_btn.grid(row=6, column=2, columnspan=2,pady=10)

create_final_btn = tk.Button(buttons_frame,
                            text="Create Final Quiz",width=15,height=1,font=('Helvetica', 10),bg="#8A1538",fg="#EEEEEE",
                            borderwidth=0,anchor="w",state="disabled",
                            command=lambda: [indicate(create_final_nd)])
create_final_btn.grid(row=7, column=2, columnspan=2,pady=10)

back_btn = tk.Button(buttons_frame,
                            text="Create OCP",width=15,height=1,font=('Helvetica', 10),bg="#8A1538",fg="#EEEEEE",
                            borderwidth=0,anchor="w",)
back_btn.grid(row=8, column=2, columnspan=2,pady=10)

main_frame = tk.Frame(root,highlightbackground='black',highlightthickness=2)
main_frame.pack_propagate(False)
main_frame.configure(width=600,height=450)
main_frame.pack(side=tk.LEFT)

root.mainloop()