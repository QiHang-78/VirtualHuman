import asyncio
import os
import time
import subprocess

import edge_tts
from ttsfunc import VOICE, tts_main
import requests
from argparse import ArgumentParser
import inference
from pydub import AudioSegment

outputpath='--result_dir E:/SadTlker/output/test1.mp4'
import openai
import time
from pathlib import Path

openai.api_key = "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"

class Chat_bot:
    def __init__(self,model):
        self.user = "\nYou: "
        self.bot = "GPT-3: "
        self.model = model
        self.question_list = []
        self.answer_list = []
        self.text = ''
        self.turns = []
        self.last_result = ''

    def dialogue_save(self):
        timestamp = time.strftime("%Y%m%d-%H%M-%S", time.localtime())  # 时间戳
        file_name = 'output/Chat_' + timestamp + '.md'  # 文件名
        f = Path(file_name)
        f.parent.mkdir(parents=True, exist_ok=True)
        with open(file_name, "w", encoding="utf-8") as f:
            for q, a in zip(self.question_list, self.answer_list):
                f.write(f"You: {q}\nGPT-3: {a}\n\n")
        print("对话内容已保存到文件中: " + file_name)

    def Generate(self):
        print('\n请开始你们的对话，以exit结束。')
        while True:
            # 用户输入
            question = input(self.user)
            self.question_list.append(question) # 将问题添加到问题列表中
            # 把输入换成这样，就可以联系上下文进行连续对话了（text里面保存了最新10次对话）
            prompt = self.bot + self.text  + self.user + question
            # 退出命令
            if question == 'exit':
                break
            else:
                try:
                    response = openai.Completion.create(
                        # 模型名称
                        model= self.model,
                        # 用户提供的输入文本，用于指导GPT输出
                        prompt=prompt,
                        # 控制输出的多样性，0-1，其中0表示最保守的输出，1表示最多样化的输出。
                        temperature=0,
                        # 输出的最大长度（输入+输出的token不能大于模型的最大token）,可以动态调整
                        max_tokens=1500,
                        # [控制字符的重复度] -2.0 ~ 2.0 之间的数字，正值会根据新 tokens 在文本中的现有频率对其进行惩罚，从而降低模型逐字重复同一行的可能性
                        frequency_penalty=0.2,
                        # [控制主题的重复度] -2.0 ~ 2.0 之间的数字，正值会根据到目前为止是否出现在文本中来惩罚新 tokens，从而增加模型谈论新主题的可能性
                        presence_penalty=0.15,
                    )
                    result = response["choices"][0]["text"].strip()
                    result = result[result.index('G'):]
                    self.answer_list.append(result) #将回答添加到回答列表中

                    

                    self.last_result = result

                    tts_main_async(self.last_result)
                    args = inference.getargs()
                    inference.sadtalkermain(args)
                    # 只有这样迭代才能连续提问理解上下文
                    self.turns += [question] + [result]
                    # 为了防止超过字数（token）限制，总是取最新5轮对话
                    if len(self.turns) <= 10:
                        self.text = " ".join(self.turns)
                    else:
                        self.text = " ".join(self.turns[-10:])
                    print(result)
                # 打印异常
                except Exception as exc:
                    print(exc)
        # 退出对话后保存
        self.dialogue_save()



# question = input("请输入问题：")
# answer = send_message(question)
# print(answer)

OUTPUT_FILE = "E:/SadTalker/output/tmp.mp3"

async def tts_main_async(TEXT):
    communicate = edge_tts.Communicate(TEXT, VOICE)
    await communicate.save(OUTPUT_FILE)

async def main():
    bot = Chat_bot('text-davinci-003')
    bot.Generate()
        # 完成后删除临时文件
    os.remove(OUTPUT_FILE)
    answer=''

# 创建一个异步事件循环并运行主函数
import asyncio
loop = asyncio.get_event_loop()
loop.run_until_complete(main())


