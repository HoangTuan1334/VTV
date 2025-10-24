import json
import re
from openai import OpenAI

# --- Cấu hình ---
# Thay API key của bạn vào đây nếu cần
client = OpenAI(
  api_key="",
  base_url="https://api.thucchien.ai"
)

# Prompt để sinh kịch bản (giữ nguyên như của bạn)
prompt = """
Context: You are a professional scriptwriter specializing in scripts for technology news programs on television. You have been tasked with creating a detailed script for a short news video, aiming to disseminate knowledge about AI in an engaging and professional manner.
Task: Create a complete video script titled "Vietnam 2025: Breakthroughs in the AI Era". The script must strictly adhere to the following requirements:
1. Main Theme: Summarize and analyze the key highlights of AI development in Vietnam, updated to October 2025.
2. Script Structure: The script must be divided into clear scenes. Each scene must include four elements:
Timestamp: Allocate time for each scene.
Visual: Describe in detail what will appear on the screen, including shots of the virtual host, graphics, charts, and AI-generated illustrative images. These descriptions must be detailed enough to serve as prompts for an AI image/video generation model.
Voiceover: The exact narration for the virtual host, with a formal, inspiring, and clear tone.
Sound: Suggestions for background music or sound effects.
3. Detailed Product Requirements:
Video Duration: 60 to 80 seconds.
Virtual Host: A professional-looking male/female virtual host, appearing in a modern virtual studio.
AI Voice: Standard, expressive Vietnamese narration, free of pronunciation errors. (Note: The voiceover text will be provided in English, assuming it will be translated to Vietnamese for the final AI voice).
Visual Content:
Illustrative images must be AI-generated, high-quality, and relevant to the content (e.g., robots in a factory, an AI doctor, smart agriculture).
Use charts and infographics to visualize data (e.g., growth rates, investment in AI).
The video design must have a clear title, professional layout, and be easy to follow.
Mandatory Content: The video must contain the sentence: "This is a submission for the AI Thuc Chien Contest." at the end.
Style: The content must be accurate, concise, engaging, and aimed at a general audience.
Language: Vietnamese (The script below is in English for generation purposes and should be translated for the final product).

4. Quan trong:
**Nội dung kết thúc bắt buộc**: Cảnh cuối cùng của video phải kết thúc bằng câu thoại chính xác là: **"Đây là sản phẩm tham dự cuộc thi AI Thực Chiến."**

**Chủ đề chính**: Tổng hợp và phân tích những điểm nhấn quan trọng trong sự phát triển AI tại Việt Nam, cập nhật đến tháng 10 năm 2025.
**Ngôn ngữ**: Toàn bộ nội dung kịch bản, đặc biệt là phần lời thoại (Voiceover), phải được viết hoàn toàn bằng **Tiếng Việt**.
**Phong cách**: Kịch bản phải mang đậm chất thời sự, đưa tin, với lời thoại trang trọng, rõ ràng và mạch lạc như một bản tin truyền hình thực thụ.
**Nội dung kết thúc bắt buộc**: Cảnh cuối cùng của video phải kết thúc bằng câu thoại chính xác là: **"Đây là sản phẩm tham dự cuộc thi AI Thực Chiến."**
Begin Script:

**[SCENE 1]**
*   **Timestamp:** 00:00 - 00:05 (5 giây)
*   **Visual Prompt:** Intro animation 3D hoành tráng. Logo chương trình công nghệ hiện ra từ những dòng chảy dữ liệu và mạng neuron nhân tạo phát sáng. Dòng tiêu đề hiện ra: **"Việt Nam 2025: Những bước tiến đột phá trong kỷ nguyên Trí tuệ Nhân tạo"**. Phong cách hiện đại, tốc độ nhanh.
*   **Voiceover:** (Không có)
*   **Sound:** Nhạc hiệu chương trình, âm thanh điện tử mạnh mẽ, dồn dập.

**[SCENE 2] - Lần xuất hiện đầu tiên của MC**
*   **Timestamp:** 00:05 - 00:13 (8 giây)
*   **Visual Prompt:** **[Prompt Gốc cho MC]** Trung cảnh (Medium shot) một MC ảo nữ, khoảng 30 tuổi, tên "Minh Anh". Khuôn mặt thanh tú, thông minh, mái tóc đen ngang vai được tạo kiểu chuyên nghiệp. Cô mặc một bộ vest công sở màu xanh navy hiện đại và áo sơ mi trắng. Cô đứng trong một phim trường ảo công nghệ cao với các màn hình hiển thị dữ liệu mờ ảo phía sau. Ánh sáng chuyên nghiệp. Cô nhìn thẳng vào camera với nụ cười thân thiện và phong thái tự tin.
*   **Voiceover:** "Kính chào quý vị khán giả. Năm 2025 đã đánh dấu một bước chuyển mình mạnh mẽ của Việt Nam trên bản đồ công nghệ toàn cầu."
*   **Sound:** Nhạc nền tin tức bắt đầu nổi lên, tiết tấu vừa phải.

**[SCENE 3]**
*   **Timestamp:** 00:13 - 00:21 (8 giây)
*   **Visual Prompt:** **[Prompt Hành Động]** Góc máy giữ nguyên. MC Minh Anh đưa tay sang phải, chỉ vào một không gian trống bên cạnh. Biểu cảm của cô trở nên hứng khởi hơn.
*   **Voiceover:** "Với chiến lược quốc gia về Trí tuệ Nhân tạo, chúng ta đã chứng kiến những thành tựu vượt bậc..."
*   **Sound:** Nhạc nền tiếp tục.

**[SCENE 4]**
*   **Timestamp:** 00:21 - 00:29 (8 giây)
*   **Visual Prompt:** Đồ họa chuyển động (Motion graphics) hiện ra đúng vị trí tay MC chỉ. Bản đồ Việt Nam 3D phát sáng, với các điểm sáng kết nối các trung tâm AI lớn (Hà Nội, Đà Nẵng, TP.HCM) bằng các luồng dữ liệu.
*   **Voiceover:** "...biến AI trở thành động lực cốt lõi cho sự phát triển kinh tế - xã hội."
*   **Sound:** Hiệu ứng âm thanh "swoosh" nhẹ khi đồ họa xuất hiện.

**[SCENE 5]**
*   **Timestamp:** 00:29 - 00:37 (8 giây)
*   **Visual Prompt:** **[Prompt Hành Động]** Cắt cảnh trở lại MC Minh Anh. Giờ là cận cảnh (Close-up shot), cô nhìn thẳng vào ống kính với ánh mắt quả quyết. Phông nền phía sau mờ đi, tập trung vào biểu cảm của cô.
*   **Voiceover:** "AI không còn là lý thuyết, mà đã hiện diện trong mọi mặt của cuộc sống. Hãy cùng điểm qua những ứng dụng nổi bật."
*   **Sound:** Nhạc nền tăng tiết tấu một chút, tạo sự tò mò.

**[SCENE 6]**
*   **Timestamp:** 00:37 - 00:45 (8 giây)
*   **Visual Prompt:** Cảnh quay điện ảnh, hyper-realistic. Một bác sĩ đang xem phim X-quang trên màn hình kỹ thuật số. Giao diện AI bên cạnh hiển thị các vùng được khoanh đỏ, chẩn đoán ung thư sớm với độ chính xác cao. Góc máy quay từ sau vai bác sĩ, tập trung vào màn hình.
*   **Voiceover:** "Trong y tế, AI đang hỗ trợ chẩn đoán bệnh, mang lại hy vọng cho hàng triệu người."
*   **Sound:** Nhạc nền sâu lắng, truyền cảm hứng. Hiệu ứng "bíp" nhẹ của máy móc y tế.

**[SCENE 7]**
*   **Timestamp:** 00:45 - 00:53 (8 giây)
*   **Visual Prompt:** Flycam shot, hyper-realistic. Một cánh đồng lúa rộng lớn của Việt Nam được giám sát bởi các drone nông nghiệp thông minh. Drone đang phun tưới chính xác vào những khu vực cần thiết. Màu sắc tươi sáng, sống động.
*   **Voiceover:** "Trong nông nghiệp, AI giúp tối ưu hóa năng suất và phát triển bền vững."
*   **Sound:** Nhạc nền trở nên tươi vui, lạc quan hơn. Tiếng gió và tiếng drone hoạt động nhẹ.

**[SCENE 8]**
*   **Timestamp:** 00:53 - 01:01 (8 giây)
*   **Visual Prompt:** Cảnh quay trong một nhà máy sản xuất ô tô hiện đại, hyper-realistic. Các cánh tay robot đang lắp ráp linh kiện một cách nhanh chóng và chính xác, tia lửa hàn tóe ra. Mọi thứ hoàn toàn tự động.
*   **Voiceover:** "Và trong sản xuất, tự động hóa đang tái định hình nền công nghiệp quốc gia."
*   **Sound:** Âm thanh công nghiệp mạnh mẽ (tiếng máy móc, kim loại).

**[SCENE 9]**
*   **Timestamp:** 01:01 - 01:09 (8 giây)
*   **Visual Prompt:** **[Prompt Hành Động]** Quay trở lại trung cảnh MC Minh Anh. Cô đi một bước nhỏ về phía trước, hai tay đan lại. Vẻ mặt trở nên nghiêm túc hơn một chút. Phía sau cô, đồ họa chữ "THÁCH THỨC" hiện ra.
*   **Voiceover:** "Tuy nhiên, tương lai cũng đi kèm với những thách thức về an ninh mạng và đào tạo nhân lực."
*   **Sound:** Nhạc nền chuyển sang giai điệu trầm hơn, mang tính suy ngẫm.

**[SCENE 10]**
*   **Timestamp:** 01:09 - 01:17 (8 giây)
*   **Visual Prompt:** **[Prompt Hành Động]** Cận cảnh MC Minh Anh, cô ngẩng cao đầu và nở nụ cười tự tin trở lại. Ánh mắt đầy hy vọng.
*   **Voiceover:** "Nhưng với khát vọng và trí tuệ Việt, chúng ta đang vững bước chinh phục công nghệ."
*   **Sound:** Nhạc nền trở nên hào hùng, mạnh mẽ.

**[SCENE 11] - Cảnh kết**
*   **Timestamp:** 01:17 - 01:25 (8 giây)
*   **Visual Prompt:** Màn hình kết thúc (Outro card). Logo chương trình hiện ra cùng dòng chữ lớn: **"AI - Trí tuệ Việt Nam, Vươn tầm thế giới"**. Bên dưới là dòng chữ nhỏ hơn: **"Đây là sản phẩm tham dự cuộc thi AI Thực Chiến."**
*   **Voiceover:** "Cảm ơn quý vị đã theo dõi."
*   **Sound:** Nhạc hiệu chương trình nổi lên đỉnh điểm rồi tắt dần.
"""

