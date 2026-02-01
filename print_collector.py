
class PrintCollector():

    def __init__(self):
        
        self.messages = []

    def collect_message(self, message):

        self.messages.append(message)

    def collect_message_list(self, message_list):

        self.messages.extend(message_list)
    
    def clear_messages(self):

        self.messages.clear()