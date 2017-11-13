# -*- coding: utf-8 -*-
import os
from phaxio import PhaxioApi
from xero import Xero
from xero.auth import PrivateCredentials

# Setup the Xero Private App
# Ensure your private key is listed in your .gitignore, so you doesn't end up in your repo.
# Xero API Consumer Key is retrieved via an environmental variable
# Ensure you add the environment variable on your local machine AND in your AWS Lambda Settings (via config.yaml)
with open('./keys/lambdaprivatekey.pem') as keyfile:
	rsa_key = keyfile.read()
credentials = PrivateCredentials(os.getenv("XERO_CONSUMER_KEY_PHAXIO"), rsa_key)
xero = Xero(credentials)

# Setup PhaxioAPI
# Phaxio API keys are set via environment variables
# Ensure you add the environment variables on your local machine AND in your AWS Lambda Settings (via config.yaml)
phaxio = PhaxioApi(os.getenv('PHAXIO_API_KEY'), os.getenv('PHAXIO_API_SECRET'))

fax_number = None

def handler(event, context):

	# invoice_id is the only param sent to the lambda function
	invoice_id = event.get('invoice_id')

	# Use the invoice_id to retrieve the invoice details from the Xero API
	invoice = xero.invoices.get(invoice_id)

	# Included in the invoice response is the Contact and their Fax Number, lets parse it out.
	for phone in invoice[0]['Contact']['Phones']:
		if phone['PhoneType'] == "FAX":
			# Check to see if the fax number is complete, if not, return an error
			if not all((phone['PhoneCountryCode'], phone['PhoneAreaCode'], phone['PhoneNumber'])):
				return { "statusCode": 400,  "headers": { "Content-Type": "application/json", "Access-Control-Allow-Origin" : "*", "Access-Control-Allow-Credentials" : True }, "body": 'Contact does not have a Fax Number, add Fax Number to Contact in Xero and try again.'}
			else:
				fax_number = phone['PhoneCountryCode']+phone['PhoneAreaCode']+phone['PhoneNumber']

	# Sanity check, did the contact have a fax number? If not, return with relevant error.
	if fax_number == None:
		return { "statusCode": 400,  "headers": { "Content-Type": "application/json", "Access-Control-Allow-Origin" : "*", "Access-Control-Allow-Credentials" : True }, "body": 'Contact does not have a Fax Number, add Fax Number to Contact in Xero and try again.'}

	# Now lets prepare to send a fax with Phaxio
	# Frist, retrieve the PDF version of the invoice from the Xero API
	invoice_pdf = xero.invoices.get(invoice_id, headers={'Accept': 'application/pdf'})

	# Save the PDF retrieved to disk temporarily.  This is probably unnecessary, but I'm a Python Noob.
	pdf_file = open('/tmp/tmp_fax.pdf', 'wb')
	pdf_file.write(invoice_pdf)
	pdf_file.close()

	# Send the PDF invoice as a fax with Phaxio
	response = phaxio.Fax.send(fax_number, files='/tmp/tmp_fax.pdf', header_text='Xero Invoice Faxed with Phaxio', tags_dict={'invoice_id': invoice_id})

	# Upload a confirmation of the Fax Receipt
	# As the Fax is not sent immediately, this needs to be done via a second Lambda function, invoked via the callback url.
	# Skipping this feature for now.
	# Mark the invoice as sent
	invoice[0]['SentToContact'] = True
	xero.invoices.save(invoice[0])


	# Return with a status code 200, adding the relevant CORS headers to handle cross domain scripting.
	return {
		"statusCode": 200,
		"headers": {
			"Content-Type": "application/json",
			"Access-Control-Allow-Origin" : "*",
			"Access-Control-Allow-Credentials" : True
		},
		"body": 'Fax Sent Successfully'
	}
