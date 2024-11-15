import os
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from PIL import Image
import io

from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv

load_dotenv()

# API 클라이언트 초기화
stability_api = client.StabilityInference(
    key=os.getenv('STABILITY_KEY'),
    verbose=True,
)

from .preprocessing import story_to_img_chain, story_to_imgs_chain, description_to_prompt_chain

# 이미지 생성 함수 정의
def generate_image(story, width=512, height=512, steps=50):
    description = story_to_img_chain.invoke({"story": story})
    prompt = description_to_prompt_chain.invoke({'description': description})
    answers = stability_api.generate(
        prompt=prompt,
        seed=992446758,
        steps=steps,
        cfg_scale=8.0,
        width=width,
        height=height,
        samples=1,
        sampler=generation.SAMPLER_K_DPMPP_2M
    )

    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.type == generation.ARTIFACT_IMAGE:
                img = Image.open(io.BytesIO(artifact.binary))
                return img
            
# 이미지 생성 함수 정의 (여러 묘사 지원)
def generate_images(story, width=512, height=512, steps=50):
    # story로부터 여러 개의 묘사(description)를 생성
    descriptions = story_to_imgs_chain.invoke({"story": story})

    # 묘사(description)마다 프롬프트를 생성하고 이미지 생성
    images = []
    for description in descriptions.split('\n\n'):  # 묘사를 여러 줄로 구분하는 경우
        prompt = description_to_prompt_chain.invoke({'description': description})
        
        # Stability API를 사용해 이미지 생성
        answers = stability_api.generate(
            prompt=prompt,
            seed=992446758,
            steps=steps,
            cfg_scale=8.0,
            width=width,
            height=height,
            samples=1,
            sampler=generation.SAMPLER_K_DPMPP_2M
        )

        # 생성된 이미지를 리스트에 추가
        for resp in answers:
            for artifact in resp.artifacts:
                if artifact.type == generation.ARTIFACT_IMAGE:
                    img = Image.open(io.BytesIO(artifact.binary))
                    images.append(img)
    
    return images