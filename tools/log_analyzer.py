class LogAnalyzer():

    def __init__(self):
        self.ALLOWED_ERRORS = [
           "random_choice: Choosed emergency move"
        ]

    def analyse_errors(self, line, line_number):
        
        found_errors = []
        
        words = []
        for word in line.split():
            words.append(word)

        level = words[0]
        error = words[-1]
        if level == "ERROR":
            if error not in self.ALLOWED_ERRORS:
                text = f"ERROR found!: {line_number}: {error}"
                found_errors.append(text)

        self.print_found_errors(found_errors)

    def print_found_errors(self, found_errors):
        for error in found_errors:
            print(error)