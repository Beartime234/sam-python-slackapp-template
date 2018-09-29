# sam-python-slackapp-template

This repository is an a simple template to create a ready working slack events
api using serverless application model and hosted on AWS. Clone the repository and follow
the setup process detailed below. The basic template slack API will create a an events
api that will respond with the reversed text of the message sent to the event. It also
correctly responds to the slack challenge. It will also verify slack requests if it is
a prod deployment/stage.

This is based of the sam cli init template.

The application when deployed will allow you to configure a slack bot
that will return what the user says reversed.

```bash
.
├── Pipfile                     <-- Pipfile
├── Pipfile.lock                <-- Pipfile.lock
├── README.md                   <-- This instructions file
├── src                         <-- Source code for a lambda function
│   ├── __init__.py
│   ├── version.py              <-- Holds version of your code/template
│   └── app.py                   <-- Lambda function code
│   └── helpers.py              <-- Lambda function code
├── requirements.txt            <-- Python dependencies
├── templates
│       ├── template.yml        <-- SAM template
        ├── variables.json      <-- Variables for sam local testing
└── tests                       <-- Unit tests
    └── unit
        ├── __init__.py
        └── test_handler.py     <-- Slack challenge test
└── scripts                     <-- Hosts scripts
    └── build.sh                <-- Builds application
    └── test.sh                 <-- Runs tests
    └── deploy.sh               <-- Deploys application to aws
    └── sam-local.sh            <-- Runs the applicaiton locally

```

## Requirements

* AWS CLI already configured with at least PowerUser permission
* [Python 3.6+ installed](https://www.python.org/downloads/)
* [Docker installed](https://www.docker.com/community-edition)
* [Python Virtual Environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/)
* [An Aws Account](https://portal.aws.amazon.com/billing/signup)

> **See [Serverless Application Model (SAM) HOWTO Guide](https://github.com/awslabs/serverless-application-model/blob/master/HOWTO.md) for more details on SAM.**

### AWS Requirements

When you deploy the slack app it assumes that you have 2 things.

1. An S3 bucket that you can store lambda code in
2. A secrets manager secret that you can store Slack API secrets

#### S3 Bucket

You will need to set up a simple S3 bucket that sam can use to upload
your code to S3 so it can be imported and used in lambda. Make sure when
you are replacing variables in the script that your profile has the ability
to upload to S3.

#### Secrets Manager

For the slack app we need to store 2 secrets in one secret in AWS Secrets
manager.

1. Your signing secret
2. Your bot token so that your bot can accept requests.

Your secret will look like the following.

```json
{
  "BOT_TOKEN": "REPLACE_WITH_YOUR_BOT_TOKEN",
  "SIGNING_SECRET": "REPLACE_WITH_YOUR_SIGNING_SECRET"
}
```

The application will use these secrets to perform checks to verify requests
and send messages.

## Setup process

**NOTE:** When you run scripts it should be run from the root directory e.g. ./scripts/scriptname.sh
**NOTE:** Before running the scripts change variables in the scripts

### Installing dependencies

[AWS Lambda requires a flat folder](https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html) with the application as well as its dependencies. Therefore, we need to have a 2 step process in order to enable local testing as well as packaging/deployment later on.

```bash
pipenv install
```

I have simplified the build process you can run it with the following

```bash
./scripts/build.sh
```

### Local development

**Invoking function locally through local API Gateway**

```bash
./scripts/sam-local.sh
```

If the previous command ran successfully you should now be able to hit the following local endpoint to invoke your function `http://localhost:3000/`

## Packaging

AWS Lambda Python runtime requires a flat folder with all dependencies including the application. SAM will use `CodeUri` property to know where to look up for both application and dependencies:

```yaml
...
    ApiLambdaFunction:
        Type: AWS::Serverless::Function
        Properties:
            CodeUri: ../src/build/
            ...
```

You can package the application using the following command.

```bash
./scripts/build.sh
```

## Deployment

You can deploy your application using the following script

```bash
./scripts/deploy.sh dev/test/prod
```

The argument for this script should be dev/test/prod depending on what
stage you are deploying too.

After deployment is complete stack outputs will be printed. You can grab the one labeled SlackApiUrl and put that into
your slack bots event URL.

## Testing

We use **Pytest** for testing our code and you can install it using pip: ``pipenv install --dev``

You can run one of the scripts in the scripts folder to run your tests.

```bash
./scripts/test.sh
```

## Uses

* [Python Slack Client](https://github.com/slackapi/python-slackclient)

## Todo

- Change the automation to be built with ansible. Not hard im just lazy.
- Fix the shell scripts to be work not from root directory
- Write some documentation around deploying to code pipeline.
- Fix that issue that causes the bot to reply twice. Needs to send a response quicker.
