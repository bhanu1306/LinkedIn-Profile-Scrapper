#Instructions for execution
1. Make sure that the FIREFOX web browser is installed in host machine.

2. The application uses GeckoDriver for Firefox. The required version is provided along with the other files. It should be in the same folder as the SCRAPPER.PY.
If the user wants to place it in some other location, then the PATH System variable should be updated with the location(windows). 

3. Provide credentials for login in the following format in the "CREDENTIALS.CSV" file :
		USERNAME/EMAIL  --->  Username for login
		PASSWORD  ---> Password for login 
   example-   foo,foo@123
		
4. The employee's profile should be in the "PROFILES.CSV" in the following format:
		NAME,SURNAME,EMPLOYEE_PROFILE_LINK

5. It is a PYTHON 3 based application, so make sure the following modules are installed on the host machine:
	a. Selenium
	b. BeautifulSoup
	c. Pandas
	
6. "OLD_DATA.CSV" is a temporary file that is used for comparing the old data with the new data for any updations. No need to edit it.

7. The application executes after every 3 days.

8. After every execution, the application generates a CSV file with the DATE of the EXECUTION DAY as the file name.
'Name', 'Surname', 'Linkedin_profile', 'Count_contacts', 'Count_contacts_recruiter', 'Count_recommendations', 'Skills_updated', 'Title_updated', 'Description_updated'

9. The generated file contains the following data :
	Column                    ---- DataType
	
    Name                      ---- String
	Surname                   ---- String
	Linked_profile            ---- String
	Count_contacts            ---- Integer
	Count_contacts_recruiter  ---- Integer
	Count_recommendations     ---- Integer   # Count of Received Recommendations
	Skills_updated            ---- Integer/Boolean   # 0 ---> No ,  1 ---> Yes
	Title_updated             ---- Integer/Boolean   # 0 ---> No ,  1 ---> Yes
	Description_updated       ---- Integer/Boolean   # 0 ---> No ,  1 ---> Yes
	
10. The employees that are provided in the "PROFILES.CSV" file should be connected with Logged In user, otherwise the application will not be able to fetch the connections of that unconnected employee.