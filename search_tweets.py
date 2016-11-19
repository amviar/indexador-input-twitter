#!/usr/bin/python
# coding=utf-8

import argparse
import logging
import twitter
import requests
import json


def configureArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--outputWidth', help='Output with for images to display in windows.',
                        type=int, default="500")
    parser.add_argument('--log', help="Log level for logging.", default="WARNING")

    return parser.parse_args()



def configureLogging(loglevel, logFile=None):
    numeric_level = getattr(logging, loglevel.upper(), None)

    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)

    if logFile is not None:
        logging.basicConfig(level=numeric_level, filename=logFile, format='%(levelname)s:%(funcName)s:%(message)s')
    else:
        logging.basicConfig(level=numeric_level, format='%(levelname)s:%(funcName)s:%(message)s')




def main():
    args = configureArguments()
    configureLogging(args.log)
    logging.info('Search tweets job started.')

    api = twitter.Api(consumer_key='EjWqy7KAOHaoXdcvAdRZDiiYV', consumer_secret='Yk0zoXpT4pka3tpgGjk6CUJ8I6ncsYLXb9yYje4FJXIN3ZavyB',
        access_token_key='1875731528-jbZ6v551n2cpQh489qdbSaTsMLUnn9k7ZeIV98W', access_token_secret='AXpNzqwFb45ut1prT70H00fK4k2CE9zCC9thZ1uXthxKC')


    results = api.GetSearch(raw_query="q=violencia%20institucional&result_type=recent&since=2014-07-19&count=100")

    for tweet in results:
        expandedURL = ''

        if tweet.urls:
            expandedURL = tweet.urls[0].expanded_url

        data = {
            'title': 'Tweet',
            'body': tweet.text,
            'url': expandedURL,
            'source': 'Twitter',
            'creator': tweet.user.screen_name,
            'published_at': tweet.created_at
        }
        tweet_json = json.dumps(data)
        headers = {'Content-type': 'application/json'}

        logging.info(tweet_json)
        
        response = requests.post('http://138.197.22.110:3000/api/v1/contents', data=tweet_json, headers=headers)
        
        logging.info(response)

    logging.info('Search tweets job finished.')    
# end main

if __name__ == '__main__':
    main()