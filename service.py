# -*- coding: utf-8 -*-
import os
from phaxio import PhaxioApi
from xero import Xero
from xero.auth import PrivateCredentials

# Setup Xero Private App
with open('./keys/lambdaprivatekey.pem') as keyfile:
	rsa_key = keyfile.read()
credentials = PrivateCredentials(os.getenv("XERO_CONSUMER_KEY_PHAXIO"), rsa_key)
xero = Xero(credentials)

# Setup PhaxioAPI
phaxio = PhaxioApi(os.getenv('PHAXIO_API_KEY'), os.getenv('PHAXIO_API_SECRET'))

fax_number = None

def handler(event, context):

	invoice_id = event.get('invoice_id')

	# find the invoice
	invoice = xero.invoices.get(invoice_id)

	# get the fax number
	for phone in invoice[0]['Contact']['Phones']:
		if phone['PhoneType'] == "FAX":
			# Check to see if the fax number is complete, if not, return an error
			if not all((phone['PhoneCountryCode'], phone['PhoneAreaCode'], phone['PhoneNumber'])):
				return { "statusCode": 400,  "headers": { "Content-Type": "application/json", "Access-Control-Allow-Origin" : "*", "Access-Control-Allow-Credentials" : true }, "body": 'Contact does not have a Fax Number, add Fax Number to Contact in Xero and try again.'}
			else:
				fax_number = phone['PhoneCountryCode']+phone['PhoneAreaCode']+phone['PhoneNumber']

	# didn't find any fax number, return an error
	if fax_number == None:
		return { "statusCode": 400,  "headers": { "Content-Type": "application/json", "Access-Control-Allow-Origin" : "*", "Access-Control-Allow-Credentials" : true }, "body": 'Contact does not have a Fax Number, add Fax Number to Contact in Xero and try again.'}

	# get the invoice pdf
	invoice_pdf = xero.invoices.get(invoice_number, headers={'Accept': 'application/pdf'})

	pdf_file = open('tmp/tmp_fax.pdf', 'wb')
	pdf_file.write(invoice_pdf)
	pdf_file.close()

	# fax the pdf
	response = phaxio.Fax.send(fax_number, files='tmp/tmp_fax.pdf')

	# upload a fax receipt (attach to invoice)
		

	return {
		"statusCode": 200,
		"headers": {
			"Content-Type": "application/json",
			"Access-Control-Allow-Origin" : "*",
			"Access-Control-Allow-Credentials" : true
		},
		"body": 'Fax Sent Successfully'
	}
