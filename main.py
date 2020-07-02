import sys
import wx
import pandas as pd
import os

def remove_duplicates(df):
    if True in df.Q4.duplicated():
        print("\nFound Duplicates!!!\n")
        print([df.Q4.values[i] for i in range(0, len(df.Q4.duplicated())) if
               df.Q4.duplicated()[i] == True])
        print()
        df = df.loc[~(df.Q4.duplicated())]
        return df
    else:
        return df


def Insert_row(row_number, df, row_value):
    # Starting value of upper half
    start_upper = 0

    # End value of upper half
    end_upper = row_number

    # Start value of lower half
    start_lower = row_number

    # End value of lower half
    end_lower = df.shape[0]

    # Create a list of upper_half index
    upper_half = [*range(start_upper, end_upper, 1)]

    # Create a list of lower_half index
    lower_half = [*range(start_lower, end_lower, 1)]

    # Increment the value of lower half by 1
    lower_half = [x.__add__(1) for x in lower_half]

    # Combine the two lists
    index_ = upper_half + lower_half

    # Update the index of the dataframe
    df.index = index_

    # Insert a row at the end
    df.loc[row_number] = row_value

    # Sort the index labels
    df = df.sort_index()

    # return the dataframe
    return df

def path_to_list(path):
    folders = []
    while True:
        path, folder = os.path.split(path)
        if folder:
            folders.append(folder)
        else:
            if path:
                folders.append(path)
            break
    folders.reverse()
    return folders

myFiles = []

########################################################################
class MyFileDropTarget(wx.FileDropTarget):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, window):
        """Constructor"""
        wx.FileDropTarget.__init__(self)
        self.window = window
    # ----------------------------------------------------------------------
    def OnDropFiles(self, x, y, filenames):
        """
        When files are dropped, write where they were dropped and then
        the file paths themselves
        """
        i = 0


        self.window.SetInsertionPointEnd()
        self.window.updateText("\n%d file(s) dropped at %d,%d:\n" %
                               (len(filenames), x, y))
        for filepath in filenames:
            self.window.updateText(filepath + '\n')
            myFiles.append(filepath)

        return True

        ########################################################################


class DnDPanel(wx.Panel):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)

        file_drop_target = MyFileDropTarget(self)
        lbl = wx.StaticText(self, label="Drag your two qualtrics output files here:\n")
        self.fileTextCtrl = wx.TextCtrl(self,
                                        style=wx.TE_MULTILINE | wx.HSCROLL | wx.TE_READONLY)
        self.fileTextCtrl.SetDropTarget(file_drop_target)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(lbl, 0, wx.ALL, 5)
        sizer.Add(self.fileTextCtrl, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(sizer)


    # ----------------------------------------------------------------------
    def SetInsertionPointEnd(self):
        """
        Put insertion point at end of text control to prevent overwriting
        """
        self.fileTextCtrl.SetInsertionPointEnd()

    # ----------------------------------------------------------------------
    def updateText(self, text):
        """
        Write text to the text control
        """
        self.fileTextCtrl.WriteText(text)


########################################################################
class DnDFrame(wx.Frame):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, parent=None, title="Peer Consulting Filter Part 1")
        panel = DnDPanel(self)
        self.Show()

