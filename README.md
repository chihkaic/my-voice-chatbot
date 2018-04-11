# Start building for voice with Alexa
Start building for Alexa with this quick walkthrough of the skill-building process.

## Step 1: Sign in to Amazon Web Services (AWS) and create a function

### Requirements:
* Python 3.6
* pip install python-twitter
* Register as a developer on twitter and register an application using https://apps.twitter.com/ to get access to developer credentials

### Steps
* 1: Log in to the AWS Management Console. If you haven’t done so already, you’ll need to create a free account.
* 2: From the list of services, select Lambda.
* 3: Click the region drop-down in the upper-right corner of the console and select US East (N. Virginia), which is a supported region for Lambda functions used with the Alexa Skills Kit.
* 4: Choose Create a Lambda Function and select Autor from scratch.

```bash
Name: We’ll use myLTDFSkill for this walkthrough.
Runtime: Select Python 3.6. 
```

* 5: Make sure the trigger is set to Alexa Skills Kit.
* 6: Upload voice_handlers.py to the lambda function code. 
* 7: Copy the Amazon Resource Name (ARN) displayed in the upper-right corner of the console that starts with arn:aws:lambda....

### voice_handlers.py
Amend consumer_key, consumer_secret, access_token_key and access_token_secret in voice_handlers.py:

```bash
consumer_key = '<INSERT_TWITTER_CONSUMER_KEY_HERE>',
consumer_secret = '<INSERT_TWITTER_CONSUMER_SECRET_HERE>', 
access_token_key= '<INSERT_TWITTER_ACCESS_TOKEN_KEY_HERE>',
access_token_secret= '<INSERT_TWITTER_ACCESS_TOKEN_SECRET_HERE>'
```

## Step 2: Use the Amazon developer portal to configure your skill

### Steps
* 1: Sign in to the Amazon developer portal. If you haven’t done so already, you’ll need to create a free account.
* 2: From the top navigation bar, select You Alexa Console > Skills.
* 3: Choose Create Skill.
* 4: Name your skill. This is the name displayed to users in the Alexa app.
* 5: Select Custom model.
* 6: Create an invocation name. This is the word or phrase that users will speak to activate the skill. For this walkthrough, we’ll use the skill name ltdf challenge. Users will say, "Alexa, open ltdf challenge" to interact with your skill.
* 7: In the Json Editor box, drag and drop intent_schema.json.
* 8: Select the Endpoint AWS Lambda ARN then paste your ARN code from previous step. 
* 9: Choose Build Model and wait until the interaction model finishes loading, in no more than a few seconds.

### intent_schema.json
```bash
{
    "interactionModel": {
        "languageModel": {
            "invocationName": "ltdf challenge",
            "intents": [
                {
                    "name": "AMAZON.CancelIntent",
                    "samples": []
                },
                {
                    "name": "AMAZON.HelpIntent",
                    "samples": []
                },
                {
                    "name": "AMAZON.StopIntent",
                    "samples": []
                },
                {
                    "name": "WhatsAGeneralRanking",
                    "slots": [],
                    "samples": [
                        "what general ranking is",
                        "what is a general ranking",
                        "What's a general ranking"
                    ]
                },
                {
                    "name": "PostAGeneralRanking",
                    "slots": [],
                    "samples": [
                        "publish a general ranking to my tweet"
                    ]
                },
                {
                    "name": "ShowStageIntro",
                    "slots": [],
                    "samples": [
                        "Show me the introduction of this stage"
                    ]
                }
            ],
            "types": []
        }
    }
}
```

## Step 3: Test your skill
Use the Service Simulator from the Test step of LTDF Challenge development. 

# Machine Learning
* The section is to run through the idea of making better use of social media integrating with crowdsourcing and supervise machine learning technology to collect and generate a bunch of different utterances in natural language for intent schema. 
* Certain playbook has been reused from what AWS has developed in https://github.com/aws-samples/machine-learning-samples/tree/master/social-media.

## Requirements
* Python 3.6
* pip install ndg-httpsclient pyasn1 pyopenssl python-twitter unicodecsv
* pip install boto

## Step 1: Gathering training data
Run the following command to gather the training data:
```bash
python gather-data.py @letour
```
This will produce a file called line_separated_tweets_json.txt that other scripts will read later.

### gather-data.py
Amend consumer_key, consumer_secret, access_token_key and access_token_secret in gather-data.py:

```bash
consumer_key = '<INSERT_TWITTER_CONSUMER_KEY_HERE>',
consumer_secret = '<INSERT_TWITTER_CONSUMER_SECRET_HERE>', 
access_token_key= '<INSERT_TWITTER_ACCESS_TOKEN_KEY_HERE>',
access_token_secret= '<INSERT_TWITTER_ACCESS_TOKEN_SECRET_HERE>'
```

## Step 2: Label training data with Mechanical Turk
In this application, we will build an ML model that mimics the behavior or opinions of humans. Building a good model requires lots of examples of the choices that humans would make. Doing this yourself is always an option, but often too slow or expensive to be practical. In supervised machine learning, these opinions are called the labels, or the target of the model.

Amazon Mechanical Turk (Mturk) is a way to quickly and economically label large quantities of data. This section will walk through that process.

