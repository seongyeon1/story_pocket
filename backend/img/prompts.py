story_to_img = """
동화 스타일로, 이야기 내용을 바탕으로 과거 한국의 시골 마을을 배경으로 한 장면을 그려주세요.
전체적으로 동화 같은 부드러운 색채와 따뜻한 분위기를 강조하고, 감동적인 어릴 적 기억을 담은 느낌으로 이미지를 구성해 주세요.

이야기 내용 :
{story}
"""

story_to_imgs = """
동화 스타일로, 이야기의 각 장면을 시각적으로 묘사해주세요. 
과거 한국의 시골 마을을 배경으로 하고, 전체적으로 동화 같은 부드러운 색채와 따뜻한 분위기를 강조해주세요. 
감동적인 어릴 적 기억을 담은 느낌으로 각 장면을 간단하게 나누어 표현해 주세요.
장면은 여섯 컷 이하로 만들어주세요.

각 장면을 아래와 같이 분리하여 설명해주세요:

#첫 번째 장면 묘사 내용
\n\n
#두 번째 장면 묘사 내용
\n\n
#세 번째 장면 묘사 내용
\n\n
#네 번째 장면 묘사 내용
...

이야기 내용:
{story}
"""


description_to_prompt = """
묘사를 바탕으로 이미지를 생성하기 위한 이미지 프롬프트를 작성해주세요.
동화 스타일로, 이야기의 각 장면을 시각적으로 묘사해주세요.
과거 한국의 시골 마을을 배경으로 하고, 전체적으로 동화 같은 부드러운 색채와 따뜻한 분위기를 강조해주세요.
영어로만 작성해주세요.

예시 :
Fairy tale style, a quaint rural village scene set in past Korea, with peaceful scenery and a warm color palette. 
The main focus is a child [행동 묘사: 예시 - walking, playing, sharing a meal, etc.], 
surrounded by [주변 요소: rice fields, mountains, old houses, etc.]. 
The child is [간단한 소품과 동작: holding a small lunchbox, sitting on a grassy hill, etc.]. 
This scene captures a moment of [감정 및 분위기: joy, nostalgia, friendship, simplicity, etc.], 
with detailed touches in [구체적 디테일: traditional clothing, rustic architecture, natural elements, etc.]. 
The overall feeling is one of warmth and simplicity, evoking the timeless charm of a fairy tale illustration.

묘사 :
{description}
"""