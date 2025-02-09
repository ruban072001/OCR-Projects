#!/usr/bin/env python
import sys
import warnings
# import streamlit as st
from crew import OcrCrew
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
            'path': r"C:\Users\KIRUBA\Desktop\vision related task\images\table.png",
            'language': 'en'
        }
    result = OcrCrew().crew().kickoff(inputs=inputs)
    print(result)

if __name__ == "__main__":
    run()