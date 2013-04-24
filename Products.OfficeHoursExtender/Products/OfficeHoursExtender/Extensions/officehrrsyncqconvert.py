from zope.app.component.hooks import getSite     

connectionString = ""
try: 
     from Products.OfficeHoursExtender.secure import *
except ImportError:
     pass

def synchronize( self ):
        site = getSite()
        ret = ""
	OfficeHrs = ""
	Quarter = ""
        acad_term_code = ""
#        ret = ret + "\nconnectionString debug"
#        return connectionString
        people = site.people.listFolderContents(contentFilter={"portal_type" : "FSDPerson"})

        ret = ret + "\nConnecting to database via ODBC"
        
        import pyodbc
        connection = pyodbc.connect( connectionString )
        cursor = connection.cursor()

        ret = ret + "\nExecuting query - SELECT * FROM Ploneoh ORDER BY loginid"
        cursor.execute( "SELECT * FROM Ploneoh ORDER BY loginid" )      
        ret = ret + "\nQuery executed, iterating over the resulting rows"


        for row in cursor:
            ret = ret + "\nI am at ID:" + str( getattr( row, "LoginID" ) )
            existing = False  
           
            
            for person in people:
                # if the entry is already there, just edit it's properties
                if person.id == getattr( row, "LoginID" ):
                     existing = True
                     OfficeHrs = getattr( row, "OfficeHours")
      		     acad_term_code = getattr( row, "acad_term_code")
                     #split into quarter and year
                     year = acad_term_code[0:4]
                     quarter = acad_term_code[4:6]
                     #convert quarter to text
                     if quarter == "01":
                          cquarter = "Winter"
                     elif quarter == "03":
                          cquarter = "Spring"
                     elif quarter == "10":
                          cquarter = "Fall"
                     elif quarter == "05":
                          cquarter = "Summer Session I"
                     elif quarter == "07":
                          cquarter = "Summer Session II"
                     else:
                          cquarter = "unrecognized quarter"
                     quarterYear = str(cquarter + " " + year)
                       
                     break
                     
 
            if existing:
                ret = ret + "\n ... entry is already there, updating it's properties"
	        person.getField('officeHours').set(person, OfficeHrs)
                person.getField('quarter').set(person, quarterYear) 
                
            else:
                ret = ret + "\n ... entry isn't in the system"
               
            # now set your properties to zope object
            
            
            
        connection.close()
        ret = ret + "\nSynchronization ran successfully!"
        return ret
      

     
