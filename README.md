# Daily-NewsLetter-Subscription
Project Description
Table of Contents
How to Install and Run the Project
How to Use the Project
Include Credits

Project Name
ETL Pipeline for Collecting News Data from Google and Uploading to S3
Overview
This project sets up an ETL (Extract, Transform, Load) pipeline to collect news data from Google and upload it to an S3 bucket. The pipeline is automated using Airflow, and a Lambda function is included to send an email to the user whenever new data is put into the S3 bucket.
Architecture
The architecture of the project consists of the following components:
Google News API: A source of news data that provides the latest headlines from various sources around the world.
Airflow: An open-source platform used for scheduling, monitoring, and managing workflows.
AWS S3: A cloud-based object storage service used to store the news data.
AWS Lambda: A serverless computing service that executes code in response to events, in this case, the addition of new data to the S3 bucket.
AWS SES: A cloud-based email service used to send email notifications to the user.
Setup
Set up an AWS S3 bucket: Create an S3 bucket to store the news data.
Set up an AWS IAM role: Create an IAM role with the necessary permissions to access S3 and SES.
Set up an AWS Lambda function: Create a Lambda function that will send an email using SES whenever new data is put into the S3 bucket.
Set up an Airflow DAG: Create an Airflow DAG (Directed Acyclic Graph) to schedule the ETL pipeline workflow.
Run the ETL pipeline: Run the Airflow DAG to start the ETL pipeline, which will collect news data from the Google News API, transform it, and upload it to the S3 bucket.
Receive email notifications: Whenever new data is added to the S3 bucket, the Lambda function will automatically invoke SES to send an email notification to the user.
Prerequisites
Python 3.6 or higher
AWS account
Airflow 1.10.12 or higher
Installation
Clone this repository to your local machine.
Install the required Python packages using pip install -r requirements.txt.
Run app.py to check if news data is successfully uploaded into the s3 bucket.
Create a Lambda Function with a new role that has required access to s3 and ses.
Add a trigger which will invoke the lambda function whenever  a PUT operation occurs in s3.
Add a layer to the lambda function that has pandas.
Add the lambda code from lambda.py .
Navigate to  Amazon SES and create identity(An identity is the email address that sends or receives an email using this service.)
Once the identities are created and verified. Get the arn of that identity and edit source and destination email and source arn into the lambda function code block.
Now run app.py. If everything runs fine, the app.py should upload news data to s3 and this should trigger the lambda function to invoke the ses to send an email.
Now lets schedule this workflow using Airflow.
Then create an ec2 instance( preferably Ubuntu  and size: T3.medium).
SSH into the instance and install python and the required packages.
Install apache-airflow and start airflow using >> airflow standalone 
for development server.
Navigate to airflow folder on the root directory. Create a dag folder and also edit the name of the dag folder in airflow.cfg
<img>
Add app.py, dag file and any other required files that is used in app.py
Login to airflow which is hosted on public dns of the ec2 instance.
Search your dag and run it.


Verify in S3 that you have received the news data.
Also you must have received an email that delivers the news.
Conclusion
This project demonstrates how to set up an automated ETL pipeline to collect news data from Google and upload it to an S3 bucket. By using Airflow to schedule the pipeline and AWS Lambda to send email notifications, the workflow can be fully automated and require minimal manual intervention.





<img height="180em" src="https://github-readme-stats.vercel.app/api?username=eminent02&show_icons=true&hide_border=true&&count_private=true&include_all_commits=true" />
<img height="300em" src="https://github-readme-stats.vercel.app/api/top-langs/?username=eminent02&langs_count=5&theme=tokyonight" />
