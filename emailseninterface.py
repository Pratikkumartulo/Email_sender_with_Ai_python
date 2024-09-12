import tkinter as tk
import smtplib as s
from config import groq_api
import re
from groq import Groq


subject = ""
body = ""
client = Groq(
 api_key=groq_api,
)

def generate_response():
 global subject,body
 user_input = ai_prompt_field.get("1.0","end")
 chat_completion = client.chat.completions.create(
 messages=[
 {
 "role": "user",
 "content": f"dont write anyother information , just {user_input}",
 }
 ],
 model="llama3-8b-8192",
 )
 response_content = chat_completion.choices[0].message.content
 ai_generate_field.delete("1.0", tk.END)
 ai_generate_field.insert("1.0",response_content)


def verify_mail():
    try:
        ob = s.SMTP('smtp.gmail.com', 587)
        ob.ehlo()
        ob.starttls()
        ob.login(entry_field_one.get(), entry_field_two.get())
        status_field.config(state=tk.NORMAL)
        status_field.delete(0,tk.END)
        status_field.insert(0,"Email verified successfully !!")
        status_field.config(state=tk.DISABLED)
        ob.quit()
    except Exception as e:
        status_field.config(state=tk.NORMAL)
        status_field.delete(0,tk.END)
        status_field.insert(0,"INVALID EMAIL ID OR APP PASSWORD !")
        status_field.config(state=tk.DISABLED)

def send(mails):
    try:
        body = body_widget.get("1.0","end")
        ob = s.SMTP('smtp.gmail.com',587)
        ob.ehlo()
        ob.starttls()
        ob.login(entry_field_one.get(), entry_field_two.get())
        message = f"subject:{subject_field.get()}\n\n{body}".encode('utf-8') 
        ob.sendmail(f'{entry_field_one.get()}',mails,message)
        status_field.config(state=tk.NORMAL)
        status_field.delete(0,tk.END)
        status_field.insert(0,"Mail sent succesfully !")
        status_field.config(state=tk.DISABLED)
        ob.quit()
    except Exception as e:
        status_field.config(state=tk.NORMAL)
        status_field.delete(0,tk.END)
        status_field.insert(0,e)
        status_field.config(state=tk.DISABLED)

def verify_reciever(mail):
    email_condition = r"^[a-z]+[\._]?[a-z 0-9]+[@]\w+[.]\w{2,3}$"
    return re.search(email_condition,mail)

def recievers():
    recievers = recipient_field.get("1.0", "end").strip().split(",")
    recievers = [mail.strip() for mail in recievers]
    length = len(recievers)
    count = 0
    for mail in recievers:
        if not verify_reciever(mail):
            status_field.config(state=tk.NORMAL)
            status_field.delete(0,tk.END)
            status_field.insert(0,f"{mail} is not a valid mail")
            status_field.config(state=tk.DISABLED)
            break
        else:
            count+=1
    if count==length:
        send(recievers)

def send_ai_gen(mails):
    try:
        response_content = ai_generate_field.get("1.0","end")
        if "Subject:" in response_content:
            parts = response_content.split("Subject:", 1)
            subject = parts[1].split("\n", 1)[0].strip() 
            body = parts[1].split("\n", 1)[1].strip() 
        else:
            subject = "No Subject"
            body = response_content.strip()
        ob = s.SMTP('smtp.gmail.com',587)
        ob.ehlo()
        ob.starttls()
        ob.login(entry_field_one.get(), entry_field_two.get())
        message = f"subject:{subject}\n\n{body}".encode('utf-8') 
        ob.sendmail(f'{entry_field_one.get()}',mails,message)
        status_field.config(state=tk.NORMAL)
        status_field.delete(0,tk.END)
        status_field.insert(0,"Mail sent succesfully !")
        status_field.config(state=tk.DISABLED)
        ob.quit()
    except Exception as e:
        status_field.config(state=tk.NORMAL)
        status_field.delete(0,tk.END)
        status_field.insert(0,e)
        status_field.config(state=tk.DISABLED)

