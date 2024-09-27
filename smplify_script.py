import subprocess
import argparse
  
def main():
    # SMPLify 명령어 실행
    command = (
        f"xvfb-run -a -s \"-screen 0 1024x768x24\" "
        f"python3 smplifyx/main.py --config cfg_files/fit_smplx.yaml "
        f"--data_folder /root/smplifyx/content/data "
        f"--output_folder /root/smplifyx/content/data/smplify_results "
        f"--visualize True "
        f"--gender neutral "
        f"--model_folder /root/smplifyx/content/SMPL-Anthropometry/data "
        f"--vposer_ckpt /root/smplifyx/content/SMPL-Anthropometry/data/vposer/V02_05 "
        f"--part_segm_fn smplx_parts_segm.pkl"
    )
    working_directory = "/root/smplifyx/content/Smplify-X-Perfect-Implementation"
    process = subprocess.Popen(command, shell=True, cwd=working_directory, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    print("SMPLify stdout:", stdout.decode())
    print("SMPLify stderr:", stderr.decode())
          
if __name__ == "__main__":
    #parser = argparse.ArgumentParser(description="SMPLify Script")
    #parser.add_argument('--keypoints', type=str, required=True, help="Path to the keypoints file") 
    #parser.add_argument('--image_name', type=str, required=True, help="Name of the image file")
    main()
