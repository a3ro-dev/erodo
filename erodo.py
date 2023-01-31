import sqlite3

# Connect to the database or create a new one if it doesn't exist
conn = sqlite3.connect('todo.db')
cursor = conn.cursor()

# Create the tasks table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS tasks (
    task_id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_name TEXT NOT NULL,
    task_description TEXT NOT NULL,
    due_date TEXT NOT NULL,
    status TEXT NOT NULL
)
''')

def add_task(task_name, task_description, due_date, status='Pending'):
    ''' Add a task to the tasks table '''
    cursor.execute('''
    INSERT INTO tasks (task_name, task_description, due_date, status)
    VALUES (?, ?, ?, ?)
    ''', (task_name, task_description, due_date, status))
    conn.commit()

def edit_task(task_id, task_name=None, task_description=None, due_date=None, status=None):
    ''' Edit a task in the tasks table '''
    updates = []
    parameters = []
    if task_name:
        updates.append('task_name = ?')
        parameters.append(task_name)
    if task_description:
        updates.append('task_description = ?')
        parameters.append(task_description)
    if due_date:
        updates.append('due_date = ?')
        parameters.append(due_date)
    if status:
        updates.append('status = ?')
        parameters.append(status)
    if not updates:
        return
    parameters.append(task_id)
    cursor.execute('''
    UPDATE tasks
    SET {}
    WHERE task_id = ?
    '''.format(', '.join(updates)), parameters)
    conn.commit()

def delete_task(task_id):
    ''' Delete a task from the tasks table '''
    cursor.execute('''
    DELETE FROM tasks
    WHERE task_id = ?
    ''', (task_id,))
    conn.commit()

def get_tasks():
    ''' Get all tasks from the tasks table '''
    cursor.execute('''
    SELECT * FROM tasks
    ''')
    return cursor.fetchall()

if __name__ == "__main__":

    while True:
        print('''
        
        Erodo
        Free To-Do List
        ---------------
        1. Add a new task.
        2. Get all tasks.
        3. Delete a task.
        4. Edit a task.
       
        ---------------
            ''')

        try:
            choice = int(input(": "))
        except ValueError as e:
            print(f"Invalid {e}")
        
        if choice == 1:
            taskname = input("Enter task name: \n")
            taskdescription = input("Enter task description: \n")
            time = input("Enter due-date or time: \n")
            add_task(task_name=taskname, task_description=taskdescription, due_date=time)
        if choice == 2:
            print(get_tasks())
        if choice == 3:
            taskid = input("Enter task id: \n")
            delete_task(taskid)
        if choice == 4:
            taskid = input("Enter task id: \n")
            taskname = input("Enter new task name: \n")
            taskdescription = input("Enter new task description: \n")
            time = input("Enter new due-date or time: ")
            sttus = input("Enter new task status: \n")
            edit_task(taskid, taskname, taskdescription, time, sttus)

# Close the database connection
conn.close()
