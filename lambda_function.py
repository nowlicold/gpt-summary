import json
import logging
import os
from langchain import OpenAI
from llama_index import LLMPredictor, GPTSimpleVectorIndex, SimpleWebPageReader

os.environ['OPENAI_API_KEY'] = "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"
logger = logging.getLogger()


# logger.addHandler(logging.StreamHandler(stream=sys.stdout))

def read_web_page(url):
    docs = SimpleWebPageReader().load_data([url])
    return docs


def build_index(docs, index_path):
    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="gpt-3.5-turbo"))
    # 按最大token数500来把原文档切分为多个小的chunk，每个chunk转为向量，并构建索引
    index = GPTSimpleVectorIndex(docs, chunk_size_limit=500, llm_predictor=llm_predictor)
    # 保存索引
    index.save_to_disk(index_path)


def query_index(index_path, query_str):
    # 加载索引
    new_index = GPTSimpleVectorIndex.load_from_disk(index_path)
    # 查询索引
    response = new_index.query(query_str)
    # 打印答案
    logger.info("response: " + response.response)
    return response


def lambda_handler(event, context):
    url = event['body']['url']
    text_id = event['body']['text_id']
    query_str = event['body']['query_str']
    logger.info("received from request body " + json.dumps(event['body']))

    logger.info("to read web page from " + url)
    docs = read_web_page(url)

    logger.info("to build index into " + text_id)
    build_index(docs, text_id)

    logger.info("to query index by " + query_str)
    resp = query_index(text_id, query_str)

    return {
        'statusCode': 200,
        'body': json.dumps(resp.response)
    }


