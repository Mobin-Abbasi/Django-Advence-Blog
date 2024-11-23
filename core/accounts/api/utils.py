import threading


class EmailThread(threading.Thread):
    def __init__(self, email_obj):
        threading.Thread.__init__(self)
        self.email_obj = email_obj

    def run(self):
        # Send email using SMTP server
        self.email_obj.send()
