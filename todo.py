TASK = 0
STATUS = 1
DONE = True
NOT_DONE = False

def get_input():
    valid = {'1', '2', '3', '4', '5'}
    res = ""
    while res not in valid:
        res = input("\n> ")
        if res not in valid: print("Invalid Option")
    return res


def add_task():
    arr = []
    inp = input().capitalize()
    arr.append(inp)
    arr.append(NOT_DONE)

    tasks[get_id()] = arr
    

def show_all():

    if not tasks:
        print("No tasks yet")
        return

    print("\nTasks")
    print("------------------------------")
    for key, value in tasks.items():
        status = "✅" if value[STATUS] == DONE else "❌"
        print(f"{key:>2}. {value[TASK]:<20} {status}")
    print("------------------------------")


def verify_input():
    res = input("Task number >")
    while (res.isalpha() or res not in tasks.keys()):
        print('Invalid number')
        res = input("Task number >")
    return res


def mark_as_done():
    if not tasks:
        print("No tasks yet")
        return
    
    
    print('Mark ', end ='')
    id = verify_input()

    tasks[id][STATUS] = not tasks[id][STATUS] 
    

def delete_task():
    global task_count, tasks

    if not tasks:
        print("No tasks yet")
        return
    
    
    print('Delete ', end ='')
    id = verify_input()
    
    tasks.pop(id)
    task_count -= 1
    tasks = renumber_items()
    
    
def renumber_items():
    new = dict()
    for index, value in enumerate(tasks.values()):
        new[str(index+1)] = value

    return new


def get_id():
    global task_count
    task_count += 1
    return str(task_count)


def handle_input(inp, ):
    match int(inp):
        case 1:
            print("Adding task > ", end = "")
            add_task()
        case 2:
            print("\n ")
            show_all()
        case 3:
            mark_as_done()
        case 4:
            delete_task()


task_count = 0
tasks = dict()


# main loop
while True:

    print("\n========== TODO LIST ==========")
    show_all()

    print("\nMenu")
    print("--------------------------------")
    print("1  Add Task")
    print("2  Show Tasks")
    print("3  Mark Task Done/Undone")
    print("4  Delete Task")
    print("5  Quit")
    print("--------------------------------")

    inp = get_input()

    if inp == '5': 
        print("Done")
        break

    handle_input(inp)
