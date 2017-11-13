Xero & Phaxio API Integration Sample Project
----

See the blog post for more indepth details: https://medium.com/p/a954b62c0407

Project is intended to be deployed to AWS Lambda with an API Gateway.  The API Gateway exposes an endpoint that can be called by the Chrome Extension.  The [Chrome Extension](https://github.com/rjaus/XeroPhaxioExtension) is available in a separate repo.

## Try it for yourself (setup instructions)
1. Clone this repo
2. Create Xero API [Private App](https://developer.xero.com/documentation/auth-and-limits/private-applications) and put the consumer key + secret into the config.yml file. Rename your privatekey.pem file to 'lambdaprivatekey.pem' and put it in a folder called 'keys', within the repo. https://app.xero.com/Application/
4. Create [Phaxio account](https://www.phaxio.com/), and put your consumer key + secrets into the config.yml file.
5. Create an AWS Account, create a User under this account with an access key + secret, and put them in config.yml.
6. Locally, create a python virtual environment and install python-lambda.
7. Deploy your Lambda function `lambda deploy`
8. You can now invoke your lambda function via the AWS Lambda console, or the unique url each lambda generates.

You could use the chrome extension create here to call your lambda function from the browser: https://github.com/rjaus/XeroPhaxioExtension


For more information, tweet [@xeroapi](twitter.com/XeroAPI)

Copyright (c) 2017 Riley James

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.