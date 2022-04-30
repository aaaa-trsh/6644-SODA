from time import sleep, time

class Command():
    def __init__(self, periodic, timeout=-1):
        if periodic:
            self.periodic = periodic
        self.timeout = timeout
        print('schedule')

    def on_schedule(self):
        self.schedule_ts = time()
        print('schedule')

    def periodic(self):
        # print("nothing to do")
        pass

    def is_finished(self):
        if self.timeout is None or self.timeout < 0:
            return False
        return (time() - self.schedule_ts) >= self.timeout

class InstantCommand(Command):
    def __init__(self, to_run):
        super().__init__(None, 0)
        self.to_run = to_run

    def on_schedule(self):
        Command.on_schedule(self)
        self.to_run()

class Scheduler():
    def __init__(self):
        self.commands = []

    def schedule_command(self, command):
        self.commands.append(command)
        command.on_schedule()

    def remove_command(self, command):
        self.commands.remove(command)
    
    def periodic(self):
        for command in self.commands:
            if command.is_finished():
                self.remove_command(command)
            else:
                command.periodic()
        sleep(0.02)