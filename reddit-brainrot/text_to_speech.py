import boto3
#https://aws.amazon.com/polly/
polly = boto3.client('polly', region_name='us-east-1')
response = polly.synthesize_speech(
    Text='Hello from Polly',
    OutputFormat='mp3',
    VoiceId='Matthew'
)

with open('output.mp3', 'wb') as f:
    f.write(response['AudioStream'].read())
