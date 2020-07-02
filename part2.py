import sys
import wx
import os
import pandas as pd

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
        lbl = wx.StaticText(self, label="Please Drag Peer_Consulting_Part1 here:\n")
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
        if "Peer_Consulting_Part1" in file:
            input = file


    outputdir = os.path.join(*path_to_list(input)[:-1])
    output = os.path.join(*[outputdir, "Peer_Consulting_Part2.tsv"])

    consultant_email = {}

    assignments = {}

    consultee_info = {}

    df = pd.read_excel(input)
    df = df.fillna("")

    max_size =0

    for index in df.index:
        row = df.iloc[index].tolist()
        consultant = row[7]
        if consultant != "" :
            assignments[consultant] = []


    for index in df.index:
        row = df.iloc[index].tolist()
        full_name = f'{row[3].replace(" ","")} {row[4].replace(" ","")}'
        email = row[0]
        consultant = row[7]
        consultee_full_name = f'{row[8]} {row[9]}'
        consultee_contact_info = row[10:13]
        consultee_contact_info.append(row[20])

        if email != "" :
            consultant_email[full_name] = email

        if consultant != "":
            assignments[consultant].append(consultee_full_name)
            if len(assignments[consultant]) > max_size:
                max_size = len(assignments[consultant])

        consultee_info[consultee_full_name] = consultee_contact_info

    with open(output, 'w', encoding='utf-8') as out:
        out.write("Consultant First Name\tConsultant Last Name\tEmail\t")
        myString = ""
        for i in range(1, max_size +1):
            myString += f'Consultee_{i}_Name\tConsultee_{i}_Email\tConsultee_{i}_Number\tConsultee_{i}_Major\tConsultee_{i}_DesiredHelp\t'
        myString = myString[:-1]
        out.write(f'{myString}\n')
        for consultant in consultant_email:
            myString =""
            myString += (consultant.replace(" ", "\t"))
            myString += (f"\t{consultant_email[consultant]}\t")
            total_assignments = assignments[consultant]
            for one_consultee in total_assignments:
                info = consultee_info[one_consultee]
                myString += (f'{one_consultee}\t')
                for value in info:
                    myString += (f'{value}\t')
            out.write(f'{myString[:-1]}\n')

    df = pd.read_csv(output, sep='\t')
    df.to_excel(output.replace("tsv","xlsx"), index=False)
    os.remove(output)

    sys.exit()
