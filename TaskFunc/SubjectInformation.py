from psychopy import gui
def SubjectInformation():
    
    # Make a GUI dialogue to receive sub data
    dataDlg = gui.Dlg(title = "Subject data")
    dataDlg.addText('For subject ID, change the last two digits only!')
    dataDlg.addField('Subject ID (three digit):', 100)
    dataDlg.addField('Age:', 1)
    dataDlg.addField('Gender:', choices=["Male", "Female"])
    dataDlg.addField('Race:', choices=["Caucasian", "African-American", "Asian", "Hispinic", "Native-American"])
    
    # define a flag to use in a while loop
    vflag=True
    
    # Check the entered information
    while vflag:
        IDflag = False
        AGEflag = False
        
        subdata = dataDlg.show()
        
        # Sub ID should be an integer with 3 digits and should be less than 200
        # Example correct inputs: 101, 120 (last two digits are sub ID)
        if isinstance(subdata[0], int) and len(str(subdata[0])) ==3 and subdata[0]<200 and subdata[0]>100:
            IDflag = True
        else: 
            errorDlg = gui.Dlg()
            errorDlg.addText('Subject ID should be 3 digit integer starting with 1')
            errorDlg.addText('For example, 101 or 106')
            errorDlg.show()
            continue
            
        # Subject age should be an two-digit integer bigger than 18
        if isinstance(subdata[1], int) and len(str(subdata[1])) ==2 and subdata[1]>=18:
            AGEflag = True
        else: 
            errorDlg = gui.Dlg()
            errorDlg.addText('AGE should be 2 digit integer. You should be older than 18.')
            errorDlg.show()
            continue
             
        
        # If sub ID and age are correctly entered, exit the while loop
        if IDflag==True and AGEflag==True:
            vflag=False
            
    
    # Show winodw informing that the sub data are correctly registered
    ConfirmDlg = gui.Dlg()
    ConfirmDlg.addText('Subject information succesfully registered!')
    ConfirmDlg.show()
    
    subdata[0] = str(subdata[0])
    subdata[1] = str(subdata[1])
    
    # return subdata
    return(subdata)