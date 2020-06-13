from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

to_do_list_loop = True


def add_task():
    print('Enter task ')
    task = input()
    new_row = Table(task=task,
                    deadline=datetime.today())
    session.add(new_row)
    session.commit()
    print('The task has been added!')


def task_for_today():
    print('Today: ')
    if not session.query(Table).all():
        print('Nothing to do!')
    else:
        for index, value in enumerate(session.query(Table).all()):
            print(str(index + 1) + '. ' + str(value))


def exit_to_do_list():
    global to_do_list_loop
    print('Bye!')
    to_do_list_loop = False


def menu():
    while to_do_list_loop:
        print('''1) Today's tasks
2) Add task
0) Exit
        ''')
        user_input = input()
        if user_input == '1':
            task_for_today()
            print()
        elif user_input == '2':
            add_task()
            print()
        elif user_input == '0':
            exit_to_do_list()
            print()


menu()