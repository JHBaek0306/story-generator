import os
from PIL import Image
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration

# 1. 모델과 프로세서 로드
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# 2. 이미지 불러오기 (URL or local)
script_dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(script_dir, "paint.jpg")
image = Image.open(path).convert('RGB')

# 3. 이미지 캡션 생성
inputs = processor(images=image, return_tensors="pt")
with torch.no_grad():
    output = model.generate(**inputs)

caption = processor.decode(output[0], skip_special_tokens=True)
print("생성된 이미지 설명:", caption)
