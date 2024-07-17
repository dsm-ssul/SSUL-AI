import anthropic
import re

client = anthropic.Anthropic(
    api_key="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",
)

def process_user_input(Name , Age ,slary , fixed_expenses,year,target ):#이름 , 나이 , 월급 , 고정비 , 몇년안에 , 얼마모으기
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        temperature=0.7,
        system=f"""
        이름,나이,월급,한달 고정 지출비,{year}년안에 목표 금액을 제공하겠다.
        첫번째 줄 1. 에는 그 나이떄에 알맞는 원그래프를 그리기 위한 생활비 , 고정비 , 저축 , 자산증식 비율의 숫자를 출력해라 예시(1.[30,40,20,10]) 1을 출력하고 다음에 예시처럼 리스트에 묻어서 4개의 원소가 들어가게
        두번째 줄 2. 에는 왜 비율을 정한 이유를 3줄로
        세번째 줄 3. 에 나이때와 월급 수준을 고려하여 어떤한 방식으로 저축(예금,적금 선택 또한 단기로 할지 장기로 할지, 아니면 채권을 할지) 구체적이고 자세히 작성을 해야하고 어떤한 방식으로 재산을 증식해야하는가(주식,부동산 투자등등) 5줄로 문맥이 매끄럽게
        단 출력을 할때는 1.첫번째줄 2.두번째줄 3. 세번째줄 이외에는 n(숫자).를 쓰지말고 **와 같이 강조문구와 -같이 특수문자를 사용하지 말고 그냥 텍스트만 출력해라
        또한 2번째줄은 무조건 3줄이상의 분량으로 3번째줄에는 무조건 5줄이상의 분량으로""",
        messages=[
            {"role": "user", "content": f"""
                이름: {Name}
                나이: {Age}
                월급: {slary}
                한달 고정 지출비: {fixed_expenses}
                {year}년안에 목표금액: {target}"""}]
    )

    result = message.content[0].text
    return result

async def ai(Name , Age ,slary , fixed_expenses,year,target):
    while True:
        text = process_user_input(Name, Age, slary, fixed_expenses, year, target)

        ratio_match = re.search(r'1\.\s*\[(.*?)\]', text, re.DOTALL)
        first_part_match = re.search(r'2\.(.*?)3\.', text, re.DOTALL)
        second_part_match = re.search(r'3\.(.*?)$', text, re.DOTALL)

        if ratio_match and first_part_match and second_part_match:
            ratio = [int(num.strip()) for num in ratio_match.group(1).split(',')] 
            effective_financial_life_first = first_part_match.group(1).strip()
            effective_financial_life_second = second_part_match.group(1).strip()
            return ratio[0] , ratio[1] , ratio[2] , ratio[3],effective_financial_life_first , effective_financial_life_second
            #생활비 , 고정비 , 저축, 재테크 , 첫번쨰 문장 , 두번째 문장 