from pathlib import Path
import subprocess

def play_increase_sound(sound_path="./asset/success.wav", volume=100):
    if Path(sound_path).exists():
        try:
            # 音量設定（出力抑制）
            subprocess.run(["amixer", "sset", "Master", f"{volume}%"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            # 音声再生（出力抑制）
            subprocess.run(
                ["aplay", sound_path],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except Exception as e:
            print(f"再生エラー: {e}")
    else:
        print(f"ファイルが存在しません: {sound_path}")