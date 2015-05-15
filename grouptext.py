#!/usr/bin/env python

from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
import glob
from optparse import OptionParser
import os.path
import sys
from twilio.rest import TwilioRestClient

TWILIO_ACCOUNT_SID = None
TWILIO_AUTH_TOKEN = None
TWILIO_FROM_NUMBER = '+14154888950'

def run_server_mode():
  flask_app = Flask('Grouptext')

  @flask_app.route('/')
  def grouptext():
    return render_template('grouptext.html')

  @flask_app.route('/numbers_files')
  def numbers_files():
    numbers_files = [filename[:-4] for filename in glob.glob('*.csv')]
    return jsonify(numbers_files=numbers_files)

  @flask_app.route('/numbers')
  def numbers():
    numbers = get_numbers_from_file(request.args.get('file') + '.csv')
    return jsonify(numbers=numbers)

  @flask_app.route('/create_numbers_file', methods=['POST'])
  def create_numbers_file():
    filename = request.form.get('file') + '.csv'
    if os.path.isfile(filename):
      resp = jsonify(error="File already exists with that name.")
      resp.status_code = 400
      return resp
    else:
      return jsonify()

  @flask_app.route('/add_number', methods=['POST'])
  def add_number():
    filename = request.form.get('file') + '.csv'
    number = request.form.get('number')
    if add_number_to_file(filename, number):
      return jsonify()
    else:
      resp = jsonify(error="%s is already in %s." % (number, filename))
      resp.status_code = 400
      return resp

  @flask_app.route('/delete_number', methods=['POST'])
  def delete_number():
    filename = request.form.get('file') + '.csv'
    number = request.form.get('number').strip()
    if delete_number_from_file(filename, number):
      return jsonify()
    else:
      resp = jsonify(error="%s is already in %s." % (number, filename))
      resp.status_code = 400
      return resp

  @flask_app.route('/send_sms', methods=['POST'])
  def send_sms():
    filename = request.form.get('file') + '.csv'
    message_body = request.form.get('message_body')

    numbers = get_numbers_from_file(filename)

    if message_body[:4] == "MMS ":
      image_url = message_body[4:]
      for number in numbers:
        send_mms_message(to_phone_number=number, media_url=image_url)
    else:
      for number in numbers:
        send_text_message(to_phone_number=number, message_body=message_body)

    return jsonify()

  flask_app.run(debug=True)

def get_numbers_from_file(numbers_filename):
  if not os.path.isfile(numbers_filename) and numbers_filename[-4:] != '.csv':
    numbers_filename = numbers_filename + '.csv'
  with open(numbers_filename, 'rU') as f:
    return [number.strip() for number in f.readlines()]

def add_number_to_file(numbers_filename, new_number):
  numbers = get_numbers_from_file(numbers_filename)
  if new_number in numbers:
    return False
  numbers.append(new_number)
  with open(numbers_filename, 'w') as f:
    for number in numbers:
      f.write(number + '\n')
  return True

def delete_number_from_file(numbers_filename, number):
  numbers = get_numbers_from_file(numbers_filename)
  if number not in numbers:
    return False
  numbers.remove(number)
  with open(numbers_filename, 'w') as f:
    for number in numbers:
      f.write(number + '\n')
  return True

def send_message(to_phone_number, message_body="", media_url=""):
  global TWILIO_ACCOUNT_SID
  global TWILIO_AUTH_TOKEN

  twilio_client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

  args = {
    'to': to_phone_number,
    'from_': TWILIO_FROM_NUMBER,
  }

  if message_body:
    args['body'] = message_body
  if media_url:
    args['media_url'] = media_url

  message = twilio_client.messages.create(**args)

  return message.sid

def send_mms_message(to_phone_number, media_url):
  return send_message(to_phone_number=to_phone_number, media_url=media_url)

def send_text_message(to_phone_number, message_body):
  return send_message(to_phone_number=to_phone_number, message_body=message_body)

def run_interactive_mode():
  numbers = get_numbers_from_file(sys.argv[1])

  print "Welcome to grouptext! Type a message and press enter to send a SMS message to every number. To send a MMS, enter \"MMS [imageurl]\""

  while True:
    try:
      message_body = raw_input("> ")
    except:
      break

    if not message_body:
      break

    if message_body[:4] == "MMS ":
      image_url = message_body[4:]
      for number in numbers:
        send_mms_message(to_phone_number=number, media_url=image_url)
      print "\"%s\" sent as MMS to all numbers" % image_url
    else:
      for number in numbers:
        send_text_message(to_phone_number=number, message_body=message_body)
      print "\"%s\" sent to all numbers" % message_body

def main():
  global TWILIO_ACCOUNT_SID
  global TWILIO_AUTH_TOKEN

  if not os.path.isfile('secrets'):
    print "Please create a plain-text file called `secrets` containing the Twilio Account SID on the first line and the Twilio Auth Token on the second line."
    sys.exit(-1)

  with open('secrets') as f:
    TWILIO_ACCOUNT_SID = f.readline().strip()
    TWILIO_AUTH_TOKEN = f.readline().strip()

  if len(sys.argv) == 1:
    run_server_mode()
  elif len(sys.argv) == 2:
    run_interactive_mode()
  else:
    print "Usage: %s [filename.csv]"  % sys.argv[0]
    print "Run without any arguments to run as a web app"
    print "Specify the name of a numbers CSV file as the first argument to run in command-line mode"
    sys.exit(-1)

if __name__ == '__main__':
  main()