### Step 2a: Label training data with Mechanical Turk
The first step is to take the raw JSON data that we have received from the Twitter API and convert it to a CSV format that Mechanical Turk can use. Do this by running:

```bash
python build-mturk-csv.py
```
This will consume the line_separated_tweets_json.txt file and output a file called mturk_unlabeled_dataset.csv.

### Step 2b: Submit the job to MTurk
Use the Mechanical Turk Console to create a set of Human Intelligence Tasks (HITs) to assign labels to these tweets. Turkers will be asked to pick which label best applies to the tweet for a designed intent:

* CUSTOM_INTENT_A

Detailed steps for generating training labels using MTurk
* 1. Create an account with Mechanical Turk
* 2. Start a new project
* 3. Select Other from the options and click Create Project
* 4. Enter properties on next page

```bash
Project Name: Labeling of tweets
Title: Categorize the tweet
Description: Categorize the tweet into the selected Alexa Intent category.
Keywords: tweet, tweets, categorization, labeling, sentiment
Checkbox for adult content: Select as checked because content may contain offensive tweets. See details
Rewards per assignment: Higher values can fetch faster results.
Number of assignments per HIT: 3
Time allotted per assignment: 2
HIT expires in: 7 days
Auto-approve and pay Workers in: 2 Hours
```

* 1. Amend the contents of mturk-project-template.xml based on your Alexa intent design. 
* 2. On the page for design layout, click the Source button and cut paste contents from mturk-project-template.xml. You may preview and edit as deemed fit. Parameter value ${tweet} and checkbox values should be left unmodified as the later steps depend on them.
* 3. Preview and finish. This creates the Project template.
* 4. Goto Create New Batch with an Existing Project
* 5. Select Publish Batch for the project you just created.
* 6. Follow instructions on the following screen. You will be using the csv file produced by build-mturk-csv.py as part of them.
* 7. Preview the HITs and submit the batch for labeling. This step will cost you money.

### Step 2c: Processing the output from MTurk
Once all of your Turk HITs are complete, download the results into a file called mturk_labeled_dataset.csv. Then run the script to convert the 3 HIT responses for each tweet into a single dataset with a binary attribute.

```bash
python build-aml-training-dataset.py
```

## Step 3: Create the ML Model
This step creates a machine learning model that performs binary classification. Requires input dataset and corresponding scheme generated from step 2. The ML model splits the dataset into two pieces, 70% of the dataset is used for training and 30% of the dataset is used for evaluation.

### Step 3a: Upload dataset to S3
* 1: Log in to the AWS Management Console. If you haven’t done so already, you’ll need to create a free account.
* 2: From the list of services, select S3.
* 3: Create a new bucket then upload aml_training_dataset.csv and aml_training_dataset.csv.schema to the bucket.
* 4: Amend the CORS configuration as below setting:

```bash
<!-- Sample policy -->
<CORSConfiguration>
	<CORSRule>
		<AllowedOrigin>*</AllowedOrigin>
		<AllowedMethod>GET</AllowedMethod>
		<MaxAgeSeconds>3000</MaxAgeSeconds>
		<AllowedHeader>Authorization</AllowedHeader>
	</CORSRule>
</CORSConfiguration>
```

### Step 3b: Create the ML Model
* 1: Log in to the AWS Management Console.
* 2: From the list of services, select Machine Learning.
* 3: Choose Create new Datasource and ML Model.
* 4: For S3 Location, type the full location of the aml_training_dataset.csv file.
* 5: For Datasource name, type ds_tweets.
* 6: Choose Verify then click Continue.
* 7: On the Schema page, click Continue.
* 8: On the Target page, click Continue.
* 9: On the Row ID page, click Review.
* 10: On the Review page, click Coninue.
* 11: On the ML model settings page, click Review.
* 12: On the Review page, click Create ML Model.
* 13: Wait for the evaluation to complete before proceeding.

### Step 3c: Review the ML Model's Predictive Performance and Set a Score Threshold
Fine-tune your ML model performance metrics by adjusting the score threshold. 

## Step 4: Use the ML Model to Generate Batch Predictions

### Step 4a: To generate batch predictions
* 1: Choose Amazon Machine Learning, and then choose Batch Predictions.
* 2: Choose Create new batch prediction.
* 3: On the ML model for batch predictions page, choose ML model you created.
* 4: For Locate the input data, choose My data is in S3, and I need to create a datasource.
* 5: For S3 Location, type the full location of the aml_training_dataset.csv file.
* 6: For Does the first line in your CSV contain the column names?, choose Yes.
* 7: Choose Verify.
* 8: Choose Continue.
* 9: For S3 destination, type the name of the Amazon S3 location where you uploaded the files in Step 1: Prepare Your Data. Amazon ML uploads the prediction results there.
* 10: For Batch prediction name, accept the default.
* 11: Choose Review.
* 12: On the Review page, choose Finish.

### Step 4b: To view the predictions
* 1: To view the results of the batch pre11diction, navigate to the Amazon S3 location referenced in the Output S3 URL field. From there, navigate to the results folder.
* 2: Download the prediction file to your desktop, uncompress it, and open it.
* 3: The file has two columns, bestAnswer and score, and a row for each observation in your datasource.
* 4: The tweets with bestAnswer is 1 indicate that these tweets are likely able to be used as the utterances for this intent.
* 5: Update the intent schema based on the prediction reuslts.

