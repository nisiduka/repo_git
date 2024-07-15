import os
import datetime
from langchain.agents import initialize_agent, Tool
from langchain.utilities import GoogleSearchAPIWrapper

from langchain.prompts  import PromptTemplate
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI

def create_prompt(user_input):
    prompt = PromptTemplate(
        input_variables=["theme"],
        template="""
        あなたはブロガー
        海外サイトも検索して
        1000文字以上で日本語出力する
        ###
        テーマ:{theme}
        """
    )
    return prompt.format(theme=user_input)

def define_tools():
    search = GoogleSearchAPIWrapper()
    return [
        Tool(
            name = "Search",
            func=search.run,
            description="useful for when you need" 
        ),
    ]

def write_response_to_file(response,filename):
    with open(filename,'w',encoding='utf-8') as file:
        file.write(response)
        #file.write(response)
    print('出力しました')

def main():
    llm= ChatOpenAI(temperature=0,model="gpt-4-turbo",max_tokens=500)
    tools = define_tools()
    agent = initialize_agent(tools,llm,agent=AgentType.OPENAI_FUNCTIONS)
   
    # ユーザーから記事のテーマを入力させる
    user_input = input("記事のテーマを入力: ")
    prompt = create_prompt(user_input)

    # 現在の日付と時刻を取得し、yyyymmddhhmmss形式にフォーマット
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    
    # 入力値を10文字でサマライズ
    summarized_input = user_input[:10]

    # ファイル名を作成
    filename = f"{timestamp}_{summarized_input}.txt"

    response = agent.run(prompt)
    # ファイルに書き込み
    write_response_to_file(response, filename)

if __name__=="__main__":
    main()

#openai.api_key = os.environ["OPENAI_API_KEY"]
