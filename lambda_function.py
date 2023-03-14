import logging
import os
import sys
import json

from langchain import OpenAI
from llama_index import LLMPredictor, GPTSimpleVectorIndex, SimpleWebPageReader

os.environ['OPENAI_API_KEY'] = "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"

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="gpt-3.5-turbo"))


def read_web_page(url):
    docs = SimpleWebPageReader().load_data([url])
    return docs


def build_index(docs, index_path):
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
    print(response)
    return response


def lambda_handler(event, context):
    url = event['body']['url']
    text_id = event['body']['text_id']
    query_str = event['body']['query_str']
    logging.info("received from request body " + event['body'])

    logging.info("to read web page from " + url)
    docs = read_web_page(url)

    logging.info("to build index into " + text_id)
    build_index(docs, text_id)

    logging.info("to query index by " + query_str)
    resp = query_index(text_id, query_str)

    return {
        'statusCode': 200,
        'body': json.dumps(resp.response)
    }

# if __name__ == '__main__':
# documents = read_web_page("https://dev-felo-meet.s3.ap-northeast-1.amazonaws.com/summary/04e64295e86070cfbba13d2c4ff1deb9/text085e970f0a5720ab99f8618fd625d63d?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBYaDmFwLW5vcnRoZWFzdC0xIkYwRAIgXdQYqLclKabuM0psKjtyVx%2FCcqmaWvPuujnxHFYS8hgCIBQYE2%2FbEL2wogvlW9jAkwVl1AYJTWS5pZoehPCaqtQmKu0CCND%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQARoMOTIxMDIwMDMyNTkxIgzC4ANUapdLPar%2B3KAqwQKDLqgIiYeByKkXeWdb%2Bp0CVG6XVaaF6MrZ5rnDjhvmRPIQt8jf8EB2BsNtU7dYnKm2eCpwUoJRmiX%2F%2Ff3RhFVwcwVADK6TcBb3Sj9vVv3YiR0Hc%2FNhFDNWcUt8kCUjhWsa3P6ECnau%2F7FDaAVxmyYTtXLuKfx7sdEikqkETJ%2FT4Pw7rWgkKPfcWLzx5nw152R1Qh5ydL9Lsiu5Wr%2Flp1fYiXQH0qgbLCacRpmwBX8iCJq4uAZKnHVlVQLMnj3r8b%2BDmKcIOpi%2BDspvIfQB4X%2FFAz5yYmIrSFcfOhoC%2BUGeCnQmCYtA4qNcjr5Rhh9Gqg99h%2B3IWv3JpXgsH6J6J8t6ZyD7VUqKhiYiK7gpRJXK6jwkwmPNsBnjpbNT3XsQWT17oMaK3M6BbENr%2BzNyA1r1%2F0742CnjqHclN3s8vsHu8zAwvrC%2FoAY6tAKHajYjlSH8u229MGGHobMcmOSPiTOWpWKvU4IHl0G9S3QMF%2FuGR3%2Fp4EZv7PTNdIiL3rbTvv9GNTQH9UgExJzrbV7AX9Pwhn8ssu%2BE6ORQ%2Br1CYAnvvPRTv18m5hOuh4O%2Fh8R2co3%2FW5ipUBh0NiCnuM8drFp%2BHnhJUqig8vVm3V7FykFD2knlr%2FhYyzHv7QHIJS8z3qVsluPQhgQ1ZeII4sYj9WM4hvbVXRMou5DFH9nH2A10IxoZ3aHAR9LcPrvOc2pvV%2FzM1YTGK%2FGCguOxZ3OuruLMoFXqhk9DfqahpE9Js1y3s5UHa%2F76QhY8SFgzdJ6UxpW5xwYeR26XMAXFYQYR9rCCL9YD4DAH6Jyocziihi%2F8BgToa637aZtLrZwN7tS2I9EKJB5apWL6TlpfbkHtgQ%3D%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20230314T065222Z&X-Amz-SignedHeaders=host&X-Amz-Expires=7200&X-Amz-Credential=ASIA5M4ISMZH4XZ62QUP%2F20230314%2Fap-northeast-1%2Fs3%2Faws4_request&X-Amz-Signature=57a9097ede877b0c97e4960b34f9edaf9d4e442d0277680362589aa13714a31c")
# build_index(documents, "index_path")
#     query_index("index_path", '''
# 按照我的格式输出会议总结:"
# 【Summary】
# - Summary by points
# - Another point
# 【Action Items】
# - content, Assignee: content, Deadline: content.
# - content, Assignee: content, Deadline: content."
#     ''')
# I need you to output the meeting summary in Chinese follow my format