def ai_recievers():
    recievers = recipient_field.get("1.0", "end").strip().split(",")
    recievers = [mail.strip() for mail in recievers]
    length = len(recievers)
    count = 0
    for mail in recievers:
        if not verify_reciever(mail):
            status_field.config(state=tk.NORMAL)
            status_field.delete(0,tk.END)
            status_field.insert(0,f"{mail} is not a valid mail")
            status_field.config(state=tk.DISABLED)
            break
        else:
            count+=1
    if count==length:
        send_ai_gen(recievers)

root = tk.Tk()
root.title("Email Sender")

#Start Frame here
start_frame = tk.Frame(root)
start_frame.grid(row=0, column=0, padx=20, pady=20)

field_one = tk.Label(start_frame, text="Your email:")
field_one.pack(side=tk.LEFT)
entry_field_one = tk.Entry(start_frame)
entry_field_one.pack(side=tk.LEFT, padx=10, pady=10)

field_two = tk.Label(start_frame, text="App password:")
field_two.pack(side=tk.LEFT)
entry_field_two = tk.Entry(start_frame, show="*") 
entry_field_two.pack(side=tk.LEFT, padx=10, pady=10)

verify_btn = tk.Button(start_frame, text="Verify Email", command=verify_mail)
verify_btn.pack(side=tk.LEFT)

#Second frame here
second_frame = tk.Frame(root)
second_frame.grid(row=1,column=0,padx=20,pady=20)

status_field = tk.Entry(second_frame,width=90)
status_field.pack(side=tk.LEFT)
status_field.delete(0,tk.END)
status_field.insert(0,"Email not verified !")
status_field.config(state=tk.DISABLED)

third_frame = tk.Frame(root)
third_frame.grid(row=2,column=0)

subject_frame = tk.Frame(third_frame)
subject_frame.pack(side=tk.TOP)
subject_label = tk.Label(subject_frame, text="Subject")
subject_label.pack(side=tk.LEFT)
subject_field = tk.Entry(subject_frame,width=90)
subject_field.pack(side=tk.LEFT)

body_frame = tk.Frame(third_frame)
body_frame.pack(side=tk.TOP)
body_label = tk.Label(body_frame,text="Body")
body_label.pack(side=tk.TOP)
body_widget = tk.Text(body_frame, height=30,wrap=tk.WORD)
body_widget.pack(side=tk.TOP)

send_btn = tk.Button(body_frame,text="send",width=10,command=recievers)
send_btn.pack(side=tk.TOP,padx=10,pady=10)


# Frame for multiple recipients
recipient_frame = tk.Frame(root)
recipient_frame.grid(row=0, column=1, padx=60, pady=20,sticky="ne",rowspan=5)

recipient_label = tk.Label(recipient_frame, text="Recipients (comma-separated):")
recipient_label.pack(side=tk.TOP)
recipient_field = tk.Text(recipient_frame, width=25, height=20)
recipient_field.pack(side=tk.TOP)


#AI frame from here --
ai_frame = tk.Frame(root)
ai_frame.grid(row=0,column=2,rowspan=5,sticky="n")

ai_label = tk.Label(ai_frame,text="Tri AI feature :")
ai_label.pack(side=tk.TOP)

ai_prompt_label = tk.Label(ai_frame,text="Promt here :")
ai_prompt_label.pack(side=tk.TOP)

ai_prompt_field = tk.Text(ai_frame,width=50,height=5)
ai_prompt_field.pack(side=tk.TOP)

ai_prompt_submit = tk.Button(ai_frame,text="Generate result",command=generate_response)
ai_prompt_submit.pack(side=tk.TOP,padx=20,pady=20)

ai_generate_field = tk.Text(ai_frame,width=70,height=28,wrap=tk.WORD)
ai_generate_field.pack(side=tk.TOP)

ai_Send_btn = tk.Button(ai_frame,width=10,text="Send",command=ai_recievers)
ai_Send_btn.pack(side=tk.TOP,padx=10,pady=10)


root.mainloop()
