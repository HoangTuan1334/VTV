# HƯỚNG DẪN THI AI THỰC CHIẾN - VÒNG CHUNG KHẢO

> **Tài liệu tổng hợp**: Tổng hợp toàn bộ hướng dẫn kỹ thuật, API và quy định thi cho cuộc thi AI Thực Chiến

---

## 📋 MỤC LỤC

1. [Quy định và Hướng dẫn kỹ thuật vòng Chung khảo](#1-quy-định-và-hướng-dẫn-kỹ-thuật-vòng-chung-khảo)
2. [Cấu hình API Gateway](#2-cấu-hình-api-gateway)
3. [Các chức năng AI chính](#3-các-chức-năng-ai-chính)
4. [Tips và Tricks thực chiến](#4-tips-và-tricks-thực-chiến)
5. [Best Practices](#5-best-practices)

---

## 1. QUY ĐỊNH VÀ HƯỚNG DẪN KỸ THUẬT VÒNG CHUNG KHẢO

### 1.1. Không gian thi
- Mỗi đội tự chuẩn bị vị trí thi đảm bảo không gian cho **3 thí sinh**
- Không gian phải **yên tĩnh**, không bị ảnh hưởng tiếng ồn
- **TUYỆT ĐỐI KHÔNG** xuất hiện người thứ tư trong khung hình/không gian thi
- Ưu tiên phòng có đủ ánh sáng và kết nối Internet băng thông rộng

### 1.2. Thiết bị kỹ thuật (BẮT BUỘC)

#### 02 Máy tính
- PC hoặc laptop có kết nối Internet
- Thực hiện các yêu cầu đề thi
- Kết nối với hệ thống giám sát Ban tổ chức (ghi lại toàn bộ hoạt động màn hình)

#### 02 Điện thoại thông minh (kèm tripod và giá kẹp)

**Điện thoại 1 - Ghi hình chính:**
- ✅ Bật "Flight/Airplane mode" (KHÔNG kết nối mạng)
- ✅ Kết nối nguồn điện liên tục (sạc suốt phiên thi)
- ✅ Tắt khóa màn hình (không tắt tự động)
- ✅ Đặt ghi hình theo phương ngang (landscape)
- ✅ Định dạng: MP4 hoặc MOV, độ phân giải tối thiểu **Full HD (1920x1080)**
- ✅ Đặt tên file: `MãĐội_TênĐội_NgàyThi` (ví dụ: `A12_TeamAlpha_2025-10-15.mp4`)

**Điện thoại 2 - Giám sát trực tiếp:**
- ✅ Bật kết nối Internet (truyền hình ảnh trực tiếp cho Hội đồng giám thị)
- ✅ Kết nối nguồn điện liên tục
- ✅ Tắt chế độ hiển thị thông báo với tất cả ứng dụng
- ✅ Tắt khóa màn hình
- ✅ Tắt khóa màn hình dọc
- ✅ Đặt quay ngang (landscape)
- ⚠️ **Mã kết nối** sẽ được Ban tổ chức cung cấp trước giờ thi

### 1.3. Quy định nộp kết quả

**Thời gian**: Có **10 phút** sau khi kết thúc làm bài để nộp kết quả

**Bộ kết quả hợp lệ bao gồm:**
1. File kết quả bài làm theo yêu cầu đề thi
2. File video ghi hình quá trình làm bài (Video Điện thoại 1)
   - Upload lên Google Drive/OneDrive với quyền tải xuống
   - Gửi link tải về email chính thức của Ban Tổ chức

**Tiêu chí chấm điểm:** Nội dung bài làm + Quá trình thực hiện trong video giám sát

### 1.4. Xử lý vi phạm

⚠️ **CÁC HÀNH VI BỊ CẤM:**
- Nhận trợ giúp từ bên ngoài
- Sử dụng tư liệu/công cụ không được phép
- Thay người thi

**Mức xử lý:** Trừ điểm, loại bỏ phần thi hoặc hủy kết quả đội thi tùy theo mức độ vi phạm

---

## 2. CẤU HÌNH API GATEWAY

### 2.1. Thông tin cơ bản

- **Base URL**: `https://api.thucchien.ai`
- **API Key**: Sử dụng API key được cung cấp (thay thế `<your_api_key>`)
- **Chuẩn API**: Tuân theo chuẩn OpenAI
- **Framework**: LiteLLM Proxy

### 2.2. Cấu hình client Python

```python
from openai import OpenAI

client = OpenAI(
    api_key="<your_api_key>",
    base_url="https://api.thucchien.ai"
)
```

### 2.3. Kiểm tra chi tiêu

**Endpoint:** `GET /user/info`

```bash
curl https://api.thucchien.ai/user/info \
  -H "Authorization: Bearer <your_api_key>"
```

---

## 3. CÁC CHỨC NĂNG AI CHÍNH

### 3.1. Sinh văn bản (Text Generation)

**Models hỗ trợ:**
- `gemini-2.5-pro` (Google Gemini)
- `gemini-2.5-flash` (Google Gemini)

**Endpoint:** `POST /chat/completions`

**Ví dụ cơ bản:**

```python
from openai import OpenAI

client = OpenAI(
    api_key="<your_api_key>",
    base_url="https://api.thucchien.ai"
)

response = client.chat.completions.create(
    model="gemini-2.5-pro",
    messages=[
        {
            "role": "user",
            "content": "Explain the concept of API gateway in simple terms."
        }
    ]
)

print(response.choices[0].message.content)
```

**Tham số quan trọng:**
- `messages`: Danh sách message trong cuộc hội thoại
- `model`: ID của mô hình
- `max_tokens`: Số token tối đa
- `temperature`: Độ ngẫu nhiên (0-2)
- `stream`: Bật/tắt streaming (true/false)

---

### 3.2. Sinh hình ảnh (Image Generation)

#### 3.2.1. Phương pháp chuẩn (Standard)

**Model hỗ trợ:** `imagen-4` (Google Vertex AI)

**Endpoint:** `POST /images/generations`

**⚠️ LƯU Ý:** API trả về dữ liệu base64 thay vì URL

**Ví dụ với Python (openai):**

```python
from openai import OpenAI
import base64

client = OpenAI(
    api_key="<your_api_key>",
    base_url="https://api.thucchien.ai/v1"
)

response = client.images.generate(
    model="imagen-4",
    prompt="An astronaut riding a horse on Mars, photorealistic",
    n=2  # Yêu cầu 2 ảnh
)

# Xử lý và lưu từng ảnh
for i, image_obj in enumerate(response.data):
    b64_data = image_obj.b64_json
    image_data = base64.b64decode(b64_data)
    
    save_path = f"generated_image_{i+1}.png"
    with open(save_path, 'wb') as f:
        f.write(image_data)
    print(f"Image saved to {save_path}")
```

**💡 Tip tránh lỗi caching:**
```python
import random
prompt = "A beautiful landscape painting, " + str(random.randint(1, 10000))
```

#### 3.2.2. Phương pháp trò chuyện (Chat)

**Model hỗ trợ:** `gemini-2.5-flash-image-preview`

**Endpoint:** `POST /chat/completions`

**Ví dụ với Python (litellm):**

```python
import litellm
import base64
import random

random_prompt_seed = random.randint(1, 10000)

AI_API_BASE = "https://api.thucchien.ai/v1"
AI_API_KEY = "<your_api_key>"
IMAGE_SAVE_PATH = "generated_chat_image.png"

litellm.api_base = AI_API_BASE

response = litellm.completion(
    model="litellm_proxy/gemini-2.5-flash-image-preview",
    messages=[
        {
            "role": "user",
            "content": "Tạo ảnh 2 con mèo bên khung cửa sổ đang nhìn ra vườn hoa. " + str(random_prompt_seed)
        }
    ],
    api_key=AI_API_KEY,
    modalities=["image"]
)

base64_string = response.choices[0].message.images[0].get("image_url").get("url")

# Decode và lưu ảnh
if ',' in base64_string:
    header, encoded = base64_string.split(',', 1)
else:
    encoded = base64_string

image_data = base64.b64decode(encoded)

with open(IMAGE_SAVE_PATH, 'wb') as f:
    f.write(image_data)
    
print(f"Image saved to {IMAGE_SAVE_PATH}")
```

---

### 3.3. Sinh video với Veo 3 (Quy trình bất đồng bộ)

**Model hỗ trợ:** `veo-3.0-generate-preview` (Google Vertex AI)

**⚠️ QUAN TRỌNG:** Sử dụng header `x-goog-api-key` thay vì `Authorization`

#### QUY TRÌNH 3 BƯỚC:

**Bước 1: Bắt đầu tạo video**

```bash
curl -X POST https://api.thucchien.ai/gemini/v1beta/models/veo-3.0-generate-preview:predictLongRunning \
  -H "Content-Type: application/json" \
  -H "x-goog-api-key: <your_api_key>" \
  -d '{
    "instances": [{
      "prompt": "A cinematic shot of a hummingbird flying in slow motion"
    }]
  }'
```

**Response:**
```json
{
  "name": "models/veo-3.0-generate-preview/operations/idrk08ltkg0a"
}
```

Lưu lại `operation_id`: `idrk08ltkg0a`

**Bước 2: Kiểm tra trạng thái**

```bash
curl https://api.thucchien.ai/gemini/v1beta/models/veo-3.0-generate-preview/operations/<operation_id> \
  -H "x-goog-api-key: <your_api_key>"
```

Lặp lại cho đến khi nhận được `"done": true`

**Response khi hoàn thành:**
```json
{
  "name": "models/veo-3.0-generate-preview/operations/idrk08ltkg0a",
  "done": true,
  "response": {
    "@type": "type.googleapis.com/google.ai.generativelanguage.v1beta.PredictLongRunningResponse",
    "generateVideoResponse": {
      "generatedSamples": [{
        "video": {
          "uri": "https://generativelanguage.googleapis.com/v1beta/files/3j6svp4106e7:download?alt=media"
        }
      }]
    }
  }
}
```

Trích xuất `video_id`: `3j6svp4106e7`

**Bước 3: Tải video**

```bash
curl https://api.thucchien.ai/gemini/download/v1beta/files/<video_id>:download?alt=media \
  -H "x-goog-api-key: <your_api_key>" \
  --output my_generated_video.mp4
```

#### Script Python tự động (đầy đủ):

```python
#!/usr/bin/env python3
import json
import os
import time
import requests
from typing import Optional

class VeoVideoGenerator:
    """Complete Veo video generation client using LiteLLM proxy."""
    
    def __init__(self, base_url: str = "https://api.thucchien.ai/gemini/v1beta", 
                 api_key: str = "sk-1234"):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            "x-goog-api-key": api_key,
            "Content-Type": "application/json"
        }
    
    def generate_video(self, prompt: str) -> Optional[str]:
        """Bắt đầu tạo video"""
        print(f"🎬 Generating video with prompt: '{prompt}'")
        
        url = f"{self.base_url}/models/veo-3.0-generate-preview:predictLongRunning"
        payload = {
            "instances": [{
                "prompt": prompt
            }]
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            data = response.json()
            operation_name = data.get("name")
            
            if operation_name:
                print(f"✅ Video generation started: {operation_name}")
                return operation_name
            else:
                print("❌ No operation name returned")
                return None
                
        except requests.RequestException as e:
            print(f"❌ Failed to start video generation: {e}")
            return None
    
    def wait_for_completion(self, operation_name: str, max_wait_time: int = 600) -> Optional[str]:
        """Chờ video hoàn thành"""
        print("⏳ Waiting for video generation to complete...")
        
        operation_url = f"{self.base_url}/{operation_name}"
        start_time = time.time()
        poll_interval = 10
        
        while time.time() - start_time < max_wait_time:
            try:
                print(f"🔍 Polling status... ({int(time.time() - start_time)}s elapsed)")
                
                response = requests.get(operation_url, headers=self.headers)
                response.raise_for_status()
                data = response.json()
                
                if "error" in data:
                    print("❌ Error in video generation:")
                    print(json.dumps(data["error"], indent=2))
                    return None
                
                if data.get("done", False):
                    print("🎉 Video generation complete!")
                    try:
                        video_uri = data["response"]["generateVideoResponse"]["generatedSamples"][0]["video"]["uri"]
                        print(f"📹 Video URI: {video_uri}")
                        return video_uri
                    except KeyError as e:
                        print(f"❌ Could not extract video URI: {e}")
                        return None
                
                time.sleep(poll_interval)
                poll_interval = min(poll_interval * 1.2, 30)
                
            except requests.RequestException as e:
                print(f"❌ Error polling operation status: {e}")
                time.sleep(poll_interval)
        
        print(f"⏰ Timeout after {max_wait_time} seconds")
        return None
    
    def download_video(self, video_uri: str, output_filename: str = "generated_video.mp4") -> bool:
        """Tải video về"""
        print(f"⬇️  Downloading video...")
        
        if video_uri.startswith("https://generativelanguage.googleapis.com/"):
            relative_path = video_uri.replace(
                "https://generativelanguage.googleapis.com/",
                ""
            )
        else:
            relative_path = video_uri

        if self.base_url.endswith("/v1beta"):
            base_path = self.base_url.replace("/v1beta", "/download")
        else:
            base_path = self.base_url

        litellm_download_url = f"{base_path}/{relative_path}"
        
        try:
            response = requests.get(
                litellm_download_url, 
                headers=self.headers, 
                stream=True,
                allow_redirects=True
            )
            response.raise_for_status()
            
            with open(output_filename, 'wb') as f:
                downloaded_size = 0
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)
            
            if os.path.exists(output_filename):
                file_size = os.path.getsize(output_filename)
                if file_size > 0:
                    print(f"✅ Video downloaded successfully!")
                    print(f"📁 Saved as: {output_filename}")
                    print(f"📏 File size: {file_size / (1024*1024):.2f} MB")
                    return True
            
            return False
                
        except requests.RequestException as e:
            print(f"❌ Download failed: {e}")
            return False
    
    def generate_and_download(self, prompt: str, output_filename: str = None) -> bool:
        """Quy trình hoàn chỉnh"""
        if output_filename is None:
            timestamp = int(time.time())
            safe_prompt = "".join(c for c in prompt[:30] if c.isalnum() or c in (' ', '-', '_')).rstrip()
            output_filename = f"veo_video_{safe_prompt.replace(' ', '_')}_{timestamp}.mp4"
        
        # Bước 1: Tạo video
        operation_name = self.generate_video(prompt)
        if not operation_name:
            return False
        
        # Bước 2: Chờ hoàn thành
        video_uri = self.wait_for_completion(operation_name)
        if not video_uri:
            return False
        
        # Bước 3: Tải video
        return self.download_video(video_uri, output_filename)

# SỬ DỤNG
if __name__ == "__main__":
    base_url = os.getenv("LITELLM_BASE_URL", "https://api.thucchien.ai/gemini/v1beta")
    api_key = os.getenv("LITELLM_API_KEY", "<your_api_key>")
    
    generator = VeoVideoGenerator(base_url=base_url, api_key=api_key)
    
    prompt = "A cat playing with a ball of yarn in a sunny garden"
    success = generator.generate_and_download(prompt)
    
    if success:
        print("✅ Video generation completed successfully!")
```

---

### 3.4. Chuyển văn bản thành giọng nói (Text-to-Speech)

**Models hỗ trợ:**
- `gemini-2.5-flash-preview-tts` (Google Gemini)
- `gemini-2.5-pro-preview-tts` (Google Gemini)

**Endpoint:** `POST /audio/speech`

**Ví dụ với Python (openai):**

```python
from openai import OpenAI
from pathlib import Path

client = OpenAI(
    api_key="<your_api_key>",
    base_url="https://api.thucchien.ai"
)

speech_file_path = Path(__file__).parent / "speech_output.mp3"

response = client.audio.speech.create(
    model="gemini-2.5-flash-preview-tts",
    voice="Charon",
    input="Hôm nay là một ngày đẹp trời để lập trình."
)

response.stream_to_file(speech_file_path)
print(f"File âm thanh đã được lưu tại: {speech_file_path}")
```

**Ví dụ với cURL:**

```bash
curl https://api.thucchien.ai/audio/speech \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your_api_key>" \
  -d '{
    "model": "gemini-2.5-flash-preview-tts",
    "input": "Xin chào, đây là một thử nghiệm chuyển văn bản thành giọng nói.",
    "voice": "Zephyr"
  }' \
  --output speech_output.mp3
```

**Các giọng nói (voices) phổ biến:**
- `Zephyr`
- `Puck`
- `Charon`

---

## 4. TIPS VÀ TRICKS THỰC CHIẾN

### 4.1. Đồng nhất nhân vật khi Generate nhiều ảnh

#### Vấn đề:
Mỗi lần generate ảnh, AI tạo ra phiên bản nhân vật khác nhau → Không nhất quán

#### Giải pháp: Sử dụng mô hình đa phương thức

**✅ Ưu điểm:**
- Hiểu cả hình ảnh và văn bản
- Có "trí nhớ" về lịch sử hội thoại
- Đảm bảo tính nhất quán

**📝 Quy trình:**

1. **Bước 1:** Tạo ảnh nhân vật "chuẩn" đầu tiên với mô tả chi tiết
   ```
   Prompt: "a young Japanese detective boy named Kenji, 10 years old, 
   messy black hair, wearing round red glasses and a beige trench coat, anime style"
   ```

2. **Bước 2:** Các lần tạo sau, chỉ cần mô tả hành động/bối cảnh mới
   ```
   Prompt: "He is reading a book in a library"
   ```

3. **Bước 3:** Tiếp tục thay đổi bối cảnh
   ```
   Prompt: "He is chasing someone on a busy Tokyo street"
   ```

**⚠️ LƯU Ý:**
- ✅ Tạo tất cả ảnh trong cùng 1 session chat
- ✅ KHÔNG cần lặp lại mô tả ngoại hình sau lần đầu
- ✅ Quản lý độ dài chat - chỉ giữ messages quan trọng nếu chat quá dài

---

### 4.2. Đồng nhất nhân vật và bối cảnh trong Video AI

#### Vấn đề:
Video dài khó giữ nhất quán nhân vật qua các cảnh quay

#### Giải pháp: Kết hợp kỹ thuật đồng nhất ảnh + Image-to-Video

**📝 Quy trình:**

**Bước 1:** Tạo các ảnh nhân vật/bối cảnh nhất quán
- Sử dụng kỹ thuật đồng nhất nhân vật trên hình ảnh
- Tạo ảnh đại diện cho mỗi đoạn video ngắn

**Bước 2:** Chuyển ảnh thành video ngắn
- Sử dụng Image-to-Video AI
- Input: Ảnh đại diện + Prompt mô tả hành động

**Bước 3:** Ghép các video ngắn lại
- Dùng phần mềm chỉnh sửa video
- Thêm âm thanh, nhạc nền, hiệu ứng chuyển cảnh

**✅ Ưu điểm:**
- Cải thiện đáng kể sự nhất quán
- Linh hoạt điều chỉnh từng đoạn video

**⚠️ Hạn chế:**
- Không đạt 100% nhất quán
- Tốn thời gian hơn

---

### 4.3. Sửa lỗi tiếng Việt của AI tạo ảnh

**Vấn đề:** AI tạo ảnh thường tạo chữ tiếng Việt bị lỗi font, sai chính tả

**Giải pháp:**

**Tip 1: Sử dụng công cụ AI khác để tạo text**
- Dùng AI tạo văn bản riêng
- Sau đó ghép text vào ảnh AI bằng công cụ chỉnh sửa

**Tip 2: Tạo ảnh không có text, sau đó thêm text bằng tay**
- Yêu cầu AI tạo ảnh mà không có chữ
- Dùng Photoshop/Canva để thêm text tiếng Việt chuẩn

---

## 5. BEST PRACTICES

### 5.1. Kỹ thuật Prompting hiệu quả

**✅ Rõ ràng và cụ thể:**
```
❌ Tệ: "Làm một trang web"
✅ Tốt: "Tạo một trang landing page cho sản phẩm XYZ bằng HTML và Tailwind CSS, 
         bao gồm header, khu vực giới thiệu tính năng, và footer."
```

**✅ Cung cấp ngữ cảnh:**
- Nếu thêm code vào dự án có sẵn, cung cấp đoạn code mẫu
- Mô tả cấu trúc hiện tại

**✅ Chia nhỏ nhiệm vụ:**
- Thay vì yêu cầu tạo cả ứng dụng
- Bắt đầu với cấu trúc thư mục
- Sau đó từng component một

---

### 5.2. Phát triển lặp lại (Iterative Development)

**Quy trình:**

1. **Bắt đầu đơn giản:** Yêu cầu phiên bản cơ bản nhất
2. **Kiểm tra và xác thực:** Chạy thử, kiểm tra hoạt động
3. **Tinh chỉnh và cải tiến:** Đưa ra yêu cầu tiếp theo để sửa lỗi, thêm tính năng

---

### 5.3. Hiểu và kiểm soát mã nguồn

**✅ Đọc và hiểu code:**
- Dành thời gian đọc hiểu mã nguồn AI tạo ra
- Phát hiện lỗi và học hỏi

**✅ Ưu tiên bảo mật:**
- Kiểm tra các vấn đề bảo mật phổ biến
- Đặc biệt khi xử lý dữ liệu người dùng
- Không mù quáng tin tưởng vào code AI

**✅ Tối ưu hóa khi cần thiết:**
- AI có thể tạo code hoạt động nhưng không tối ưu
- Chủ động refactor và cải thiện code

---

## 📚 TÀI LIỆU THAM KHẢO

### Tài liệu chính thức:
- **API Gateway**: https://docs.thucchien.ai
- **LiteLLM Documentation**: https://docs.litellm.ai
- **Google Cloud Vertex AI**: https://cloud.google.com/vertex-ai/docs
- **Google AI Studio**: https://ai.google.dev

### Các endpoint API chính:

| Chức năng | Endpoint | Method |
|-----------|----------|--------|
| Chat Completions | `/chat/completions` | POST |
| Image Generation | `/images/generations` | POST |
| Video Generation | `/gemini/v1beta/models/veo-3.0-generate-preview:predictLongRunning` | POST |
| Video Status | `/gemini/v1beta/models/veo-3.0-generate-preview/operations/{id}` | GET |
| Video Download | `/gemini/download/v1beta/files/{id}:download?alt=media` | GET |
| Text-to-Speech | `/audio/speech` | POST |
| User Info | `/user/info` | GET |

---

## ✅ CHECKLIST CHUẨN BỊ THI

### Trước ngày thi:

- [ ] Kiểm tra API key hoạt động
- [ ] Cài đặt Python và các thư viện cần thiết (`openai`, `litellm`, `requests`)
- [ ] Test các chức năng AI cơ bản
- [ ] Chuẩn bị 02 máy tính có Internet
- [ ] Chuẩn bị 02 điện thoại + tripod + giá kẹp
- [ ] Kiểm tra chế độ Flight mode trên điện thoại 1
- [ ] Kiểm tra kết nối Internet điện thoại 2
- [ ] Chuẩn bị cáp sạc cho cả 2 điện thoại
- [ ] Test ghi hình thử (~30 giây)
- [ ] Kiểm tra không gian thi (ánh sáng, tiếng ồn)

### Trong ngày thi:

- [ ] Đặt tên file video theo format: `MãĐội_TênĐội_NgàyThi.mp4`
- [ ] Bật Flight mode điện thoại 1
- [ ] Kết nối Internet điện thoại 2
- [ ] Nhận mã kết nối từ Ban tổ chức
- [ ] Bắt đầu ghi hình trước khi làm bài
- [ ] Hoàn thành bài làm
- [ ] Dừng ghi hình
- [ ] Upload video lên Google Drive/OneDrive
- [ ] Nộp file kết quả + link video trong 10 phút

---

## 🚀 CODE MẪU NHANH

### Python - Chat Completion
```python
from openai import OpenAI

client = OpenAI(api_key="<your_api_key>", base_url="https://api.thucchien.ai")
response = client.chat.completions.create(
    model="gemini-2.5-pro",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)
```

### Python - Image Generation
```python
from openai import OpenAI
import base64

client = OpenAI(api_key="<your_api_key>", base_url="https://api.thucchien.ai/v1")
response = client.images.generate(model="imagen-4", prompt="A cat", n=1)
image_data = base64.b64decode(response.data[0].b64_json)
with open("image.png", 'wb') as f:
    f.write(image_data)
```

### Python - Text-to-Speech
```python
from openai import OpenAI

client = OpenAI(api_key="<your_api_key>", base_url="https://api.thucchien.ai")
response = client.audio.speech.create(
    model="gemini-2.5-flash-preview-tts",
    voice="Charon",
    input="Xin chào!"
)
response.stream_to_file("speech.mp3")
```

---

## 📞 HỖ TRỢ

- **Website**: https://thucchien.ai
- **Documentation**: https://docs.thucchien.ai
- **Email**: [Theo thông báo từ Ban Tổ chức]

---

**Chúc các đội thi thành công! 🎉**

*Tài liệu được tổng hợp từ docs.thucchien.ai - Cập nhật: 2025-10-23*