if __name__ == '__main__':
    event = json.loads('''
    {
    "body": {
        "url": "https://dev-felo-meet.s3.ap-northeast-1.amazonaws.com/summary/04e64295e86070cfbba13d2c4ff1deb9/text085e970f0a5720ab99f8618fd625d63d?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjECoaDmFwLW5vcnRoZWFzdC0xIkYwRAIgPIOEt4pzTNHHxStSL2rfZqhOfjPjtWzBJ0IpSYuLBjcCIH%2BTtRZKAfcECayiw4n3pjWrOp%2FP6rKvScQTKJQJaW5cKu0CCOP%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQARoMOTIxMDIwMDMyNTkxIgwxdovSD7UQAKCV83YqwQLGvWN6e0%2FtDq%2FAT6tHXM1Xewhy25L5hEYghF%2Bz2NNE3gpbUqf1n4aUpwTEpzkSQd%2F2Xt3SyqvUtZoqOxJLis%2FEVlhPScZ2D6iy8%2Fh9%2B4KtDGn8lvVOZ5FEizA4Ux45oSyO1hXn3y4SsFKsDgKCb04qhEOCQVs5br%2FJWWHtOQtC%2FZR5jrnzwqyQqMJ0%2BnCwySUF1IjdqRusjyEnDrzvE1RpPTshrvoWDcxTYuo6Fn96wRsWNmMHpKFIR6SK42%2FURqQwJb3hy%2BlWUi8KLGjvdhhZ2xIX6dcYGNW9qckSM29UYQY%2B3TCLYVdgJSFJHOu8CNst%2BE3Ju4F8QgT66ddpHqwRGCkkcjqTFv9Ptcbve%2FcHdu1LzWe1dT7qd85rFc1%2BjXHtUexXx3jNgtybFzR0VHs8nrMqLLQAnxtWEAkAkdkBZs8wmcvEoAY6tAKDOC14ow8isiuZSKlNVg5gWPvw8k9m%2FGDb7ubnr5ajaWgDhM%2FZjSLFFO7qIp2hshrrF6e%2F%2FixyNftz85RIJvaJ7Yyl9GICTkBToBDavERbQI%2Bc1%2BYW1eRmfVtgoM5TbtICaZKUy%2BiXiRHPV2hneyC1jL87Lz1h4W%2F0jcJC0uFhWREDZ1rfruO55DVyf3VBgKMXXpRfVr1ydARVIfKun70xJ8GaZv1OGkhgi0x81uDDLqngEAnDnC%2FABxbdq790exkLXQ9lHDDX2ckgBQSmsvGzEuY5RKwPaPNu%2Fv2CgB1hOQMr91y3nykkoGhy15LQOLGc5m93C%2BqNhjCSUaoS%2B5oerOEKsDlhOaP4u6VwiQgKJq4QUpJPXzvhJ0ziGDi5A8aN4o6iCuwDTvBKS%2BXZ7oCzT2Irxg%3D%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20230315T033731Z&X-Amz-SignedHeaders=host&X-Amz-Expires=43200&X-Amz-Credential=ASIA5M4ISMZHV3SZSFBY%2F20230315%2Fap-northeast-1%2Fs3%2Faws4_request&X-Amz-Signature=94786d9af61a6f352133ae7893c53199944bfea03ecb62c361f0cab8486424a5",
        "text_id": "text_id_2023_3_14",
        "query_str": "I need you to output the meeting summary follow my format:\\n【Summary】\\n- Summary by points\\n- Another point\\n【Action Items】\\n- content, Assignee: content, Deadline: content.\\n- content, Assignee: content, Deadline: content."
    },
    "resource": "/{proxy+}",
    "path": "/path/to/resource",
    "httpMethod": "POST",
    "isBase64Encoded": true,
    "queryStringParameters": {
        "foo": "bar"
    },
    "multiValueQueryStringParameters": {
        "foo": [
            "bar"
        ]
    },
    "pathParameters": {
        "proxy": "/path/to/resource"
    },
    "stageVariables": {
        "baz": "qux"
    },
    "headers": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, sdch",
        "Accept-Language": "en-US,en;q=0.8",
        "Cache-Control": "max-age=0",
        "CloudFront-Forwarded-Proto": "https",
        "CloudFront-Is-Desktop-Viewer": "true",
        "CloudFront-Is-Mobile-Viewer": "false",
        "CloudFront-Is-SmartTV-Viewer": "false",
        "CloudFront-Is-Tablet-Viewer": "false",
        "CloudFront-Viewer-Country": "US",
        "Host": "1234567890.execute-api.us-east-1.amazonaws.com",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Custom User Agent String",
        "Via": "1.1 08f323deadbeefa7af34d5feb414ce27.cloudfront.net (CloudFront)",
        "X-Amz-Cf-Id": "cDehVQoZnx43VYQb9j2-nvCh-9z396Uhbp027Y2JvkCPNLmGJHqlaA==",
        "X-Forwarded-For": "127.0.0.1, 127.0.0.2",
        "X-Forwarded-Port": "443",
        "X-Forwarded-Proto": "https"
    },
    "multiValueHeaders": {
        "Accept": [
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        ],
        "Accept-Encoding": [
            "gzip, deflate, sdch"
        ],
        "Accept-Language": [
            "en-US,en;q=0.8"
        ],
        "Cache-Control": [
            "max-age=0"
        ],
        "CloudFront-Forwarded-Proto": [
            "https"
        ],
        "CloudFront-Is-Desktop-Viewer": [
            "true"
        ],
        "CloudFront-Is-Mobile-Viewer": [
            "false"
        ],
        "CloudFront-Is-SmartTV-Viewer": [
            "false"
        ],
        "CloudFront-Is-Tablet-Viewer": [
            "false"
        ],
        "CloudFront-Viewer-Country": [
            "US"
        ],
        "Host": [
            "0123456789.execute-api.us-east-1.amazonaws.com"
        ],
        "Upgrade-Insecure-Requests": [
            "1"
        ],
        "User-Agent": [
            "Custom User Agent String"
        ],
        "Via": [
            "1.1 08f323deadbeefa7af34d5feb414ce27.cloudfront.net (CloudFront)"
        ],
        "X-Amz-Cf-Id": [
            "cDehVQoZnx43VYQb9j2-nvCh-9z396Uhbp027Y2JvkCPNLmGJHqlaA=="
        ],
        "X-Forwarded-For": [
            "127.0.0.1, 127.0.0.2"
        ],
        "X-Forwarded-Port": [
            "443"
        ],
        "X-Forwarded-Proto": [
            "https"
        ]
    },
    "requestContext": {
        "accountId": "123456789012",
        "resourceId": "123456",
        "stage": "prod",
        "requestId": "c6af9ac6-7b61-11e6-9a41-93e8deadbeef",
        "requestTime": "09/Apr/2015:12:34:56 +0000",
        "requestTimeEpoch": 1428582896000,
        "identity": {
            "cognitoIdentityPoolId": null,
            "accountId": null,
            "cognitoIdentityId": null,
            "caller": null,
            "accessKey": null,
            "sourceIp": "127.0.0.1",
            "cognitoAuthenticationType": null,
            "cognitoAuthenticationProvider": null,
            "userArn": null,
            "userAgent": "Custom User Agent String",
            "user": null
        },
        "path": "/prod/path/to/resource",
        "resourcePath": "/{proxy+}",
        "httpMethod": "POST",
        "apiId": "1234567890",
        "protocol": "HTTP/1.1"
    }
}
    ''')

    # print(event['body']['query_str'])

    lambda_handler(event, None)
