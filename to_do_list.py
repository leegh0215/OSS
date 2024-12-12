from tkinter import *
from tkinter import messagebox
import sqlite3 as sql
import json

# 파일 저장 경로
DO_FILE = "./do.json"

# 초기 데이터 로드
def load_do():
    try:
        with open(DO_FILE, 'r') as file:
            data = json.load(file)  # JSON 데이터를 읽어옴
            for item in data:
                if isinstance(item, dict) and "task" in item and "done" in item:
                    task = item["task"]
                    done = item["done"]
                    # task가 이미 데이터베이스에 있는지 확인
                    if task not in [row[0] for row in the_cursor.execute('SELECT title FROM tasks')]:
                        the_cursor.execute(
                            'INSERT OR IGNORE INTO tasks (title, done) VALUES (?, ?)',
                            (task, done)
                        )
    except FileNotFoundError:
        # 파일이 없으면 아무 작업도 하지 않음
        pass
    except json.JSONDecodeError:
        messagebox.showinfo('에러', 'JSON 파일을 읽는 중 오류가 발생했습니다.')


# 데이터 저장
def save_do():
  with open(DO_FILE, 'w', encoding='UTF-8') as file:
    json.dump(do_list, file, indent=4, ensure_ascii=False)

def add_do():
    do_string = do_field.get()
    if len(do_string) == 0:
        messagebox.showinfo('에러', '텍스트를 입력해 주세요!')
    else:
        # 새로운 작업을 do_list와 데이터베이스에 추가
        new_task = {"task": do_string, "done": False}
        do_list.append(new_task)
        the_cursor.execute('INSERT OR IGNORE INTO tasks (title, done) VALUES (?, ?)', (new_task["task"], new_task["done"]))
        list_update()
        do_field.delete(0, 'end')

def list_update():
    clear_list()
    for item in do_list:
        display_text = f"[{'✔' if item['done'] else ' '}] {item['task']}"
        do_listbox.insert('end', display_text)

def delete_do():
    try:
        # 선택한 항목의 인덱스 가져오기
        index = do_listbox.curselection()[0]
        selected_task = do_list[index]
        
        # do_list와 데이터베이스에서 삭제
        do_list.pop(index)
        the_cursor.execute('DELETE FROM tasks WHERE title = ?', (selected_task["task"],))
        list_update()
    except IndexError:
        messagebox.showinfo('에러', '지울 작업을 선택해 주세요!')   

def delete_all():
    message_box = messagebox.askyesno('초기화', '정말로 초기화하겠습니까??')        
    if message_box == True:
        while(len(do_list) != 0):
              do_list.pop()
        the_cursor.execute('delete from tasks')           
        list_update()

def toggle_done():
    try:
        index = do_listbox.curselection()[0]
        selected_task = do_list[index]
        selected_task["done"] = not selected_task["done"]  # 상태 토글
        the_cursor.execute(
            'UPDATE tasks SET done = ? WHERE title = ?',
            (selected_task["done"], selected_task["task"])
        )
        list_update()
    except IndexError:
        messagebox.showinfo('에러', '변경할 작업을 선택해 주세요!')

def clear_list():
    do_listbox.delete(0,'end')

def close():
    guiwindow.destroy()

def retrieve_database():
    while len(do_list) != 0:
        do_list.pop()
    
    for row in the_cursor.execute('SELECT title, done FROM tasks'):
        do_list.append({"task": row[0], "done": bool(row[1])})


if __name__ == "__main__":
    guiwindow = Tk()
    guiwindow.title("To do list")
    guiwindow.geometry("660x400+400+250")
    guiwindow.resizable(0, 1)
    the_connection = sql.connect('listofdo.db')
    the_cursor = the_connection.cursor()
    the_cursor.execute('CREATE TABLE IF NOT EXISTS tasks (title TEXT UNIQUE, done BOOLEAN)')

    do_list=[]
    
    functions_frame = Frame(guiwindow, bg = "floral white")        
    functions_frame.pack(side = "top", expand = True, fill = "both")

    do_label = Label(functions_frame,text="입력:",
        font = ("arial", "18", "bold"),
        background = "floral white",
        foreground = "black"
    )
    do_label.place(x = 90, y = 26)
    
    do_field = Entry( # 타이핑 공간
        functions_frame,
        font = ("arial","14"),
        width = 42,
        foreground = "black",
        background = "white",
    )
    do_field.place(x = 160, y = 30)

    add_button = Button(
        functions_frame,
        text = "할 일 추가",
        width = 15,
        bg = 'white', font = ("arial", "14", "bold"),
        command = add_do,
    )

    del_button = Button(  
        functions_frame,  
        text = "삭제",  
        width = 15,
        bg = 'white', font = ("arial", "14", "bold"),
        command = delete_do,  
    )  

    del_all_button = Button(  
        functions_frame,  
        text = "초기화",  
        width = 15,
        font = ("arial", "14", "bold"),
        bg = 'yellow',
        command = delete_all 
    )

    toggle_button = Button(
    functions_frame,
    text="완료 상태 변경",
    width=15,
    bg='green', font=("arial", "14", "bold"),
    command=toggle_done,
    )

    exit_button = Button(  
        functions_frame,  
        text = "프로그램 종료",  
        width = 51,
        bg = 'red',  font=("arial", "14", "bold"),
        command = close
    )  

    add_button.place(x = 18, y = 70,)  
    del_button.place(x = 230, y = 70)  
    del_all_button.place(x = 440, y = 70)
    toggle_button.place(x=440, y=110)
    exit_button.place(x = 17, y = 330)  

    do_listbox = Listbox(
        functions_frame,
        width = 68,
        height = 9,
        font = "bold",
        selectmode = 'single',
        background = "white",
        foreground = "black",
        selectbackground = "black",
        selectforeground = "blue"
    )

    do_listbox.place(x = 17, y = 140)

    load_do()
    retrieve_database()
    list_update()
    guiwindow.mainloop()
    the_connection.commit()
    the_cursor.close()
    save_do()