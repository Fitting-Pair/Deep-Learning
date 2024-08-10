import subprocess
import argparse

def main():
    # 오픈포즈 명령어 실행
    command = (
        f"./build/examples/openpose/openpose.bin --image_dir /Users/vecherish/Desktop/gradsmu/smplifyx/content/data/images "
        f"--write_json /Users/vecherish/Desktop/gradsmu/smplifyx/content/data/keypoints "
        f"--face --hand --display 0 "
        f"--render_pose 0"
        #f"--write_images /Users/vecherish/Desktop/gradsmu/smplifyx/content/openpose_images"
    )
    working_directory = "/Users/vecherish/Desktop/gradsmu/smplifyx/content/openpose-with-caffe-for-MacM1"
    process = subprocess.Popen(command, shell=True, cwd=working_directory, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    # print("OpenPose stdout:", stdout.decode())
    # print("OpenPose stderr:", stderr.decode())


if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description="OpenPose Script")
    # parser.add_argument('--image_path', type=str, required=True, help="Path to the image")
    # args = parser.parse_args()
    main()
