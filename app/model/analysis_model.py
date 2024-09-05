from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv(override=True)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
assistant = client.beta.assistants.retrieve("asst_caS8vMfyOpzLoA2roNqrW4i2")


def analysis(content):
    thread = client.beta.threads.create()

    client.beta.threads.messages.create(
      thread_id=thread.id,
      role="user",
      content=content
    )

    run = client.beta.threads.runs.create(
      thread_id=thread.id,
      assistant_id=assistant.id
    )

    while run.status != "completed":
      run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    message = client.beta.threads.messages.list(thread_id=thread.id)

    return message.data[0].content[0].text.value

if __name__ == '__main__':
  analysis('''제목: "마음의 팔레트: 오늘의 다채로운 감정들"

오늘 하루는 마치 팔레트에 물감을 얹은 것처럼 다양한 감정들이 나를 스쳐 지나갔다. 아침에 눈을 떴을 때, 창밖으로 비치는 햇살을 보며 느꼈던 기쁨은 하루의 시작을 밝게 해주었다. 따스한 빛이 창문 너머로 스며들 때, 마치 세상이 나에게 미소를 지어주는 것만 같았다. 이런 평화로운 순간들이 가끔은 내가 얼마나 단순한 것에 행복을 느낄 수 있는지를 일깨워준다.

하지만 그 기쁨은 곧 불안으로 바뀌었다. 출근 준비를 하다가 중요한 발표를 앞두고 있다는 생각이 머리를 스치자, 갑자기 마음이 무거워졌다. ‘잘 해낼 수 있을까?’라는 생각에 내 안의 자신감이 흔들리기 시작했고, 준비했던 내용들이 머릿속에서 엉키는 듯했다. 아마 내가 이 순간에 대한 압박감을 스스로 너무 크게 만들어버린 것 같았다.

사무실에 도착해서 동료들과 인사를 나눌 때, 살짝 질투가 스며들었다. 나와 비슷한 시기에 입사한 동료가 얼마 전에 큰 프로젝트를 성공적으로 마무리했다는 이야기를 들었을 때, 나는 그에게 축하를 건넸지만 속으로는 ‘나도 저렇게 인정받고 싶다’는 생각이 들었다. 그 동료의 성과를 축하하는 마음과 동시에 나 자신에 대한 실망도 함께 찾아왔다. 왜 나는 아직 이런 성취를 이루지 못했을까?

그러나 발표 시간이 다가오면서, 생각보다 동료들이 나를 많이 응원해주고 있다는 사실에 감사한 마음이 들었다. 작은 격려의 말 한마디, ‘넌 할 수 있어’라는 말이 나에게는 큰 위로가 되었다. 나는 혼자가 아니었다는 사실에, 그들이 내 곁에 있다는 사실에 묘한 안도감이 밀려왔다.

발표가 끝나고 나니, 처음 느꼈던 불안감이 무색할 만큼 모든 것이 순조롭게 진행되었다. 그 순간 느꼈던 뿌듯함은 내가 오늘 하루를 잘 해냈다는 스스로에 대한 작은 보상처럼 느껴졌다. 사람들은 내 발표에 긍정적인 피드백을 주었고, 나는 내 자신에게 조금 더 자신감을 가져도 된다는 것을 깨달았다.

하지만 퇴근 후 집으로 돌아오는 길, 그제야 하루의 피로가 온몸을 감싸면서 피곤함이 몰려왔다. 머릿속이 텅 빈 것처럼 아무 생각도 하고 싶지 않았고, 그저 집에 가서 쉬고 싶었다. 하루 종일 쌓였던 긴장이 서서히 풀리면서, 몸이 무거워지고 눈꺼풀이 내려앉는 느낌이 들었다.

마지막으로, 저녁을 먹고 침대에 누워 하루를 돌아보니 나 자신에게 조금 더 평화를 허락해주고 싶다는 생각이 들었다. 오늘 하루 동안 느꼈던 다양한 감정들이 나를 조금씩 성장시키고 있다는 생각에, 나 자신에게 조금 더 너그러워지기로 다짐했다.''')