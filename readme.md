## Python Behave API Testing Accelerator

<br/>

>### This solution/accelerator helps in automating API scenarios in python using Behave Framework. This will help in automating complex functional scenarios and can be executed on different environments as per the requirement. This solution supports different data parsers such as google sheets, excel, csv, json. This solution supports parallel and sequential execution and after completion of execution the standard reports are available.


<br />

### Folder structure
    src
    |- allure_reports
        |--reports
            |--- ...
        |--results
            |--- ...        
    |- readme.md
    |- requirements.txt
    |- behave-parallel.py
    |- config
        |-- ...                  
    |- data_providers
        |-- ...
    |- reports
        |-- ...                 
    |- logs
        |-- ...               
    |- tests
        |-- features
            |--- ...
        |-- steps
            |--- ...
        |-- utils
            |--- ...
            
- **`Tests`:** under 'Features' keep all test cases implementation files with .feature extension.
- **`Steps`:** keep Step Definition files with .py extensions. 
- **`Testdata`:** keep respective environment Test data here, Test data can be in the form of json, csv or excel. 
- **`Config`:** keep config files here such as db_config and google_config and in respective config file you can keep configurations as per the environment.
- **`Utils`:** keep Project utility files here .
- **`Helper`:** keep Common helper files here such as api_helper, db_helper etc.
- **`Data_providers`:** keep all the Data Provider implementation files in .py extension such as csv, json, excel, google sheet etc.


### Dependencies
-   Python version 2.7.x
-   behave 1.2.6
-   WooCommerce 2.1.1
-   Faker 3.0.1
-   configparser 4.0.2
-   parse 1.17.0
-   xlrd 1.2.0
<br />

- **`To use google-sheets, please install the given below packages:`**
  -   google-api-core 1.22.1
  -   google-api-python-client 1.11.0
  -   google-auth 1.21.1
  -   google-auth-httplib2 0.0.4
  -   httplib2 0.18.1
  -   oauth2client 4.1.3

### Prerequisite
- To setup the Application under test locally, please refer to the document ```Setup Application Under Test Locally.docx```
- To execute the test cases, we would need to setup the website on our local machine, please refer to the document:<br />```Site Setup on local Machine.docx```

- Download dependencies by using the following command:<br />```pip install -r requirements.txt```

### Config Parameters
- The base url of API is configurable and can be configured in `api_helper.py` in `Helper` folder.
- Environment of base url, Consumer Key and Consumer Secret is configurable and can be configured in `api_config.json` in `Config` folder.
- Database credentials and port are configurable and can be configured in `db_config.json` in `Config` folder.
- Google Sheets data are configurable and can be configured in `google_config.json` in `Config` folder.
- The Consumer Key and Consumer Secret is used as the credentials to connect to REST API and is added in system environment of the machine and is used in `api_helper.py` file. 
- To add logging as to show it in the log file, use the `logger_utility` from `Data providers` folder.

### Running Tests
<br />

- ### Execution from Command line
  - ### Arguments and their usage explanation:
      - **`--processes`:** Used to input number of parallel processes to run at a time.
      - **`--allure_reporting`:** Used to generate allure reports.
      - **`--junit_reporting`:** Used to generate junit reports.
      - **`-D log_level`:** Used to set the level of logging.
  
  - ### Execute a specific test feature : 
    - Navigate to src\ in cmd and run,<br />
      -  ```behave tests/features/$FILE_NAME.feature -k -f plain  -D log_level=$LOG_LEVEL```

  - ### Execute a specific test feature with allure reports:
    -  Navigate to src\ in cmd and run below command:
       - ```behave tests/features/$FILE_NAME.feature -k -f plain  -D log_level=$LOG_LEVEL -f allure_behave.formatter:AllureFormatter -o allure_reports/results```
  
  - ### Execute all tests without Allure Reports and Junit Reports:     
    - ### Execute all tests in sequential without allure reports: 
      - Navigate to src and run below command:
        -  ```python behave-parallel.py -D log_level=$LOG_LEVEL --processes=1```

    - ### Execute all tests in parallel without allure reports: 
      - Navigate to src in cmd and run below command:
        -  ```python behave-parallel.py -D log_level=$LOG_LEVEL --processes=$NUM_OF_PROCESSES``` 
  - ### With Allure Reports and Junit Reports : 
  - ### Allure Reports
    -  Allure reports are generated in CSV and JSON format at first and than it is converted to HTML format.
    
  - ### Junit Reports
    - Junit reports are generated in XML format.
    - Output JUnit-compatible reports. When junit is enabled, all stdout and stderr will be redirected and dumped to the junit report, regardless of the “–capture” and “–no-capture” options.
  
  - ### To Execute all tests in sequential with allure reports: 
    - Navigate to src and run below command:
      - ```python behave-parallel.py -D log_level=$LOG_LEVEL --processes=1 --allure_reporting=true --junit_reporting=true```

  - ### Execute all tests in parallel with allure reports: 
    - Navigate to src and run below command:
      -  ```python behave-parallel.py -D log_level=$LOG_LEVEL --processes=$NUM_OF_PROCESSES --allure_reporting=true --junit_reporting=true```

  - ### Open Allure HTML report
    - After execution, To open the reports run the following command in terminal:
      -  ```allure open allure/reports``` 
    - We can also open it by navigating to `src/allure/reports` and open `index.html`.

### Test Logs
-   Test Logs are saved in location after the execution:<br />`src\logs`.

### Reports
-   Reports saved in location after execution:<br />`src\reports`.

### Allure Reports
-   Allure Reports are saved in location after the execution:<br />`src\allure\html_reports`.