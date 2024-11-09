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

from .preprocessing import story_to_img_chain, description_to_prompt_chain

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