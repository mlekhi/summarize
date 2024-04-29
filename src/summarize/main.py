from config import Config
from llm import LLM_review, LLM_summarize

import sys
import os
import argparse
import json

config_manager = Config()

def main():
    config = config_manager.load()

    parser = argparse.ArgumentParser(
        description='This is a command-line tool to summarize repositories of code using OpenAI.',
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        '--version', 
        action='version', 
        version='%(prog)s 0.4.6'  # Add your version here
    )

    parser.add_argument(
        '--llm',
        type=str,
        choices=['azure', 'groq', 'openai', 'togetherai'],
        help='Select the large language model to use. Default is OpenAI. All other models and are intended for developer use and require API keys.'
    )

    parser.add_argument(
        'path',
        nargs='?',
        help='Path to folder/repository to summarize.'
    )

    args = parser.parse_args()

    # If no arguments were passed, print the help message and exit
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    try:
        llm = config['llm']
    except:
        config['llm'] = 'openai'
        config_manager.save(config)


    if args.llm:
        config['llm'] = args.llm.lower()
        config_manager.save(config)
        print(f"Using ", config['llm'])
        exit()

    # define functions to process data
    path = args.path
    important_files = LLM_review(path)
    LLM_summarize(important_files, config['llm'])        

if __name__ == '__main__':
    main()