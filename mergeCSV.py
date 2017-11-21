import csv
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox


class App:
    def __init__(self, master):
        self.filename = ""
        self.fines_csv = ""
        self.overdue_books_csv = ""
        self.output_csv = ""

        master.minsize(width=360, height=240)
        master.title("Allan's time saving csv merge thingy")
        frame = Frame(master)
        frame.pack()

        self.mergeButton = Button(
            frame, text="Merge fines and overdue books CSVs", command=self.merge_overdue_books_and_fines
        )
        self.mergeButton.pack(side=LEFT)

        self.button = Button(
            frame, text="Exit", fg="red", command=frame.quit
        )
        self.button.pack(side=LEFT)

    def merge_overdue_books_and_fines(self):
        messagebox.showinfo("Welcome", "Please follow the following instructions VERY carefully otherwise the program "
                                       "will most like crap itself.")
        messagebox.showinfo("Step 1", "Firstly, after you hit OK, select the CSV file containing the OVERDUE books "
                                      "(the fines one comes next)")
        self.overdue_books_csv = filedialog.askopenfilename(title="Pick the OVERDUE BOOKS CSV",
                                                            filetypes=(("csv files", "*.csv"), ("All files", "*.*")))
        messagebox.showinfo("Step 2", "Secondly, select the CSV file containing the FINES (not the overdue books)")
        self.fines_csv = filedialog.askopenfilename(title="Pick the FINES CSV",
                                                    filetypes=(("csv files", "*.csv"), ("All files", "*.*")))
        messagebox.showinfo("Step 3", "Now, where would you like to save the output file (give it a name too!)?")
        self.output_csv = filedialog.asksaveasfilename(filetypes=(("csv files", "*.csv"), ("All files", "*.*")))
        overdue_books_list = []
        list_of_fines = []
        naughty_kids = []

        # Read in the overdue books file
        with open(self.overdue_books_csv, newline='') as csv_file:
            input_file = csv.reader(csv_file, delimiter=',', quotechar='|')
            for row in input_file:
                # Remove all the header rows
                if not ' '.join(row).strip().startswith('Class') \
                        and not ' '.join(row).strip().startswith('Palmerston') \
                        and not ' '.join(row).strip().startswith('Vertical') \
                        and not ' '.join(row).strip().startswith('Date'):
                    overdue_books_list.append(' '.join(row).strip())

        # Read in the fines file
        with open(self.fines_csv, newline='') as csv_file:
            input_file = csv.reader(csv_file, delimiter=',', quotechar='|')
            for row in input_file:
                # Remove all the header rows
                if not ' '.join(row).strip().startswith('Name') \
                        and not ' '.join(row).strip().startswith('Palmerston') \
                        and not ' '.join(row).strip().startswith('Date') \
                        and not ' '.join(row).strip().startswith('Borrower'):
                    list_of_fines.append(' '.join(row).strip())

        def set_current_fine():
            # Clear current dict data
            return {
                'formClass': "-",
                'id': "-",
                'surname': "-",
                'name': "-",
                'classification': "-",
                'barcode': "-",
                'type': "-",
                'title': "-",
                'author': "-",
                'dueDate': "-",
                'letter': "-",
                'fine': "-",
            }

        # Sort overdue books data into list of dictionaries
        current_fine = set_current_fine()
        for i in range(len(overdue_books_list)):
            row = overdue_books_list[i].replace('"', '').split()
            try:
                person = overdue_books_list[i].split('"')[1]
            except IndexError:
                # If person doesn't have a comma in their name, it doesn't generate quotations
                # so can't split by them
                person = overdue_books_list[i].split('  ')[1]

            if i % 2 == 0:
                current_fine["formClass"] = row[0]
                current_fine["surname"] = person.split()[0]
                try:
                    current_fine["name"] = person.split()[1]
                except IndexError:
                    # Allows for single name entities
                    current_fine["name"] = '-'
                current_fine["title"] = overdue_books_list[i].split("    ")[1]
                current_fine["barcode"] = row[-2]
            else:
                current_fine["id"] = row[0]
                current_fine["classification"] = row[-2]

                current_fine["type"] = row[-3]

                try:
                    current_fine["author"] = person.replace('  ', ', ')
                except IndexError:
                    current_fine["author"] = '-'

                current_fine["dueDate"] = row[-1]

                naughty_kids.append(current_fine.copy())
                current_fine = set_current_fine()

        # Sort fine data into list of dictionaries
        for i in range(len(list_of_fines)):
            row = list_of_fines[i].replace('"', '').split()
            if i % 2 == 0:
                current_fine["surname"] = row[0]
                current_fine["name"] = row[1]
                current_fine["title"] = ' '.join(row[2:])
            else:
                current_fine["id"] = row[0]
                current_fine["formClass"] = row[1]
                current_fine["fine"] = row[-1]

                naughty_kids.append(current_fine.copy())
                current_fine = set_current_fine()

        # Sort by surname
        sorted_list = sorted(naughty_kids, key=lambda k: k['surname'])

        # Write to new CSV file
        with open(self.output_csv + '.csv', 'w', newline='') as new_csv_file:
            final_file = csv.writer(new_csv_file, delimiter=',')
            final_file.writerow(
                ['Number', 'Name', 'Class', 'Title of very late book', 'Barcode', 'Type', 'Classification',
                 'Author', 'Date Due', 'Charge'])
            for row in sorted_list:
                # Excludes teachers
                if row['formClass'] != 'TEACHER':
                    final_file.writerow([row['id'], ' '.join([row['surname'] + ',', row['name']]), row['formClass'],
                                         row['title'].strip('"').strip(), row['barcode'], row['type'],
                                         row['classification'],
                                         row['author'].strip(';'), row['dueDate'], row['fine']])
        messagebox.showinfo("Done", "Files successfully merged!")


root = Tk()

app = App(root)

root.mainloop()
root.destroy()