if __name__ == '__main__':
    app = wx.App(False)
    frame = DnDFrame()
    app.MainLoop()


    for file in myFiles:
        if "Consultant" in file:
            consultant_file = file
        elif "Consultee" in file:
            consultee_file = file

    outputdir = os.path.join(*path_to_list(consultee_file)[:-1])
    output = os.path.join(*[outputdir, "Peer_Consulting_Part1.xlsx"])

    df_consultant = pd.read_csv(consultant_file)
    df_consultee = pd.read_csv(consultee_file)

    df_consultee = df_consultee.fillna(" ")
    df_consultee.Q6 = df_consultee.Q6.replace(" ", "Undecided")
    df_consultant = df_consultant.fillna(" ")
    df_consultant.Q6 = df_consultant.Q6.replace(" ", "Undecided")

    columns_to_keep_consultee = [x for x in df_consultee.columns.values if x.startswith("Q") and " - " not in x]
    columns_to_keep_consultant = [x for x in df_consultant.columns.values if x.startswith("Q")]

    df_consultant = remove_duplicates(df_consultant)
    df_consultee = remove_duplicates(df_consultee)

    questions_consultants = df_consultant.iloc[0]
    questions_consultees = df_consultee.iloc[0]

    df_consultee = df_consultee[columns_to_keep_consultee]
    df_consultant = df_consultant[columns_to_keep_consultant]

    df_consultant = df_consultant.sort_values(by=["Q6"])
    df_consultee = df_consultee.sort_values(by=["Q6"])

    df_consultant = df_consultant.drop([0, 1])
    df_consultee = df_consultee.drop([0, 1])

    df_consultee = df_consultee.reset_index(drop=True)
    df_consultant = df_consultant.reset_index(drop=True)

    consultant_majors = {}
    consultee_majors = {}

    cols = ["Q4", "Q5", "Q7", "Q7_23_TEXT", "Q8", "Q10", "Q2", "Q3", "Q6"]

    df_consultant = df_consultant[cols]

    df_consultant.insert(9, "", ["" for x in df_consultant.index.values], True)

    df_consultee.insert(0, "Consultant Full Name", ["" for x in df_consultee.index.values], True)

    row_value = ["" for x in df_consultant.columns.values]

    df_consultee = df_consultee.rename(
        columns={"Q2": "Consultee First Name", "Q3": "Consultee Last Name", "Q6": "Major", "Q4": "Consultee Email",
                 "Q5": "Phone Number", "Q7": "Career Path", "Q7_23_TEXT": "Other Career Path",
                 "Q9": "Gender Preferance", "Q14": "Interests"})

    df_consultant = df_consultant.rename(
        columns={"Q2": "Consultee First Name", "Q3": "Consultee Last Name", "Q6": "Major", "Q4": "Consultant Email",
                 "Q7": "Career Path", "Q7_23_TEXT": "Other Career Path"})

    consultant_cols = [x for x in df_consultant.columns.values if not x.startswith("Q")]

    df_consultee = df_consultee.drop(columns=["Q14_14_TEXT", "Q8", "Q11"])

    df_consultant = df_consultant[consultant_cols]

    new_df_consultant = pd.DataFrame(columns=df_consultant.columns)
    new_df_consultee = pd.DataFrame(columns=df_consultee.columns)
    print(df_consultee)
    print(df_consultant)

    i = 0
    j = 0
    df_consultee.Major = df_consultee.Major.fillna("Undecided")
    while i < len(df_consultee.index.values) - 1:
        df_consultant.Major = df_consultant.Major.fillna("Undecided")
        if df_consultant.Major.loc[j] == df_consultee.Major.loc[i]:
            new_df_consultant = new_df_consultant.append(df_consultant.iloc[j], ignore_index=True)
            new_df_consultee = new_df_consultee.append(df_consultee.iloc[i], ignore_index=True)
            j += 1
            i += 1
            print('both are majoring in:', df_consultant.Major.loc[j])
        else:
            major_of_consultant = df_consultant.Major.iloc[j]
            major_of_consultee = df_consultee.Major.iloc[i]
            print('Major of consultant:', major_of_consultant, '\n', "Major of consultee:", major_of_consultee)

            my_dictionary = {major_of_consultant: "consultant", major_of_consultee: "consultee"}
            myList = [major_of_consultant, major_of_consultee]
            myList.sort()
            alphabetically_first = myList[0]
            print('Alphabetically_first', alphabetically_first, '\n')

            if my_dictionary[alphabetically_first] == "consultant":
                new_df_consultee = new_df_consultee.append(pd.Series(), ignore_index=True)
                new_df_consultant = new_df_consultant.append(df_consultant.iloc[j], ignore_index=True)
                j += 1
            else:
                new_df_consultant = new_df_consultant.append(pd.Series(), ignore_index=True)
                new_df_consultee = new_df_consultee.append(df_consultee.iloc[i], ignore_index=True)
                i += 1

        print(f'i = {i}')
        print(f'j = {j}')
        if j == len(df_consultant.index.values) - 1:
            df_consultant = df_consultant.append(pd.Series(), ignore_index=True)
        if j == len(df_consultee.index.values) - 1:
            break

    # new_df_consultant.to_excel("consultant.xlsx", index=False)
    # new_df_consultee.to_excel("consultee.xlsx", index=False)

    final_df = pd.concat([new_df_consultant, new_df_consultee], axis=1)
    final_df.to_excel(output, index=False)

    sys.exit()