def parse_script_to_structured_json(script_text):
    """
    Hàm này phân tích văn bản kịch bản thô thành một đối tượng JSON có cấu trúc.
    """
    try:
        title_search = re.search(r'titled "([^"]+)"', script_text)
        script_title = title_search.group(1) if title_search else "Untitled Script"

        scenes = []
        # Tách kịch bản thành các cảnh dựa trên định dạng [timestamp] - TITLE
        scene_blocks = re.split(r'(?=\[\d{2}:\d{2}\s*-\s*\d{2}:\d{2}\])', script_text)

        for block in scene_blocks:
            if not block.strip():
                continue

            # Tách header (timestamp, title) và nội dung (visual, voiceover, sound)
            parts = re.split(r'\n', block, 1)
            header = parts[0]
            content = parts[1] if len(parts) > 1 else ""

            header_match = re.match(r'(\[.*?\])\s*-\s*(.*)', header)
            if not header_match:
                continue

            scene_obj = {
                "timestamp": header_match.group(1).strip(),
                "scene_title": header_match.group(2).strip()
            }

            # Tách các phần con
            visual_search = re.search(r'Visual:(.*?)(?:Voiceover:|Sound:|$)', content, re.DOTALL)
            voiceover_search = re.search(r'Voiceover:(.*?)(?:Sound:|$)', content, re.DOTALL)
            sound_search = re.search(r'Sound:(.*)', content, re.DOTALL)

            scene_obj["visual"] = visual_search.group(1).strip() if visual_search else ""
            scene_obj["Voiceover"] = voiceover_search.group(1).strip() if voiceover_search else ""
            scene_obj["Sound"] = sound_search.group(1).strip() if sound_search else ""
            
            scenes.append(scene_obj)
        
        return {"title": script_title, "scenes": scenes}

    except Exception as e:
        print(f"Lỗi khi phân tích kịch bản: {e}")
        return None

# --- Thực thi ---
print("Đang tạo kịch bản từ AI...")
response = client.chat.completions.create(
  model="gemini-2.5-pro", # Chọn model bạn muốn
  messages=[
      {
          "role": "user",
          "content": prompt 
      }
  ]
)

# Lấy nội dung kịch bản từ phản hồi
generated_script_text = response.choices[0].message.content
print("--- KỊCH BẢN GỐC TỪ AI ---")
print(generated_script_text)
print("---------------------------\n")


# Phân tích kịch bản thành cấu trúc JSON
print("Đang phân tích kịch bản thành JSON...")
structured_script = parse_script_to_structured_json(generated_script_text)

# Lưu kết quả vào file JSON
if structured_script:
    file_path = "script.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(structured_script, f, ensure_ascii=False, indent=2)
    print(f"Đã lưu kịch bản có cấu trúc vào file: {file_path}")
else:
    print("Không thể lưu file JSON do lỗi phân tích.")