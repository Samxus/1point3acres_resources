class seed:
    def __init__(self):
        self.url = ''
        self.title = ''
        self.time = ''
        self.last_post = ''
        self.reply = 0
        self.view = 0
        self.tag = ''

    def __str__(self):
        return f'url: {self.url}, title: {self.title}, tag: {self.tag}, reply: {self.reply}, view: {self.view}, time: {self.time}, last_post: {self.last_post}'
