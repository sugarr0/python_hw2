import datetime
import enum
import json

statuses = ['новая', 'выполняется', 'ревью', 'выполнено']


class Status(enum.Enum):
    new = 0
    in_progress = 1
    review = 2
    done = 3
    cancelled = -1


class Task:
    def __init__(self, name='', description='', status=Status.new, date=datetime.date.today().isoformat(),
                 date_change=datetime.date.today().isoformat()):
        self._name = name
        self._description = description
        self._status = status
        self._date = date
        self._date_change = date_change

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def status(self):
        return self._status.name

    @status.setter
    def status(self, new_status):
        if self._status.value == -1:
            return
        elif new_status.value == -1:
            self._status = new_status
            self._date_change = datetime.date.today().isoformat()
        elif self._status.value + 1 == new_status.value or self._status.value - 1 == new_status.value:
            self._status = new_status
            self._date_change = datetime.date.today().isoformat()
        return

    @property
    def date(self):
        return self._date

    @property
    def date_change(self):
        return self._date_change


class TaskManager:
    def __init__(self, file_name='f'):
        self._file_name = file_name
        self._all_tascs = []
        with open(f'{file_name}.json') as json_file:
            for i in json.load(json_file):
                if i['status'] == 'new':
                    self._all_tascs.append(
                        Task(i['name'], i['description'], Status.new, i['date'], i['date_change']))
                elif i['status'] == 'in_progress':
                    self._all_tascs.append(
                        Task(i['name'], i['description'], Status.in_progress, i['date'], i['date_change']))
                elif i['status'] == 'review':
                    self._all_tascs.append(
                        Task(i['name'], i['description'], Status.review, i['date'], i['date_change']))
                elif i['status'] == 'done':
                    self._all_tascs.append(
                        Task(i['name'], i['description'], Status.done, i['date'], i['date_change']))
                elif i['status'] == 'cancelled':
                    self._all_tascs.append(
                        Task(i['name'], i['description'], Status.cancelled, i['date'], i['date_change']))
        self._history = []

    def add(self, task):
        self._all_tascs.append(task)

    def add_history(self, task):
        self._history.append(task)

    @property
    def history(self):
        return self._history

    @property
    def all_tascs(self):
        return self._all_tascs

    def save(self):
        list = []
        for i in self._all_tascs:
            d = {}
            d['name'] = i.name
            d['description'] = i.description
            d['status'] = i.status
            d['date'] = i.date
            d['date_change'] = i.date_change
            list.append(d)
        with open(f'{self._file_name}.json', 'w') as outfile:
            json.dump(list, outfile)


print("file name:")
file_name = input()
manager = TaskManager(file_name)
while True:
    print("New task - 1")
    print("All task - 2")
    print("History - 3")
    print("Exit - 4")
    k = input()
    if k == '1':
        print("Name of task:")
        name = input()
        print("Description of task:")
        description = input()
        print("Change status:")
        print("new - 1")
        print("in_progress - 2")
        print("review - 3")
        print("done - 4")
        print("cancelled - 5")
        k1 = input()
        if k1 == '1':
            task = Task(name, description, Status.new)
        elif k1 == '2':
            task = Task(name, description, Status.in_progress)
        elif k1 == '3':
            task = Task(name, description, Status.review)
        elif k1 == '4':
            task = Task(name, description, Status.done)
        elif k1 == '5':
            task = Task(name, description, Status.cancelled)
        else:
            print("invalid value")
            continue
        print("the task has been created")
        manager.add(task)
    elif k == '2':
        while True:
            list = manager.all_tascs
            for i in range(len(list)):
                print(
                    f'{i + 1}: {list[i].name}, {list[i].description}, {list[i].status}, {list[i].date}, {list[i].date_change}')
            print('изменить статус задачи - 1')
            print('exit - 2')
            k1 = input()
            if k1 == '1':
                print('enter the issue number:')
                n = int(input())
                if 0 < n <= len(list):
                    print("Change new status:")
                    print("new - 1")
                    print("in_progress - 2")
                    print("review - 3")
                    print("done - 4")
                    print("cancelled - 5")
                    k2 = input()
                    if k2 == '1':
                        list[n - 1].status = Status.new
                    elif k2 == '2':
                        list[n - 1].status = Status.in_progress
                    elif k2 == '3':
                        list[n - 1].status = Status.review
                    elif k2 == '4':
                        list[n - 1].status = Status.done
                    elif k2 == '5':
                        list[n - 1].status = Status.cancelled
                    else:
                        print("invalid value")
                        continue
                    manager.add_history(list[n - 1])
            elif k1 == '2':
                break
    elif k == '3':
        list = manager.history
        for i in range(len(list)):
            print(
                f'{i + 1}: {list[i].name}, {list[i].description}, {list[i].status}, {list[i].date}, {list[i].date_change}')

    elif k == '4':
        manager.save()
        break
