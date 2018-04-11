"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.

"""

from __future__ import print_function
import twitter

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output,
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_speechlet_withimage_response(title, output, imageURL, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Standard',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output,
            'image': {
            'smallImageUrl': imageURL,
            'largeImageUrl': imageURL
             }
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_speechlet_accountlinking_response(should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': 'Please go to your Alexa app and link your account.'
        },
        'card': {
            'type': 'LinkAccount'
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"

    speech_output = "Welcome to the Le Tour de France 2018 demo. " \
                    "Please tell me what you would like to know by saying, " \
                    "What is a general ranking"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me what you would like to know by saying, " \
                    "What is a general ranking"
    should_end_session = False

    #return build_response(session_attributes, build_speechlet_accountlinking_response(should_end_session))
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Alexa Skills Kit sample. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def get_general_ranking():
    """ Query database """

    session_attributes = {}
    card_title = "General Ranking"
    speech_output = "A general ranking is Geraint Thomas, 00:16:04 +00:00:00 " \
                    "Stefan Kueng, 00:16:09 +00:00:05 " \
                    "Vasili Kiryienka, 00:16:09 +00:00:07"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = None
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def set_stage_intro():
    session_attributes = {}
    card_title = "Stage Intro"
    speech_output = "Show stage intro"
    image_url = "https://s3.amazonaws.com/ltdf/stage_intro.jpg"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = None
    should_end_session = False
    return build_response(session_attributes, build_speechlet_withimage_response(
        card_title, speech_output, image_url, reprompt_text, should_end_session))


def set_tweet():
    session_attributes = {}
    card_title = "General Ranking"
    tweet_output = "A general ranking is Geraint Thomas, 00:16:04 +00:00:00 Stefan Kueng, 00:16:09 +00:00:05 Vasili Kiryienka, 00:16:09 +00:00:07"
    speech_output = "Tweet a general ranking"
    api = twitter.Api(consumer_key= '<INSERT_TWITTER_CONSUMER_KEY_HERE>',
                      consumer_secret= '<INSERT_TWITTER_CONSUMER_SECRET_HERE>',
                      access_token_key= '<INSERT_TWITTER_ACCESS_TOKEN_KEY_HERE>',
                      access_token_secret= '<INSERT_TWITTER_ACCESS_TOKEN_SECRET_HERE>')
    #tweet_image = "https://s3.amazonaws.com/ltdf/general_ranking.jpg"
    api.PostUpdate("A general ranking is Geraint Thomas, 00:16:04 +00:00:00 Stefan Kueng, 00:16:09 +00:00:05 Vasili Kiryienka, 00:16:09 +00:00:07")
    reprompt_text = None
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "WhatsAGeneralRanking":
        return get_general_ranking()
    elif intent_name == "PostAGeneralRanking":
        return set_tweet()
    elif intent_name == "ShowStageIntro":
        return set_stage_intro()
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])
    try:
        access_token = event['context']['System']['user']['accessToken']
    except:
        access_token = None

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
