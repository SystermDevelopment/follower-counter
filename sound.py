"""
このモジュールは Linux 環境で効果音を再生するための関数を提供します。
amixer と aplay に依存しています。
"""

from pathlib import Path
import subprocess

def play_increase_sound(sound_path: str = "./asset/success.wav", volume: int = 100):
    if not (0 <= volume <= 100):
        print(f"音量値エラー: {volume}（0〜100の範囲で指定してください）")
        return
    
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