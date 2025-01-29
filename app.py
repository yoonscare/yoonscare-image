import streamlit as st
import replicate
from PIL import Image
import requests
from io import BytesIO

# Streamlit UI 설정
st.set_page_config(page_title="AI 이미지 생성기", page_icon="🎨", layout="wide")

# 사이드바 설정
st.sidebar.header("🔑 API 설정")
replicate_api = st.sidebar.text_input("Replicate API Key", type="password")

st.sidebar.header("⚙️ 설정")
aspect_ratio = st.sidebar.selectbox("이미지 비율", ["1:1", "3:2", "2:3"], index=1)
output_format = st.sidebar.radio("출력 형식", ["jpg", "png"], index=0)
image_prompt_strength = st.sidebar.slider("이미지 프롬프트 강도", 0.0, 1.0, 0.1)
safety_tolerance = st.sidebar.slider("안전 허용치", 0, 5, 2)

# 메인 UI
st.title("🎨 AI 이미지 생성기")
st.markdown("Replicate AI 모델을 사용하여 원하는 이미지를 생성하세요.")

# 프롬프트 입력
prompt = st.text_area(
    "🔮 원하는 이미지 설명을 입력하세요",
    "Detailed illustration of majestic lion roaring proudly in a dream-like jungle, purple white line art background, clipart on light violet paper texture"
)

# 이미지 생성 버튼
if st.button("✨ 이미지 생성하기"):
    if not replicate_api:
        st.warning("⚠️ API 키를 입력해주세요.")
    else:
        with st.spinner("🔄 이미지를 생성 중입니다... 잠시만 기다려 주세요."):
            try:
                client = replicate.Client(api_token=replicate_api)
                output = client.run(
                    "recraft-ai/recraft-v3",
                    input={
                        "raw": False,
                        "prompt": prompt,
                        "aspect_ratio": aspect_ratio,
                        "output_format": output_format,
                        "safety_tolerance": safety_tolerance,
                        "image_prompt_strength": image_prompt_strength
                    }
                )

                # 출력된 이미지 가져오기
                image_url = str(output)
                response = requests.get(image_url)
                img = Image.open(BytesIO(response.content))

                # 이미지 크기 조정 (최대 너비 400px, 비율 유지)
                max_width = 400
                img.thumbnail((max_width, max_width))

                # 이미지 표시 (use_container_width=False로 크기 고정)
                st.image(img, caption="🖼️ 생성된 이미지", width=max_width)

                # 다운로드 버튼 추가
                img_bytes = BytesIO()
                img.save(img_bytes, format=output_format.upper())
                img_bytes = img_bytes.getvalue()

                st.download_button(
                    label="📥 이미지 다운로드",
                    data=img_bytes,
                    file_name=f"generated_image.{output_format}",
                    mime=f"image/{output_format}"
                )

            except Exception as e:
                st.error(f"⚠️ 에러 발생: {e}")

# 푸터
st.markdown("---")
st.markdown("💡 *AI로 창의적인 이미지를 만들어 보세요!*")
