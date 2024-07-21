#!/usr/bin/env python
from finagent.crew import finagent
from dotenv import load_dotenv
load_dotenv()

def run():
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    inputs = {
        'topic': '¿Es cierto que los congresistas no tienen que estudiar leyes?'
    }
    finagent().crew().kickoff(inputs=inputs)