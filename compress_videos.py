import os
import subprocess

def compress_videos(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.mp4'):
                input_path = os.path.join(root, file)
                temp_output = os.path.join(root, "temp_" + file)
                
                print(f"Compressing {input_path}...")
                
                # ffmpeg -i input.mp4 -vf scale=640:-1 -t 8 output.mp4
                cmd = [
                    'ffmpeg', '-y', '-i', input_path, 
                    '-vf', 'scale=640:-1', 
                    '-t', '8', 
                    temp_output
                ]
                
                try:
                    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    os.replace(temp_output, input_path)
                    print(f"✅ Successfully compressed {file}")
                except subprocess.CalledProcessError as e:
                    print(f"❌ Failed to compress {file}: {e}")
                    if os.path.exists(temp_output):
                        os.remove(temp_output)

if __name__ == "__main__":
    compress_videos("data")
