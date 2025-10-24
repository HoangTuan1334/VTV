# 📚 HƯỚNG DẪN XÂY DỰNG HỆ THỐNG TẠO TRUYỆN TRANH TỰ ĐỘNG

> **Phiên bản:** 1.1.0 (Bubble Position Editor Update)  
> **Ngày cập nhật:** 24/10/2025  
> **Chủ đề:** Kỷ niệm 80 năm Quốc khánh Việt Nam 2/9/1945 - 2/9/2025

---

## 📑 MỤC LỤC

1. [Tổng quan hệ thống](#1-tổng-quan-hệ-thống)
2. [Yêu cầu hệ thống](#2-yêu-cầu-hệ-thống)
3. [Cài đặt môi trường](#3-cài-đặt-môi-trường)
4. [Kiến trúc code](#4-kiến-trúc-code)
5. [Chi tiết từng module](#5-chi-tiết-từng-module)
6. [Cấu hình API](#6-cấu-hình-api)
7. [Hướng dẫn sử dụng](#7-hướng-dẫn-sử-dụng)
8. [Build trên máy mới](#8-build-trên-máy-mới)
9. [Lưu ý quan trọng](#9-lưu-ý-quan-trọng)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. TỔNG QUAN HỆ THỐNG

### 1.1. Mô tả

Hệ thống **quoc_khanh_comic_generator.py** là một ứng dụng Python tự động tạo truyện tranh về chủ đề lịch sử Việt Nam, sử dụng Google Gemini AI để:

- ✅ **Sinh kịch bản** tự động hoặc theo yêu cầu
- ✅ **Tạo hình ảnh** cho từng panel với AI
- ✅ **Vẽ bubble lời thoại** thông minh, không che mặt nhân vật
- ✅ **Ghép trang** và xuất PDF hoàn chỉnh
- ✅ **Manual review** từng ảnh trước khi chấp nhận
- ✅ **Chỉnh sửa kịch bản** trước khi tạo ảnh

### 1.2. Tính năng chính

| Tính năng | Mô tả |
|-----------|-------|
| **AI Script Generation** | Gemini 2.0 Flash Exp tự động viết kịch bản JSON |
| **AI Image Generation** | Gemini 2.5 Flash Image tạo ảnh manhwa style |
| **Smart Bubble System** | Bubble nhỏ gọn, đặt ngược với vị trí nhân vật để không che mặt |
| **Bubble Position Editor** | Chỉnh sửa vị trí textbox cho từng nhân vật (NEW v1.1.0) |
| **Character Consistency** | 4 nhân vật nhất quán (An, Bình, Chi, Dũng) |
| **Multi-format Support** | Hỗ trợ 2 format JSON (cũ và mới) |
| **Unlimited Retry** | Thử lại không giới hạn cho đến khi hài lòng |
| **Script Editing** | Xem, chỉnh sửa JSON trước khi tạo ảnh |
| **PDF Export** | Xuất file PDF chất lượng cao |

### 1.3. Workflow tổng quát

```
┌─────────────────┐
│  1. Input       │ → Nhập số trang (3-5)
└────────┬────────┘
         ↓
┌─────────────────┐
│  2. Generate    │ → AI sinh kịch bản JSON
│     Script      │   (hoặc dùng default)
└────────┬────────┘
         ↓
┌─────────────────┐
│  3. Review      │ → Xem, sửa, hoặc tạo lại
│     Script      │   (y/e/r/q)
└────────┬────────┘
         ↓
┌─────────────────┐
│  4. Generate    │ → AI tạo ảnh từng panel
│     Images      │   + Manual review (y/n/e/s)  ← CẬP NHẬT
│                 │   + Edit bubble position  ← MỚI
└────────┬────────┘
         ↓
┌─────────────────┐
│  5. Draw        │ → Vẽ bubble lời thoại
│     Dialogues   │   thông minh với vị trí tùy chỉnh
└────────┬────────┘
         ↓
┌─────────────────┐
│  6. Compose     │ → Ghép panels thành trang
│     Pages       │   (A4 300DPI)
└────────┬────────┘
         ↓
┌─────────────────┐
│  7. Export PDF  │ → QUOC_KHANH_80_NAM.pdf
└─────────────────┘
```

---

## 2. YÊU CẦU HỆ THỐNG

### 2.1. Hệ điều hành

- ✅ **Windows 10/11** (đã test)
- ⚠️ **Linux/MacOS** (cần điều chỉnh đường dẫn font)

### 2.2. Python version

```
Python 3.11+ (khuyến nghị 3.11.14)
```

### 2.3. Thư viện bắt buộc

```
google-generativeai==0.8.3+
Pillow==10.0.0+
requests==2.31.0+
```

### 2.4. API Key

- **Google Gemini API Key** (Free tier hoặc paid)
- Đăng ký tại: https://aistudio.google.com/app/apikey

### 2.5. Font chữ

- **Arial.ttf** (đã có sẵn trong project)
- Hoặc dùng font hệ thống: `C:\Windows\Fonts\arial.ttf` (Windows)

### 2.6. Dung lượng disk

- Tối thiểu: **500MB** (cho ảnh tạm)
- Khuyến nghị: **1GB+**

---

## 3. CÀI ĐẶT MÔI TRƯỜNG

### 3.1. Clone/Copy project

```bash
# Tạo thư mục project
mkdir C:\CodeRac
cd C:\CodeRac

# Copy file chính
copy quoc_khanh_comic_generator.py C:\CodeRac\
```

### 3.2. Tạo môi trường Conda (Khuyến nghị)

```bash
# Tạo môi trường mới
conda create -p C:\CodeRac\.conda python=3.11.14 -y

# Kích hoạt
conda activate C:\CodeRac\.conda
```

**Hoặc dùng venv:**

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
```

### 3.3. Cài đặt thư viện

```bash
pip install google-generativeai pillow requests
```

**Kiểm tra:**

```bash
pip list | findstr "google-generativeai pillow requests"
```

Kết quả mong đợi:
```
google-generativeai    0.8.3
Pillow                 10.4.0
requests               2.31.0
```

### 3.4. Chuẩn bị font chữ

**Cách 1: Copy arial.ttf vào thư mục project**

```bash
copy C:\Windows\Fonts\arial.ttf C:\CodeRac\
copy C:\Windows\Fonts\arialbd.ttf C:\CodeRac\
```

**Cách 2: Dùng font hệ thống** (Code đã hỗ trợ tự động tìm)

---

## 4. KIẾN TRÚC CODE

### 4.1. Cấu trúc file

```
quoc_khanh_comic_generator.py (1476 dòng)
├── PHẦN 1: CẤU HÌNH (dòng 1-205)
│   ├── API Keys
│   ├── Models (text + image)
│   ├── Page Layout (A4 300DPI)
│   ├── 4 Layouts (4-6 panels)
│   ├── Default Story
│   └── Page Prompts (0-6)
│
├── PHẦN 2: LAYOUTS & EXPORT (dòng 206-262)
│   ├── create_layout_preview()
│   ├── select_layouts()
│   └── export_prompts_to_file()
│
├── PHẦN 3: SINH KỊCH BẢN (dòng 263-458)
│   └── generate_story_script()
│       ├── Prompt engineering
│       ├── Gemini AI call
│       └── JSON parsing
│
├── PHẦN 4: SINH HÌNH ẢNH (dòng 459-558)
│   └── generate_image_with_gemini()
│       ├── REST API call
│       ├── Base64 decode
│       └── Image resize
│
├── PHẦN 5: VẼ LỜI THOẠI (dòng 559-876)
│   ├── draw_speech_tail() - 8 hướng
│   ├── draw_character_dialogue() - Smart bubble
│   └── draw_dialogue_bubble() - Wrapper cũ
│
├── PHẦN 6: TẠO PANELS (dòng 877-1200)
│   └── create_panel_images()
│       ├── Generate image loop
│       ├── Manual review (y/n/e/s) ← CẬP NHẬT
│       ├── Bubble position editor ← MỚI
│       ├── Unlimited retry
│       └── Draw dialogues
│
├── PHẦN 7: GHÉP TRANG & PDF (dòng 1201-1310)
│   ├── compose_page()
│   └── create_comic_pdf()
│
└── PHẦN 8: MAIN WORKFLOW (dòng 1311-1572)
    └── main()
        ├── Export prompts
        ├── Input pages
        ├── Generate script
        ├── Review/Edit loop
        ├── Create panels
        ├── Compose pages
        └── Export PDF
```

### 4.2. Các hằng số quan trọng

```python
# API
GEMINI_API_KEY = "YOUR_KEY_HERE"

# Page size (A4 300DPI)
PAGE_W = 2100
PAGE_H = 2970
MARGIN = 50
GAP = 20

# Bubble settings
max_bubble_width = int(w * 0.35)  # 35% panel width
min_bubble_width = int(w * 0.15)  # 15% panel width
margin = 35  # Bubble margin
font_size = max(16, min(28, int(w / 28)))
```

### 4.3. Cấu trúc dữ liệu

#### Story Script JSON Format (NEW - Ưu tiên)

```json
{
  "title": "Kỷ Niệm 80 Năm Quốc Khánh 2/9",
  "characters": [
    {
      "name": "An",
      "description": "Vietnamese high school girl, 16, long black ponytail..."
    }
  ],
  "art_style": "Modern manhwa style...",
  "pages": [
    {
      "page_num": 1,
      "scene_description": "Planning meeting...",
      "panels": [
        {
          "panel_num": 1,
          "dialogues": [
            {
              "character": "An",
              "text": "Chào mọi người!",
              "character_position": "bottom-left",
              "bubble_position": "top-right",
              "tail_direction": "bottom-left"
            }
          ],
          "visual_prompt": "An at BOTTOM-LEFT corner...",
          "characters_in_panel": ["An", "Bình"]
        }
      ]
    }
  ]
}
```

#### Format cũ (Tương thích)

```json
{
  "dialogues": [
    {
      "character": "An",
      "text": "Chào mọi người!",
      "position": "left"
    }
  ]
}
```

---

## 5. CHI TIẾT TỪNG MODULE

### 5.1. Module 1: Cấu hình & Layouts

#### `LAYOUTS` Dictionary

Định nghĩa 4 layout khác nhau:

```python
LAYOUTS = {
    "layout_1": [4 khung 2x2],
    "layout_2": [5 khung: 1 to + 4 nhỏ],
    "layout_3": [6 khung 2x3],
    "layout_intro": [6 khung cho demo page]
}
```

**Định dạng panel:** `(x, y, width, height)`

#### `select_layouts(num_pages)`

- **Input:** Số trang truyện (không bao gồm demo)
- **Output:** List layouts cho tất cả trang (bao gồm demo)
- **Logic:**
  1. Thêm `layout_intro` cho trang 0 (demo)
  2. Random chọn layout cho các trang còn lại

---

### 5.2. Module 2: Sinh Kịch Bản AI

#### `generate_story_script(requirement, pages_info)`

**Nhiệm vụ:** Gọi Gemini AI để tạo kịch bản JSON

**Prompt Engineering:**

```python
prompt = f"""
Bạn là chuyên gia viết kịch bản truyện tranh về lịch sử Việt Nam.

YÊU CẦU: {requirement}

⭐ FORMAT DIALOGUE MỚI (QUAN TRỌNG):
{{
  "character": "An",
  "text": "Lời nói tiếng Việt",
  "character_position": "bottom-left",    # Nhân vật ở đâu
  "bubble_position": "top-right",         # Bubble đặt ngược lại
  "tail_direction": "bottom-left"         # Đuôi chỉ về nhân vật
}}

NGUYÊN TẮC VÀNG: Bubble đặt NGƯỢC LẠI với nhân vật để KHÔNG CHE MẶT
"""
```

**Xử lý response:**

1. Strip markdown code fence (```json)
2. Parse JSON
3. Validate structure
4. Return script hoặc None nếu lỗi

**⚠️ LƯU Ý:** Gemini có thể trả về format cũ (`position`) hoặc mới (`bubble_position`). Code hỗ trợ cả 2.

---

### 5.3. Module 3: Sinh Hình Ảnh AI

#### `generate_image_with_gemini(prompt, width, height)`

**API Endpoint:**
```
POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent
```

**Request Body:**
```json
{
  "contents": [{
    "parts": [{"text": "prompt here"}]
  }],
  "generation_config": {
    "response_modalities": ["image"],
    "response_mime_type": "image/png"
  }
}
```

**Response:**
```json
{
  "candidates": [{
    "content": {
      "parts": [{
        "inline_data": {
          "mime_type": "image/png",
          "data": "base64_string_here"
        }
      }]
    }
  }]
}
```

**Xử lý:**
1. Decode base64 → bytes
2. BytesIO → PIL Image
3. Resize nếu cần: `image.resize((width, height), Image.LANCZOS)`
4. Return PIL Image

---

### 5.4. Module 4: Vẽ Bubble Thông Minh

#### `draw_speech_tail()` - Vẽ đuôi bubble

**Hỗ trợ 8 hướng:**

| Position | Mô tả | Đuôi chỉ về |
|----------|-------|-------------|
| `left` | Nhân vật bên trái | ← Trái |
| `right` | Nhân vật bên phải | → Phải |
| `top-left` | Góc trên trái | ↖ Chéo |
| `top-right` | Góc trên phải | ↗ Chéo |
| `bottom-left` | Góc dưới trái | ↙ Chéo |
| `bottom-right` | Góc dưới phải | ↘ Chéo |
| `top` | Phía trên | ↑ Lên |
| `bottom` | Phía dưới | ↓ Xuống |

**Code example:**
```python
if position == "bottom-left":
    tail_points = [
        (bubble_x + 20, bubble_y + bubble_height),
        (bubble_x - 10, bubble_y + bubble_height + 15),
        (bubble_x + 35, bubble_y + bubble_height)
    ]
```

#### `draw_character_dialogue()` - Vẽ bubble + text

**Thuật toán:**

```
1. Parse dialogue format (new hoặc old)
2. Tính kích thước bubble:
   - max_width = 35% panel
   - min_width = 15% panel
   - Wrap text, max 3 lines
   - Tính actual_width từ text dài nhất
3. Xác định vị trí bubble:
   - Dựa vào bubble_position
   - margin = 35px
   - Đặt tại góc/cạnh/giữa
4. Vẽ tail (nếu có)
5. Vẽ bubble:
   - Shadow (offset 3px)
   - Rounded rectangle (radius 12px)
   - Border (width 3px)
6. Vẽ text:
   - Tên nhân vật (bold)
   - Nội dung (center-aligned)
   - Shadow + main text
```

**Màu sắc:**
```python
character_colors = {
    "An": (255, 200, 200, 240),      # Hồng
    "Bình": (200, 220, 255, 240),    # Xanh
    "Chi": (255, 240, 200, 240),     # Vàng
    "Dũng": (220, 255, 220, 240),    # Xanh lá
}
```

**⚠️ QUAN TRỌNG:** Bubble position logic

```python
if bubble_pos == "center-top":
    # AN TOÀN NHẤT: không che nhân vật
    bubble_x = (w - actual_bubble_width) // 2
    bubble_y = margin
elif bubble_pos == "top-left":
    bubble_x = margin
    bubble_y = margin
elif bubble_pos == "bottom-right":
    bubble_x = w - actual_bubble_width - margin
    bubble_y = h - bubble_height - margin
# ... 8 positions tổng cộng
```

---

### 5.5. Module 5: Tạo Panel Images

#### `create_panel_images(story_script, selected_layouts)`

**Workflow chi tiết:**

```python
for page in pages:
    for panel in panels:
        # 1. Build visual prompt
        prompt = f"Character {char}: {desc}, ..."
        
        # 2. Generate image với AI
        while True:  # UNLIMITED RETRY
            img = generate_image_with_gemini(prompt, w, h)
            
            # 3. Save temp
            img.save(f"temp_panel_{page}_{panel}.png")
            
            # 4. Manual review
            choice = input("y/n/s: ")
            
            if choice == 'y':
                # 5. Draw dialogues
                img = draw_character_dialogue(img, dialogues)
                
                # 6. Save final
                img.save(f"panel_images/...")
                break
            elif choice == 's':
                # Skip panel
                break
            elif choice == 'n':
                # Retry
                continue
```

**⚠️ LƯU Ý:**
- Không giới hạn số lần retry
- Temp images được xóa sau khi accept
- Error handling: hỏi continue hoặc skip

---

### 5.6. Module 6: Ghép Trang & PDF

#### `compose_page(page_num, panels)`

**Logic:**

```python
# 1. Tạo canvas trắng A4
canvas = Image.new('RGB', (PAGE_W, PAGE_H), 'white')

# 2. Paste từng panel
for (x, y, w, h), panel_img in zip(layout, panels):
    canvas.paste(panel_img, (x, y))

# 3. Vẽ border cho mỗi panel
draw = ImageDraw.Draw(canvas)
for (x, y, w, h) in layout:
    draw.rectangle([x, y, x+w, y+h], outline='black', width=3)

return canvas
```

#### `create_comic_pdf(final_pages, output_filename)`

```python
# 1. Lấy page đầu tiên
first_page = final_pages[0]

# 2. Convert tất cả sang RGB
rgb_pages = [page.convert('RGB') for page in final_pages]

# 3. Save PDF
first_page.save(
    output_filename,
    save_all=True,
    append_images=rgb_pages[1:],
    resolution=300.0
)
```

---

## 6. CẤU HÌNH API

### 6.1. Lấy Gemini API Key

1. Truy cập: https://aistudio.google.com/app/apikey
2. Đăng nhập Google Account
3. Click **"Create API Key"**
4. Copy key (dạng: `AIzaSy...`)

### 6.2. Thay thế API Key trong code

**Dòng 28:**
```python
GEMINI_API_KEY = "AIzaSyCwhqIs7GrVi1G6wgtejD_w_niFFQws6mo"  # ❌ Key cũ
```

**Thay bằng:**
```python
GEMINI_API_KEY = "YOUR_NEW_API_KEY_HERE"  # ✅ Key của bạn
```

**Hoặc dùng biến môi trường (Khuyến nghị):**

```python
import os
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "default_key")
```

**Set biến môi trường:**
```bash
# Windows PowerShell
$env:GEMINI_API_KEY="AIzaSy..."

# Linux/Mac
export GEMINI_API_KEY="AIzaSy..."
```

### 6.3. Models sử dụng

| Model | Dùng cho | Version |
|-------|----------|---------|
| `gemini-2.0-flash-exp` | Text generation (script) | Experimental |
| `gemini-2.5-flash-image` | Image generation | Beta |

**⚠️ LƯU Ý:**
- `gemini-2.5-flash-image` chỉ có trên REST API (chưa có trong SDK)
- Code đã implement REST API call thủ công

---

## 7. HƯỚNG DẪN SỬ DỤNG

### 7.1. Chạy script

```bash
cd C:\CodeRac
conda activate C:\CodeRac\.conda
python quoc_khanh_comic_generator.py
```

### 7.2. Workflow từng bước

#### **Bước 1: Export prompts**

Script tự động xuất file `PROMPTS_TONG_QUAN_QUOC_KHANH.txt` với chi tiết 7 trang.

#### **Bước 2: Nhập số trang**

```
📖 Nhập số trang truyện (khuyến nghị 3-5 trang): 3
```

→ Sẽ tạo 4 trang (1 demo + 3 nội dung)

#### **Bước 3: Chọn layouts**

```
✅ Đã chọn layouts:
   Trang 0: layout_intro (6 khung) [DEMO]
   Trang 1: layout_3 (6 khung)
   Trang 2: layout_2 (5 khung)
   Trang 3: layout_2 (5 khung)
```

#### **Bước 4: Sinh kịch bản**

AI tạo kịch bản JSON, sau đó hiển thị tóm tắt.

#### **Bước 5: Review kịch bản**

```
❓ Lựa chọn của bạn (y/e/r/q):
```

- **y** - Accept, bắt đầu tạo ảnh
- **e** - Mở JSON editor để sửa
- **r** - Tạo lại kịch bản mới
- **q** - Thoát

**Nếu chọn 'e':**
1. File JSON mở trong notepad
2. Sửa text, dialogues, positions, v.v.
3. Save và đóng notepad
4. Script tiếp tục

#### **Bước 6: Tạo ảnh panels (CẬP NHẬT v1.1.0)**

Với mỗi panel:

```
🎨 Panel 1: 1000x950px
   💬 Hội thoại: 2 nhân vật
      - An: Chào mọi người!...
      - Bình: Vâng đúng rồi!...
   
⏳ Đang tạo ảnh...
✅ Ảnh tạm: TEMP_page_01_panel_01.png

════════════════════════════════════════════════
🖼️  ẢNH VỪA TẠO:
📁 File: TEMP_page_01_panel_01.png
📐 Kích thước: (1000, 950)
📝 Prompt: Four students sitting around table...
════════════════════════════════════════════════

👀 Vui lòng mở file và xem ảnh!
📂 Đường dẫn: C:\CodeRac\panel_images\TEMP_...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 LỰA CHỌN:
   y - ✅ Chấp nhận ảnh này
   n - 🔄 Tạo lại ảnh hoàn toàn
   e - ✏️  Chỉnh sửa vị trí textbox  ← MỚI!
   s - ⏭️  Bỏ qua panel này
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❓ Lựa chọn của bạn (y/n/e/s):
```

**Nếu chọn 'y':**
- Vẽ bubble lời thoại
- Save vào `panel_images/`
- Xóa temp
- Next panel

**Nếu chọn 'n':**
- Tạo lại ảnh với prompt giống
- Unlimited retry

**Nếu chọn 'e' - CHỈNH SỬA VỊ TRÍ TEXTBOX (MỚI):**

```
✏️  CHỈNH SỬA VỊ TRÍ TEXTBOX
════════════════════════════════════════════════
📝 Danh sách textbox hiện tại:
   1. An: 'Chào mọi người!...' → Vị trí: bottom-left
   2. Bình: 'Vâng đúng rồi!...' → Vị trí: bottom-right

❓ Chọn textbox để chỉnh (1-2, 0=Xong): 1

📍 VỊ TRÍ CÓ SẴN cho 'An':
   1. ⬆️  Giữa trên (an toàn nhất)
   2. ↖️  Góc trên trái
   3. ↗️  Góc trên phải
   4. ⏺️  Chính giữa
   5. ⬅️  Bên trái giữa
   6. ➡️  Bên phải giữa
   7. ↙️  Góc dưới trái
   8. ↘️  Góc dưới phải
   9. ⬇️  Giữa dưới

❓ Chọn vị trí mới (1-9): 1
✅ Đã cập nhật 'An' → Giữa trên

❓ Chọn textbox để chỉnh (1-2, 0=Xong): 2
❓ Chọn vị trí mới (1-9): 1
✅ Đã cập nhật 'Bình' → Giữa trên

❓ Chọn textbox để chỉnh (1-2, 0=Xong): 0

🎨 Đang vẽ lại textbox với vị trí mới...
✅ Đã cập nhật! Vui lòng xem lại file: TEMP_page_01_panel_01.png

[Quay lại menu chính để xem và quyết định]
```

**Nếu chọn 's':**
- Bỏ qua panel
- Tạo placeholder trắng

#### **Bước 7: Ghép trang**

```
📄 Tạo trang 1...
✅ Đã lưu: final_comic/page_1.png
```

#### **Bước 8: Xuất PDF**

```
📕 Tạo file PDF...
✅ Đã tạo PDF: final_comic/QUOC_KHANH_80_NAM.pdf
```

### 7.3. Output files

```
C:\CodeRac\
├── PROMPTS_TONG_QUAN_QUOC_KHANH.txt  # Prompts tổng quan
├── story_script_TEMP.json             # Kịch bản tạm
├── panel_images\                      # Ảnh panels
│   ├── page_0_panel_1.png
│   ├── page_0_panel_2.png
│   └── ...
└── final_comic\                       # Output cuối
    ├── page_0.png
    ├── page_1.png
    ├── ...
    └── QUOC_KHANH_80_NAM.pdf         # 🎯 FILE CHÍNH
```

---

## 8. BUILD TRÊN MÁY MỚI

### 8.1. Checklist chuẩn bị

- [ ] Python 3.11+ đã cài
- [ ] Conda hoặc venv đã setup
- [ ] Có kết nối Internet (gọi API)
- [ ] Có Gemini API Key
- [ ] Có file `quoc_khanh_comic_generator.py`

### 8.2. Các bước thực hiện

#### **Bước 1: Setup thư mục**

```bash
# Tạo thư mục project
mkdir C:\CodeRac
cd C:\CodeRac

# Copy file chính vào
copy path\to\quoc_khanh_comic_generator.py .
```

#### **Bước 2: Tạo môi trường Python**

**Option A: Conda (Khuyến nghị)**

```bash
conda create -p C:\CodeRac\.conda python=3.11 -y
conda activate C:\CodeRac\.conda
```

**Option B: venv**

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### **Bước 3: Cài thư viện**

```bash
pip install google-generativeai pillow requests
```

**Verify:**
```bash
python -c "import google.generativeai as genai; import PIL; print('OK')"
```

#### **Bước 4: Cấu hình API Key**

**Mở file và sửa dòng 28:**

```python
GEMINI_API_KEY = "YOUR_API_KEY_HERE"
```

**Hoặc dùng biến môi trường:**

```bash
$env:GEMINI_API_KEY="AIzaSy..."
```

**Và sửa code dòng 28:**
```python
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
```

#### **Bước 5: Chuẩn bị font**

**Cách 1: Copy font vào project**

```bash
copy C:\Windows\Fonts\arial.ttf C:\CodeRac\
copy C:\Windows\Fonts\arialbd.ttf C:\CodeRac\
```

**Cách 2: Sửa đường dẫn font trong code (dòng ~658)**

```python
# Nếu dùng MacOS/Linux
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
```

#### **Bước 6: Tạo thư mục output**

```bash
mkdir panel_images
mkdir final_comic
```

**Hoặc để code tự tạo** (đã có `os.makedirs(..., exist_ok=True)`)

#### **Bước 7: Test chạy**

```bash
python quoc_khanh_comic_generator.py
```

**Nếu thành công:**
```
✅ Đã cấu hình Gemini API
================================================================================
🇻🇳 HỆ THỐNG TẠO TRUYỆN TRANH - KỶ NIỆM 80 NĂM QUỐC KHÁNH 2/9
================================================================================
```

---

## 9. LƯU Ý QUAN TRỌNG

### 9.1. ⚠️ API Key

- **KHÔNG commit API key lên Git/GitHub**
- Dùng `.env` file hoặc biến môi trường
- Mỗi máy phải có API key riêng

**Tạo .env file:**
```
GEMINI_API_KEY=AIzaSy...
```

**Đọc trong code:**
```python
from dotenv import load_dotenv
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
```

### 9.2. ⚠️ Font path

**Windows:**
```python
font = ImageFont.truetype("arial.ttf", font_size)
# hoặc
font = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", font_size)
```

**Linux:**
```python
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
```

**MacOS:**
```python
font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
```

**⚠️ LƯU Ý:** Code hiện tại có try-except để tự động fallback.

### 9.3. ⚠️ API Rate Limit

**Gemini Free Tier:**
- 15 requests/minute
- 1,500 requests/day
- 1 million tokens/day

**Nếu gặp lỗi `429 Too Many Requests`:**
- Thêm delay giữa các request:

```python
import time
time.sleep(5)  # Chờ 5 giây
```

**Đã có trong code (dòng ~1001):**
```python
except Exception as e:
    print(f"❌ Lỗi tạo ảnh: {e}")
    retry = input("Tiếp tục thử (c) hay Bỏ qua (s)? ")
```

### 9.4. ⚠️ Image size

**Gemini 2.5 Flash Image:**
- Recommended: 1024x1024
- Max: 2048x2048
- Format: PNG

**Panel size trong code:**
```python
# Layout 1: 1000x1400
# Layout 2: 1050x950, 2100x900
# Layout 3: 1000x950
```

**⚠️ Nếu ảnh quá lớn:**
- AI có thể timeout
- Giảm PAGE_W, PAGE_H xuống

### 9.5. ⚠️ Dialogue format

**Code hỗ trợ 2 format:**

**Format MỚI (Khuyến nghị):**
```json
{
  "character": "An",
  "text": "...",
  "character_position": "bottom-left",
  "bubble_position": "top-right",
  "tail_direction": "bottom-left"
}
```

**Format CŨ (Tương thích):**
```json
{
  "character": "An",
  "text": "...",
  "position": "left"
}
```

**⚠️ Nếu AI trả về format cũ:**
- Code tự động convert sang logic mới
- Bubble vẫn vẽ được nhưng chưa tối ưu

### 9.6. ⚠️ Character consistency

**Để nhân vật nhất quán:**

1. **Dùng character reference** (Trang 0 - Demo)
2. **Mô tả chi tiết** trong visual_prompt:
   ```
   "Character An: Vietnamese girl, 16, long black ponytail, 
    white áo dài with red details, bright brown eyes, 
    160cm tall, friendly smile"
   ```

3. **Lặp lại mô tả** trong mỗi prompt
4. **Retry nhiều lần** nếu không giống

### 9.7. ⚠️ Bubble không che mặt

**Nguyên tắc:**

| Nhân vật ở | Bubble đặt | Lý do |
|------------|------------|-------|
| `bottom-left` | `top-right` | Nhân vật dưới trái, bubble trên phải → không che |
| `bottom-right` | `top-left` | Tương tự |
| `center-bottom` | `center-top` | AN TOÀN NHẤT |
| `left` | `right` | Nhân vật trái, bubble phải |

**⚠️ AI phải được hướng dẫn rõ trong prompt:**

```python
prompt = """
Trong visual_prompt PHẢI mô tả: "character An at BOTTOM-LEFT corner"
Trong dialogue PHẢI có: "character_position": "bottom-left"
"""
```

### 9.8. ⚠️ Temp files

**Code tạo temp files:**
```
temp_panel_0_1.png
temp_panel_0_2.png
...
```

**⚠️ Tự động xóa sau khi accept:**
```python
if choice == 'y':
    os.remove(temp_path)  # Xóa temp
```

**⚠️ Nếu script crash:**
- Temp files vẫn còn
- Xóa thủ công: `del temp_panel_*.png`

### 9.9. ⚠️ PDF resolution

**Code set resolution 300 DPI:**
```python
first_page.save(
    output_filename,
    resolution=300.0  # High quality
)
```

**⚠️ File size:**
- 1 trang A4 300DPI PNG: ~5-10MB
- PDF 5 trang: ~30-50MB

**Giảm size:**
```python
# Option 1: Giảm resolution
resolution=150.0  # 150 DPI

# Option 2: Compress
img.save(..., optimize=True, quality=85)
```

### 9.10. ⚠️ Script editing

**Khi chọn 'e' (Edit script):**

```python
os.system(f'notepad "{script_path}"')  # Windows
```

**⚠️ Nếu dùng Linux/Mac:**
```python
# Linux
os.system(f'gedit "{script_path}"')
# hoặc
os.system(f'nano "{script_path}"')

# Mac
os.system(f'open -a TextEdit "{script_path}"')
```

**Thay đổi tại dòng ~1287:**
```python
if choice == 'e':
    print(f"\n📝 Mở file JSON: {script_path}")
    # Sửa lại cho phù hợp OS
    os.system(f'notepad "{script_path}"')  # Windows
    # os.system(f'nano "{script_path}"')  # Linux
    input("\n⏸️ Nhấn Enter sau khi sửa xong và SAVE file...")
```

---

## 10. TROUBLESHOOTING

### 10.1. Lỗi: "Module 'google.generativeai' not found"

**Nguyên nhân:** Chưa cài thư viện

**Giải pháp:**
```bash
pip install google-generativeai
```

### 10.2. Lỗi: "Invalid API key"

**Nguyên nhân:** API key sai hoặc hết hạn

**Giải pháp:**
1. Kiểm tra key tại: https://aistudio.google.com/app/apikey
2. Tạo key mới
3. Thay trong code (dòng 28)

### 10.3. Lỗi: "429 Too Many Requests"

**Nguyên nhân:** Vượt quá rate limit

**Giải pháp:**
```python
# Thêm delay trước API call (dòng ~480)
time.sleep(5)  # Chờ 5 giây
response = requests.post(...)
```

### 10.4. Lỗi: "Font not found"

**Nguyên nhân:** Không tìm thấy arial.ttf

**Giải pháp:**

**Option 1:** Copy font vào project
```bash
copy C:\Windows\Fonts\arial.ttf C:\CodeRac\
```

**Option 2:** Sửa đường dẫn (dòng ~658)
```python
font = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", font_size)
```

**Option 3:** Dùng default font
```python
font = ImageFont.load_default()
```

### 10.5. Lỗi: "ValueError: Invalid format specifier"

**Nguyên nhân:** Dấu ngoặc nhọn `{}` trong f-string

**Giải pháp:** Escape bằng `{{}}`

**Ví dụ:**
```python
# ❌ Sai
prompt = f"""
  {{"character": "An"}}
"""

# ✅ Đúng
prompt = f"""
  {{{{"character": "An"}}}}
"""
```

**Đã fix trong code (dòng ~360)**

### 10.6. Lỗi: "JSON decode error"

**Nguyên nhân:** AI trả về JSON không hợp lệ

**Giải pháp:**

1. **Retry:** Chọn 'r' để tạo lại script
2. **Manual edit:** Chọn 'e' để sửa JSON
3. **Check format:**
   ```json
   {
     "title": "...",
     "characters": [...],
     "pages": [...]
   }
   ```

### 10.7. Lỗi: "Image generation timeout"

**Nguyên nhân:** API timeout (>60s)

**Giải pháp:**

1. **Giảm image size:**
   ```python
   PAGE_W = 1600  # Thay vì 2100
   PAGE_H = 2200  # Thay vì 2970
   ```

2. **Thêm timeout:**
   ```python
   response = requests.post(..., timeout=120)
   ```

3. **Retry:** Chọn 'n' để thử lại

### 10.8. Lỗi: "Bubble che mất nhân vật"

**Nguyên nhân:** AI không sinh đúng positions

**Giải pháp:**

**Option 1:** Manual edit JSON
```json
{
  "character_position": "bottom-left",
  "bubble_position": "top-right",
  "tail_direction": "bottom-left"
}
```

**Option 2:** Dùng center-top (an toàn nhất)
```json
{
  "bubble_position": "center-top",
  "tail_direction": "bottom"
}
```

### 10.9. Lỗi: "Nhân vật không nhất quán"

**Nguyên nhân:** Mô tả không đủ chi tiết

**Giải pháp:**

1. **Thêm chi tiết trong character description:**
   ```json
   {
     "name": "An",
     "description": "Vietnamese high school girl, age 16, 
                     long black hair in high ponytail, 
                     bright brown eyes, fair skin, 
                     160cm tall, slim build,
                     white áo dài with red details on collar,
                     energetic expression, friendly smile,
                     always wear red ribbon in hair"
   }
   ```

2. **Lặp lại mô tả trong mỗi visual_prompt**

3. **Tạo reference sheet** (Trang 0)

4. **Retry nhiều lần** nếu không giống

### 10.10. Lỗi: "PDF quá lớn"

**Nguyên nhân:** Resolution cao (300 DPI)

**Giải pháp:**

**Option 1:** Giảm resolution
```python
first_page.save(..., resolution=150.0)
```

**Option 2:** Compress images
```python
img = img.convert('RGB')
img.save(..., optimize=True, quality=85)
```

**Option 3:** Export PNG thay vì PDF
```python
for i, page in enumerate(final_pages):
    page.save(f"page_{i}.png", optimize=True)
```

### 10.11. Lỗi: "IndexError: list index out of range" (MỚI - v1.1.0)

**Nguyên nhân:** Số trang trong script không khớp với số layouts

**Giải pháp:**

**Đã fix trong code v1.1.0:**
```python
# Tìm layout theo page_num thay vì dùng index
for layout in selected_layouts:
    if layout['page_num'] == page_num:
        layout_info = layout
        break
```

**Nếu vẫn lỗi:**
1. Kiểm tra `story_script['pages']` có đầy đủ không
2. Kiểm tra `selected_layouts` có đủ cho tất cả pages không
3. Chọn 'r' để tạo lại script

### 10.12. Lỗi: "Không chỉnh được vị trí bubble" (MỚI - v1.1.0)

**Nguyên nhân:** Panel không có dialogues

**Giải pháp:**

```
⚠️  Panel này không có lời thoại để chỉnh sửa
```

- Chọn 'y' để chấp nhận ảnh
- Hoặc 'n' để tạo lại
- Hoặc 'e' trong script editor để thêm dialogues

---

## 11. BEST PRACTICES

### 11.1. Tối ưu prompt

**✅ TỐT:**
```
"Vietnamese high school girl An, age 16, long black ponytail, 
white áo dài, at BOTTOM-LEFT corner, looking up and smiling, 
Vietnamese classroom background, patriotic posters on wall"
```

**❌ XẤU:**
```
"A girl in classroom"
```

### 11.2. Character consistency tips

1. **Luôn dùng trang 0 (Demo)** - Character reference
2. **Copy-paste mô tả** vào mỗi prompt
3. **Mention previous panels:**
   ```
   "Same character An from previous panels..."
   ```

4. **Retry nhiều lần** cho đến khi giống

### 11.3. Bubble placement tips (CẬP NHẬT v1.1.0)

**✅ TỐT:**
- Nhân vật dưới → Bubble trên
- Nhân vật trái → Bubble phải
- Dùng `center-top` khi không chắc chắn
- **Dùng chức năng 'e' để điều chỉnh** nếu vị trí không hợp lý

**❌ TRÁNH:**
- Nhân vật dưới trái + Bubble dưới trái → CHE MẶT
- Quá nhiều bubble trong 1 panel → RỐI

**💡 MẸO:**
- Chọn 'e' sau khi xem ảnh để chỉnh vị trí textbox
- Thử nhiều vị trí khác nhau cho đến khi hài lòng
- 9 vị trí có sẵn: góc, cạnh, giữa
- Vẽ lại ngay lập tức, không cần tạo ảnh mới

### 11.4. Manual review best practices (CẬP NHẬT v1.1.0)

- **Xem kỹ mặt nhân vật:** Có giống không?
- **Kiểm tra bối cảnh:** Đúng yêu cầu không?
- **Chất lượng ảnh:** Có blur, artifact không?
- **Kiểm tra vị trí bubble:** Có che mặt nhân vật không?
  - Nếu có → Chọn 'e' để chỉnh lại
  - Thử vị trí khác cho hợp lý
- **Không ngại retry:** Unlimited attempts!
- **Không ngại chỉnh bubble:** Vẽ lại nhanh chóng!

### 11.5. Error handling

```python
try:
    result = risky_function()
except Exception as e:
    print(f"❌ Lỗi: {e}")
    choice = input("Tiếp tục (c) hay Bỏ qua (s)? ")
    if choice == 's':
        return None
    else:
        # Retry
        result = risky_function()
```

---

## 12. CHANGELOG & VERSION HISTORY

### Version 1.1.0 (24/10/2025) - LATEST

**Tính năng mới:**
- ✅ **Bubble Position Editor** - Chỉnh sửa vị trí textbox trực tiếp
  - Menu 'e' trong review screen
  - 9 vị trí có sẵn với emoji trực quan
  - Vẽ lại ngay lập tức
  - Chỉnh nhiều lần không giới hạn
- ✅ **IndexError Fix** - Sửa lỗi khi số trang không khớp với layouts
  - Tìm layout theo page_num thay vì index
  - Xử lý trường hợp thiếu layout

**Cải tiến:**
- 🔧 Review menu mở rộng: y/n/e/s (thêm 'e')
- 🔧 Tự động cập nhật tail_direction khi đổi vị trí
- 🔧 Giữ ảnh gốc để vẽ lại bubble
- 📝 Cập nhật docs với hướng dẫn chỉnh bubble

### Version 1.0.0 (24/10/2025)

**Tính năng:**
- ✅ AI script generation với Gemini 2.0 Flash
- ✅ AI image generation với Gemini 2.5 Flash Image
- ✅ Smart bubble system với 8 hướng đuôi
- ✅ Manual review (y/n/s) unlimited retry
- ✅ Script editing (JSON editor)
- ✅ 2 dialogue formats (old + new)
- ✅ PDF export 300 DPI
- ✅ 4 layouts (4-6 panels)
- ✅ Character consistency system

**Cải tiến so với phiên bản notebook:**
- 🔄 Standalone Python script (không cần Jupyter)
- 🔄 Bubble thông minh, không che mặt
- 🔄 Unlimited retry (không giới hạn 5 lần)
- 🔄 2 format dialogue (tương thích ngược)
- 🔄 Manual test từng ảnh
- 🔄 Script editing trước khi tạo

---

## 13. LIÊN HỆ & HỖ TRỢ

**Nếu cần hỗ trợ:**

1. **Check Troubleshooting section** (Mục 10)
2. **Google error message**
3. **Check Gemini API status:** https://status.cloud.google.com/

**Tài liệu tham khảo:**
- Gemini API: https://ai.google.dev/gemini-api/docs
- Pillow: https://pillow.readthedocs.io/
- Python: https://docs.python.org/3/

---

## 14. APPENDIX

### A. Cấu trúc thư mục đầy đủ

```
C:\CodeRac\
├── quoc_khanh_comic_generator.py      # Script chính (1572 dòng) - v1.1.0
├── arial.ttf                           # Font chữ (optional)
├── arialbd.ttf                         # Font chữ bold (optional)
├── .conda\                             # Môi trường Python
│   ├── python.exe
│   └── Lib\
├── PROMPTS_TONG_QUAN_QUOC_KHANH.txt   # Prompts tổng quan (auto-gen)
├── story_script_TEMP.json              # Kịch bản tạm (auto-gen)
├── panel_images\                       # Ảnh panels (auto-gen)
│   ├── page_0_panel_1.png
│   ├── page_0_panel_2.png
│   └── ...
└── final_comic\                        # Output cuối (auto-gen)
    ├── page_0.png
    ├── page_1.png
    ├── ...
    └── QUOC_KHANH_80_NAM.pdf          # 🎯 KẾT QUẢ CUỐI
```

### B. Requirements.txt

```txt
google-generativeai>=0.8.3
Pillow>=10.0.0
requests>=2.31.0
```

**Cài tất cả:**
```bash
pip install -r requirements.txt
```

### C. .gitignore

```gitignore
# Python
__pycache__/
*.py[cod]
.venv/
.conda/

# Output
panel_images/
final_comic/
*.png
*.pdf
*.txt

# Config
.env
*.json

# OS
.DS_Store
Thumbs.db
```

### D. ENV Template (.env.example)

```
# Gemini API Key
GEMINI_API_KEY=your_api_key_here

# Optional: Custom settings
PAGE_WIDTH=2100
PAGE_HEIGHT=2970
OUTPUT_DIR=final_comic
```

---

## ✅ KẾT LUẬN

Tài liệu này cung cấp **đầy đủ thông tin** để:

1. ✅ **Hiểu rõ code** - Kiến trúc, logic, workflow
2. ✅ **Build trên máy mới** - Chi tiết từng bước
3. ✅ **Debug lỗi** - Troubleshooting đầy đủ (12 lỗi phổ biến)
4. ✅ **Tùy chỉnh** - Best practices, tips & tricks
5. ✅ **Maintain** - Changelog, version history
6. ✅ **Sử dụng tính năng mới** - Bubble position editor (v1.1.0)

**Đảm bảo:** Code build trên máy mới sẽ **chạy đúng chuẩn**, **không mất chức năng**.

**Phiên bản hiện tại:** v1.1.0 (24/10/2025)

**Tính năng nổi bật v1.1.0:**
- ✨ Chỉnh sửa vị trí textbox trực tiếp với menu 'e'
- ✨ 9 vị trí có sẵn với emoji trực quan
- ✨ Vẽ lại ngay lập tức, không cần tạo ảnh mới
- ✨ Fix lỗi IndexError khi số trang không khớp

---

**📝 Tài liệu này được tạo bởi AI Assistant**  
**🗓️ Ngày: 24/10/2025**  
**🇻🇳 Chủ đề: Kỷ niệm 80 năm Quốc khánh Việt Nam**  
**📌 Version: 1.1.0 - Bubble Position Editor Update**
