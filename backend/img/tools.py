import os
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from PIL import Image
import io

from dotenv import load_dotenv

load_dotenv()

# API 클라이언트 초기화
stability_api = client.StabilityInference(
    key=os.getenv('STABILITY_KEY'),
    verbose=True,
)

# 이미지 생성 함수 정의
def generate_image(prompt, width=512, height=512, steps=50):
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