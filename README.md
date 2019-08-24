# Ticket selling platform
Ticket selling platform is an application for buying tickets for different events. Allows to choose seats in different standards (regular, premium and vip), pay for them and check reservations details. 

## Run app
To run app you need to have python 3 installed. Then you can use virtual enviroment to install additional requirements or just install them on your system. 

### Use virtualenv
If you do not want to use virtual enviroment just skip this steps.
But if you want, firstly install virtualenv with pip:
```
$ pip install virtualenv
```
Then in repository directory create virtual enviroment with use:
```
$ virtualenv env
```
To activate enviroment on linux system enter:
```
$ source env/bin/activate
```
and for windows system:
```
> env\Scripts\activate
```
After that you are ready to install requirements

### Install requirements
Application just need django framework and django-paypal library to be installed. Use *requirements.txt* file to install that. In repository directory run:
```
$ pip install -r requirements.txt
```

### Run server
Now we are ready to run our server. Go to *ticket_selling_platform/* directory and then run:
```
$ python manage.py runserver
```
Default port for localhost server is **8000**, but you can use customize it. For example to run server on 7000 port you should use:
```
$ python manage.py runserver 7000
```

After that got to http://127.0.0.1:8000/ (or http://127.0.0.1:7000/ if you use port 7000) in your web browser. The application is almost ready to use...

### Adjust ngrok
For integration with paypal (receiving IPN - instatnt payment notification) application must be publicly accessible. It can be done with use of ngrok, which create secure URL for localhost server just with one commend.

Firstly open *ngrok.exe* and then use this commend to create tunel:
```
> ngrok http 8000
```
replace **8000** with your port number if you do not use default one.

The last step is changing **ALLOWED_HOSTS** in application settings. Without that the app will not work. Open *settings.py* file which you can find in *ticket_selling_platform/* directory, find **ALLOWED_HOSTS** parameter and change element with *ngrok.io* part to value from ngrok panel. It should looks like *8a9d924d.ngrok.io*.

And thats all. Now the app can receive paypal notifications.

## Payment 
To try payment you can use following fictitious account:
* login:
customer1test@email.com
* password:
Customer
