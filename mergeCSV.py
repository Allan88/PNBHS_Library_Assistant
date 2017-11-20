import csv

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import csv


class App:
    def __init__(self, master):
        self.filename = ""
        self.csvFines = ""
        self.csvOverdues = ""
        self.outputCsv = ""

        master.minsize(width=360, height=240)
        master.title("Allan's time saving csv merge thingy")
        frame = Frame(master)
        frame.pack()

        self.mergeButton = Button(
            frame, text="Merge fines and overdues", command=self.merge_overdues_and_fines
        )
        self.mergeButton.pack(side=LEFT)

        self.button = Button(
            frame, text="Exit", fg="red", command=frame.quit
        )
        self.button.pack(side=LEFT)

    def merge_overdues_and_fines(self):
        messagebox.showinfo("Welcome", "Please follow the following instructions VERY carefully otherwise the program "
                                       "will most like crap itself.")
        messagebox.showinfo("Step 1", "Firstly, after you hit OK, select the CSV file containing the OVERDUE books "
                                      "(the fines one comes next)")
        self.csvOverdues = filedialog.askopenfilename(title="Pick a file to clean",
                                                   filetypes=(("csv files", "*.csv"), ("All files", "*.*")))
        messagebox.showinfo("Step 2", "Secondly, select the CSV file containing the FINES (not the overdues)")
        self.csvFines = filedialog.askopenfilename(title="Pick a file to clean",
                                                      filetypes=(("csv files", "*.csv"), ("All files", "*.*")))
        messagebox.showinfo("Step 3", "Now, where would you like to save the output file (give it a name too!)?")
        self.outputCsv = filedialog.asksaveasfilename(filetypes=(("csv files", "*.csv"), ("All files", "*.*")))
        listOfOverdues = []
        listOfFines = []
        naughtyKids = []

        # Read in the overdues file
        with open(self.csvOverdues, newline='') as csvfile:
            inputFile = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in inputFile:
                # Remove all the header rows
                if not ' '.join(row).strip().startswith('Class') \
                        and not ' '.join(row).strip().startswith('Palmerston') \
                        and not ' '.join(row).strip().startswith('Date'):
                    listOfOverdues.append(' '.join(row).strip())

        # Read in the fines file
        with open(self.csvFines, newline='') as csvfile:
            inputFile = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in inputFile:
                # Remove all the header rows
                if not ' '.join(row).strip().startswith('Name') \
                        and not ' '.join(row).strip().startswith('Palmerston') \
                        and not ' '.join(row).strip().startswith('Date') \
                        and not ' '.join(row).strip().startswith('Borrower'):
                    listOfFines.append(' '.join(row).strip())

        def setCurrentFine():
            # Clear current dict data
            return {
                'formClass': "",
                'id': "",
                'surname': "",
                'name': "",
                'classification': "",
                'barcode': "",
                'type': "",
                'title': "",
                'author': "",
                'dueDate': "",
                'letter': "",
                'fine': "",
            }

        # Sort overdue books data into list of dictionaries
        currentFine = setCurrentFine()
        for i in range(len(listOfOverdues)):

            row = listOfOverdues[i].replace('"', '').split()

            if i % 2 == 0:
                currentFine["formClass"] = row[0]
                currentFine["id"] = row[1]
                currentFine["surname"] = row[2]
                try:
                    currentFine["name"] = row[3]
                except IndexError:
                    # Allows for single name entities
                    pass
            else:
                currentFine["classification"] = row[0]
                currentFine["barcode"] = row[1]
                currentFine["type"] = row[2]
                currentFine["title"] = ' '.join(listOfOverdues[i].split('   ')[1].split()[1:])
                currentFine["author"] = ' '.join(listOfOverdues[i].split('   ')[2].split('"')[0:2]).strip().strip('"') \
                    .replace('  ', ', ')
                currentFine["dueDate"] = row[-3]
                currentFine["letter"] = row[-2]
                currentFine["fine"] = row[-1]

                naughtyKids.append(currentFine.copy())
                currentFine = setCurrentFine()

        # Sort fine data into list of dictionaries
        for i in range(len(listOfFines)):
            row = listOfFines[i].replace('"', '').split()
            if i % 2 == 0:
                currentFine["surname"] = row[0]
                currentFine["name"] = row[1]
                currentFine["title"] = ' '.join(row[2:])
            else:
                currentFine["id"] = row[0]
                currentFine["formClass"] = row[1]
                currentFine["fine"] = row[-1]

                naughtyKids.append(currentFine.copy())
                currentFine = setCurrentFine()

        # Sort by surname
        sortedList = sorted(naughtyKids, key=lambda k: k['surname'])

        # Write to new CSV file
        with open(self.outputCsv+'.csv', 'w', newline='') as newcsvfile:
            finalFile = csv.writer(newcsvfile, delimiter=',')
            finalFile.writerow(
                ['Number', 'Name', 'Class', 'Title of very late book', 'Barcode', 'Type', 'Classification',
                 'Author', 'Date Due', 'Charge'])
            for row in sortedList:
                # Excludes teachers
                if row['formClass'] != 'TEACHER':
                    finalFile.writerow([row['id'], ' '.join([row['surname'] + ',', row['name']]), row['formClass'],
                                        row['title'].strip('"').strip(), row['barcode'], row['type'],
                                        row['classification'],
                                        row['author'].strip(';'), row['dueDate'], row['fine']])
        messagebox.showinfo("Done", "Files successfully merged!")


root = Tk()

app = App(root)

root.mainloop()
root.destroy()

