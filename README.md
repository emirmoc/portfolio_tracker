# portfolio_tracker
Django app for tracking stock portfolio using multiple stock exchange API endpoints as source.

Portfolio tracking page:

![Alt text](portfolio_screenshots/portfolio.png?raw=true "Title")  

Administration page (after login):

![Alt text](portfolio_screenshots/admin-panel.png?raw=true "Title")  

**Installation**

The file initial-setup.sh located in the source code root contains the shell script necessary for getting the app up and running on your local Linux installation. You also need a local installation of Python. 

In case you are using Windows or Mac, you may need to install the GNU gettext:  
https://www.gnu.org/software/gettext/  
Then paste the lines 3-8 from the file initial-setup.sh into the terminal and execute them.

You will be required to enter username and password for a newly created app admin.

**Use**

To run the app on your local default browser, run the following lines in the application root:
```
source .env/bin/activate
exec ./manage.py runserver
```

The administration panel is accessible via:  
http://127.0.0.1:8000/admin/  

You can login with the username and password defined during the installation. You can add new asset symbols to track, add investments along with fees, as well as received dividends via the admin panel. You can also add investment filters.

Symbols can be added, edited, or deleted, along with custom links used for accessing information on upcoming dividends. The four SASE tickers added by default during installation can also be edited or deleted.

The portfolio tracker is accessible via:  
http://127.0.0.1:8000  
No login is required for viewing the portfolio status.

Currently available languages: English (default), Bosnian. To access a language different from default, add its code to query string:  
http://127.0.0.1:8000?lang=bs  

To filter investments by some category (e.g. "myfilter") add it to the query string:  
http://127.0.0.1:8000?lang=bs&filter=myfilter  

The file settings_local.py contains a list of different API endpoints for checking the ticker price. The checks are executed in sequence, so that if the ticker is found in the first API, the second one is skipped. If no ticker value is found, the portfolio page does not show the asset.

Currently available stock exchange APIs:  
http://www.sase.ba  
https://www.blberza.com  

The file settings_local.py is extensible. You can add any stock exchange API endpoint, provided that the endpoint returns a JSON array, the currencies match, and each field is correct.
