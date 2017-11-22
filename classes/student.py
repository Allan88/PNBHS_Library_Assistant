class Student:
    def __init__(self, form_class, student_id, name):
        self.form_class = form_class
        self.student_id = student_id
        self.name = name
        self.list_of_offenses = []

    def print_info(self):
        print("Form Class:", self.form_class)
        print("Student ID:", self.student_id)
        print("Name:", self.name)

    def print_offenses(self):
        for offense in self.list_of_offenses:
            print('-----')
            print(offense.classification)
            print(offense.barcode)
            print(offense.type)
            print(offense.title)
            print(offense.author)
            print(offense.dueDate)
            print('${:,.2f}'.format(offense.fine))

    def get_total_fines(self):
        sum_of_fines = 0.00
        for offense in self.list_of_offenses:
            sum_of_fines += offense.fine
        return sum_of_fines
