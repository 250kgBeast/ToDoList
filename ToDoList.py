from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return '{}. {}'.format(self.task, str(self.deadline))


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

to_do_list_loop = True


def add_task():
    print('Enter task ')
    task = input()
    print('Enter deadline ')
    deadline = input().split('-')
    new_row = Table(task=task,
                    deadline=datetime(int(deadline[0]), int(deadline[1]), int(deadline[2])))
    session.add(new_row)
    session.commit()
    print('The task has been added!')


def task_for_week():
    today = datetime.today()
    weekday = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    timedelta_index = 0
    while timedelta_index < 7:
        date = today + timedelta(days=timedelta_index)
        print(f"{weekday[date.weekday()]} {date.day} {date.strftime('%b')}:")
        if not session.query(Table).filter(Table.deadline == date.date()).all():
            print('Nothing to do!\n')
        else:
            for index, value in enumerate(session.query(Table.task).filter(Table.deadline == date.date()).all()):
                print(str(index + 1) + '. ' + value[0])
            print()
        timedelta_index += 1


def task_for_today():
    today = datetime.today().date()
    print('Today {} {}'.format(today.day, today.strftime('%b')))
    if not session.query(Table).filter(Table.deadline == today).all():
        print('Nothing to do!')
    else:
        for index, value in enumerate(session.query(Table).filter(Table.deadline == today).all()):
            print(str(index + 1) + '. ' + str(value))


def all_tasks():
    print('All tasks: ')
    for task_id, task, date in session.query(Table.id, Table.task, Table.deadline):
        print(f"{task_id}. {task}. {date.day} {date.strftime('%b')}")


def exit_to_do_list():
    global to_do_list_loop
    print('Bye!')
    to_do_list_loop = False


def menu():
    while to_do_list_loop:
        print("1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Add task\n0) Exit")
        user_input = input()
        if user_input == '1':
            print()
            task_for_today()
            print()
        elif user_input == '2':
            print()
            task_for_week()
        elif user_input == '3':
            print()
            all_tasks()
            print()
        elif user_input == '4':
            print()
            add_task()
            print()
        elif user_input == '0':
            print()
            exit_to_do_list()


menu()
