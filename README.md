# Is my lambda deprecated?

Most people uses lambda functions. Recently AWS announced that functions currently using Node JS 8.10 will not be supported after December 31, 2019.

So we have created this project which checks if there are lambdas needing update.

# Configuration

Generate an AWS access key, with following permission and create a local profile to run this code.

    AWSLambdaReadOnlyAccess
    AmazonEC2ReadOnlyAccess

# Running the verification

Set environment variable to select your local profile:

    Windows: set AWS_PROFILE=<your-local-profile>
    Linux: export AWS_PROFILE=<your-local-profile>

Run the code to check if some action is needed:

    python lambda_check.py