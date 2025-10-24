#!/usr/bin/env python3
"""
🔥 Multi-scene Vietnamese news video generator using Veo via LiteLLM Proxy.

Features:
- Generate 4 sequential scenes (prompts below)
- Retry & cooldown logic for reliability
- Auto-download from LiteLLM proxy
- Combine scenes into one final MP4 video

Author: Phúc & ChatGPT (2025)
"""

import os
import json
import time
import requests
from typing import Optional
from moviepy import VideoFileClip, concatenate_videoclips


# ===============================================================
#  CLASS: VeoVideoGenerator (using LiteLLM proxy)
# ===============================================================
class VeoVideoGenerator:
    def __init__(self, base_url: str = "https://api.thucchien.ai/gemini/v1beta",
                 api_key: str = "sk-VWZxoX1d8ZY4cF4eTTyLWQ"):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            "x-goog-api-key": api_key,
            "Content-Type": "application/json"
        }

    # ----------------------
    # 1️⃣ Generate a video
    # ----------------------
    def generate_video(self, prompt: str) -> Optional[str]:
        print(f"🎬 Starting generation for: {prompt[:60]}...")
        url = f"{self.base_url}/models/veo-3.0-generate-preview:predictLongRunning"
        payload = {"instances": [{"prompt": prompt}]}

        try:
            r = requests.post(url, headers=self.headers, json=payload)
            r.raise_for_status()
            data = r.json()
            op_name = data.get("name")
            if op_name:
                print(f"✅ Operation started: {op_name}")
                return op_name
            else:
                print("❌ No operation name returned:", json.dumps(data, indent=2))
                return None
        except requests.RequestException as e:
            print(f"❌ Failed to start generation: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(e.response.text)
            return None

    # ----------------------
    # 2️⃣ Poll for completion
    # ----------------------
    def wait_for_completion(self, op_name: str, max_wait=900) -> Optional[str]:
        op_url = f"{self.base_url}/{op_name}"
        start = time.time()
        while time.time() - start < max_wait:
            try:
                r = requests.get(op_url, headers=self.headers)
                r.raise_for_status()
                data = r.json()

                if "error" in data:
                    print("❌ Error:", data["error"])
                    return None

                if data.get("done"):
                    try:
                        uri = data["response"]["generateVideoResponse"]["generatedSamples"][0]["video"]["uri"]
                        print(f"🎥 Video ready: {uri}")
                        return uri
                    except KeyError:
                        print("❌ Could not parse video URI:", json.dumps(data, indent=2))
                        return None

                print("⏳ Still processing... waiting 20s")
                time.sleep(20)
            except Exception as e:
                print(f"⚠️ Poll error: {e}")
                time.sleep(30)
        print("⏰ Timeout waiting for video.")
        return None

    # ----------------------
    # 3️⃣ Download result
    # ----------------------
    def download_video(self, video_uri: str, output_filename: str) -> bool:
        print(f"⬇️ Downloading {output_filename}...")
        if video_uri.startswith("https://generativelanguage.googleapis.com/"):
            relative = video_uri.replace("https://generativelanguage.googleapis.com/", "")
        else:
            relative = video_uri

        dl_url = self.base_url.replace("/v1beta", "/download") + "/" + relative

        try:
            r = requests.get(dl_url, headers=self.headers, stream=True, allow_redirects=True)
            r.raise_for_status()

            total = 0
            with open(output_filename, "wb") as f:
                for chunk in r.iter_content(8192):
                    if chunk:
                        f.write(chunk)
                        total += len(chunk)
                        if total % (1024 * 1024) == 0:
                            print(f"📦 Downloaded {total / (1024*1024):.1f} MB...")

            if os.path.getsize(output_filename) < 100_000:
                print("⚠️ File too small, may be corrupted.")
                return False
            print(f"✅ Saved to {output_filename} ({os.path.getsize(output_filename)/1e6:.2f} MB)")
            return True
        except Exception as e:
            print(f"❌ Download failed: {e}")
            return False

    # ----------------------
    # 4️⃣ Generate + download wrapper
    # ----------------------
    def generate_and_download(self, prompt: str, filename: str) -> bool:
        op = self.generate_video(prompt)
        if not op:
            return False

        uri = self.wait_for_completion(op)
        if not uri:
            return False

        return self.download_video(uri, filename)


# ===============================================================
#  MAIN PROGRAM
# ===============================================================
def main():
    generator = VeoVideoGenerator()

    scenes = [
        {
            "name": "scene_1",
            "prompt": """
            A photorealistic, ultra-high-definition (4K) video of a female news anchor in a modern TV news studio.
            Visuals: Vietnamese woman in her 30s wearing navy blue blazer, white blouse, behind a news desk with the logo "Bản tin Xanh 24h".
            Audio: "Xin kính chào quý vị khán giả! Quý vị đang theo dõi Bản tin Xanh 24h. Hôm nay, chúng ta cùng nhìn lại những diễn biến đáng chú ý về tình hình cháy rừng trong thời gian qua — một vấn đề đang gióng lên hồi chuông cảnh báo toàn cầu."
            """
        },
        {
            "name": "scene_2",
            "prompt": """
            A professional Vietnamese female news anchor continues reporting. The background screen transitions to a world map with animated fire icons over Vietnam, Canada, and Greece. 4K, hyper-realistic, news broadcast style.
            Audio: "Những đám cháy này không chỉ tàn phá hệ sinh thái, mà còn gây thiệt hại nghiêm trọng cho đời sống con người."
            """
        },
        {
            "name": "scene_3",
            "prompt": """
            Dramatic aerial drone footage of a massive forest fire in Vietnam's Central Highlands. Thick plumes of smoke rise from lush green mountains being consumed by orange flames. 4K cinematic style.
            Audio: "Các chuyên gia cảnh báo rằng nếu không có biện pháp bảo vệ, các khu rừng sẽ tiếp tục bị tàn phá."
            """
        },
        {
            "name": "scene_4",
            "prompt": """
            An expansive aerial shot of a large Indonesian city almost completely obscured by a thick, oppressive blanket of orange haze and smoke from nearby forest fires. 4K, hyper-realistic, impactful.

            """
        },
        {
            "name": "scene_5",
            "prompt": """
            A fast-paced montage of global wildfires. First, a shot of a massive forest fire on the outskirts of a Canadian city. Second, a fire raging on a hillside near the Mediterranean coast in Greece. Dynamic editing, 4K, news report style.
            """
        },
        {
            "name": "scene_6",
            "prompt": """
            Final shot of the Vietnamese female news anchor at her desk. She offers a slight, professional nod to the camera as she concludes the report. The background screen transitions to display the official logo of the news channel. 4K, hyper-realistic, news broadcast style.
            Audio: "Chúng ta cùng nhau chúc mừng các hoạt động chính kỷ niệm 80 năm Quốc khánh 2/9 vào ngày 2 tháng 9 năm 2025."
            """
        }
    ]

    generated_files = []

    for i, s in enumerate(scenes, 1):
        print(f"\n🚀 Scene {i}/{len(scenes)} — {s['name']}")
        retries = 0
        success = False

        while not success and retries < 3:
            success = generator.generate_and_download(s["prompt"], f"{s['name']}.mp4")
            if not success:
                retries += 1
                print(f"⚠️ Retry {retries}/3 after 60s...")
                time.sleep(60)

        if success:
            generated_files.append(f"{s['name']}.mp4")
        print("😴 Cooling down before next scene (120s)...\n")
        time.sleep(120)

    # ===================================================
    #  Combine all scenes into one final news video
    # ===================================================
    if generated_files:
        print("🎞 Combining scenes...")
        clips = [VideoFileClip(v) for v in generated_files if os.path.exists(v)]
        final = concatenate_videoclips(clips, method="compose")
        final.write_videofile("final_news.mp4", codec="libx264", audio_codec="aac", fps=30)
        print("✅ Final combined video saved as final_news.mp4")
    else:
        print("❌ No valid videos to combine.")


if __name__ == "__main__":
    main()
