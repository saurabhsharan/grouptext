# grouptext

Welcome to grouptext! grouptext makes it easy to manage groups of numbers to send SMS or MMS messages to.

## Setup

grouptext is written entirely in Python, and relies only on the `flask` and `twilio` libraries. To install these two libraries, run:

````
sudo pip install twilio
````

and

````
sudo pip install flask
````

Finally, create a new plain text file in the top-level directory called `secrets` (no file extension), containing exactly 2 lines. The first line is your Twilio account SID, and the second line is your Twilio auth token. For example:

````
TWILIO-SID
TWILIO-AUTH-TOKEN
````

## Usage

grouptext can be run as either a web app or in the command-line.

To run as a web app, simply run grouptext without any arguments or options:

````
python grouptext.py
````

The default port is 5000. Visit http://localhost:5000 in your browser.

To run in command-line mode, provide the name of the numbers CSV file as the only command-line argument:

````
python grouptext.py numbers.csv
````

In other words, grouptext will run as a web app when not provided any arguments, and will run in command-line mode when given the name of a numbers CSV file.

## Web App

The web app makes it easy to manage different groups of numbers and send SMS messages to those groups. Rather than using a separate database, the numbers are persisted in the same CSV files, making it easy to switch between using grouptext as a web app and in the command-line. For example, a group called `example` in the web app is stored as `example.csv` in the same top-level directory.

## Command-Line

The command-line mode prompts you for a text message to send to all numbers in the provided CSV file. For example, here's how you can tell everyone you're awesome:

````
> I'm awesome.
````

You can also send MMS messages with images by typing `MMS` followed by an image URL. For example, to send everyone a picture of a sushi emoji, enter:

````
> MMS http://pix.iemoji.com/sbemojix2/0294.png
````

