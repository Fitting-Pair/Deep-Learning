import subprocess
import argparse

def main():
    # 오픈포즈 명령어 실행
    command = (
        f"./examples/openpose/openpose.bin --image_dir /root/smplifyx/content/data/images "
        f"--write_json /root/smplifyx/content/data/keypoints "
        f"--face --hand --display 0 "
        f"--render_pose 0 "
        f"--model_pose BODY_25 "
        f"--net_resolution 320x176 "
        f"--face_net_resolution 320x320 "
        #f"--write_images /Users/vecherish/Desktop/gradsmu/smplifyx/content/openpose_images"
    )
    working_directory = "/root/smplifyx/content/openpose"
    process = subprocess.Popen(command, shell=True, cwd=working_directory, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    print("OpenPose stdout:", stdout.decode())
    print("OpenPose stderr:", stderr.decode())


if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description="OpenPose Script")
    # parser.add_argument('--image_path', type=str, required=True, help="Path to the image")
    # args = parser.parse_args()
    main()
