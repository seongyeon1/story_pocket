story_to_img = """
동화 스타일로, 이야기 내용을 바탕으로 과거 한국의 시골 마을을 배경으로 한 장면을 그려주세요.
전체적으로 동화 같은 부드러운 색채와 따뜻한 분위기를 강조하고, 감동적인 어릴 적 기억을 담은 느낌으로 이미지를 구성해 주세요.

이야기 내용 :
{story}
"""

description_to_prompt = """
묘사를 바탕으로 이미지를 생성하기 위한 이미지 프롬프트를 작성해주세요.
영어로 작성해주세요.

예시 :
Fairy tale style, a quaint rural village scene set in past Korea, with peaceful scenery and a warm color palette. The main focus is a child [행동 묘사: 예시 - walking, playing, sharing a meal, etc.], surrounded by [주변 요소: rice fields, mountains, old houses, etc.]. The child is [간단한 소품과 동작: holding a small lunchbox, sitting on a grassy hill, etc.]. This scene captures a moment of [감정 및 분위기: joy, nostalgia, friendship, simplicity, etc.], with detailed touches in [구체적 디테일: traditional clothing, rustic architecture, natural elements, etc.]. The overall feeling is one of warmth and simplicity, evoking the timeless charm of a fairy tale illustration.

묘사 :
{description}
"""