from fastapi import FastAPI, File, UploadFile, Form
from time import sleep
import uvicorn
import subprocess
import json
import os
import requests
import shutil
from pydantic import BaseModel
import os
from pathlib import Path
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

app = FastAPI()

class UserSize(BaseModel):
    chestSize: float
    hipSize: float
    shoulderSize: float
    waistSize: float

class UserBodySizeRequestDto(BaseModel):
    userId: int
    userSize: UserSize
#루트경로
BASE_DIR = Path(__file__).resolve().parent
parent_dir = BASE_DIR.parent
#이미지 저장 경로
images_dir = BASE_DIR / "data/images"
keypoints_dir = BASE_DIR / "data/keypoints"
smplify_results_dir = BASE_DIR / "data/smplify_results"

# 가상환경 경로 설정
envs = {
    "openpose": "openpose",
    "smplifyx": "smplifyx",
    "obj2json": "smpla"
}

def run_command(command, env_name):
    #shell_script = "/Users/vecherish/Desktop/gradsmu/smplifyx/scripts/run_in_script.sh"  # 셸 스크립트 경로
    shell_script = parent_dir / "scripts/run_in_script.sh"
    full_command = f"bash {shell_script} {env_name} {command}"
    print(f"Running in environment: {env_name}")
    process = subprocess.Popen(full_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout, stderr

def delete_all_subfolders(base_dir):
    for folder in ["images", "meshes", "results","meshes_png"]:
        folder_path = os.path.join(base_dir, folder)
        if os.path.exists(folder_path):
            for subfolder in os.listdir(folder_path):
                subfolder_path = os.path.join(folder_path, subfolder)
                if os.path.isdir(subfolder_path):
                    shutil.rmtree(subfolder_path)

@app.post("/process")
async def process_image(userId: int = Form(...), file: UploadFile = File(...)):
    #파일 저장
    #file_location = f"/Users/vecherish/Desktop/gradsmu/smplifyx/content/data/images/{file.filename}"
    file_location = images_dir / file.filename
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)
        # 1. OpenPose 실행
    openpose_command = f"python scripts/openpose_script.py"
    openpose_stdout, openpose_stderr = run_command(openpose_command, envs["openpose"])

    print("OpenPose stdout:", openpose_stdout.decode())
    print("OpenPose stderr:", openpose_stderr.decode())
    #키포인트 파일 경로
    #keypoints_file = f"/Users/vecherish/Desktop/gradsmu/smplifyx/content/data/keypoints/{file.filename.replace('.jpg','')}_keypoints.json"
    keypoints_file = keypoints_dir / f"{file.filename.replace('.png','')}_keypoints.json"
    # 2. SMPLify 실행
    smplify_command = f"python scripts/smplify_script.py"
    smplify_stdout, smplify_stderr = run_command(smplify_command, envs["smplifyx"])

    #결과 obj 파일 경로
    #obj_file = f"/Users/vecherish/Desktop/gradsmu/smplifyx/content/data/smplify_results/meshes/{file.filename.replace('.jpg', '')}/000.obj"
    #obj_dir = f"/Users/vecherish/Desktop/gradsmu/smplifyx/content/data/smplify_results/meshes/{file.filename.replace('.jpg', '')}"
    # 결과 obj 파일 경로
    obj_file = smplify_results_dir / "meshes" / file.filename.replace('.png', '') / "000.obj"
    obj_dir = smplify_results_dir / "meshes" / file.filename.replace('.png', '')
    if not obj_file.exists():
    # 파일이 없을 경우 에러 메시지 반환
        return {"error": f"OBJ file not found: {obj_file}"}
    # 3. OBJ to JSON 변환
    obj2json_command = f"python scripts/obj2json_script.py --obj {obj_file}"
    obj2json_stdout, obj2json_stderr = run_command(obj2json_command, envs["obj2json"])
    print("obj2json stdout:", obj2json_stdout.decode())
    print("obj2json stderr:", obj2json_stderr.decode())

    #stdout으로부터 JSON 데이터를 파싱
    obj2json_output = obj2json_stdout.decode()

    json_data = json.loads(obj2json_output)

    # 후에 모델로 변환
    user_size = UserSize(**json_data)
    user_body_size_request_dto = UserBodySizeRequestDto(userId=userId, userSize=user_size)

    response_data = user_body_size_request_dto.json()
    print(response_data)
    #obj.png file
    obj_png= "/root/smplifyx/content/data/smplify_results/meshes_png/000.png"
    #obj_png = smplify_results_dir / "meshes_png" / "000.png"
    obj_file_name = f"obj{userId}.png"
    multipart_data = {
        "json":(None,response_data,"application/json"),
        "file":(obj_file_name,open(obj_png,'rb'),"image/png")
    }
    #전송
    retry_strategy = Retry(
        total = 30,
        status_forcelist=[429, 500, 502, 503, 504]
    )

    session = requests.Session()
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    session.headers.update({'Connection': 'keep-alive'})

    #custom_headers = {
     #'Content-Type': 'multipart/form-data'
    #}   
    url = "https://fittingpair.store/get/json"
    multipart_response = session.post(
        url,  # Spring 서버의 엔드포인트 URL
        files=multipart_data,  # 전송할 파일 데이
    )

    #원본 이미지와 임시 파일 삭제
    os.remove(file_location)
    os.remove(keypoints_file)
    delete_all_subfolders(smplify_results_dir)

    if multipart_response.status_code == 200:
        return {"status_code": multipart_response.status_code, "message": "Data sent successfully"}
    else:
        return {"status_code": multipart_response.status_code, "message": "Failed to send data"}

@app.post("/send-test-data")
def send_test_data():
    url = "http://175.113.68.69:5900/get/json"  # 스프링 서버의 엔드포인트 URL
    data = {"message": "Hello from FastAPI!"}  # 테스트 데이터
    retry_strategy = Retry(
        total = 30,
        status_forcelist=[429, 500, 502, 503, 504]
    )

    session = requests.Session()
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    session.headers.update({'Connection': 'keep-alive'})

    custom_headers = {
     'Content-Type': 'application/json'
    }

    sleep(6)
    try:
        multipart_response = session.post(
            url,  # Spring 서버의 엔드포인트 URL
            json= data,
            headers=custom_headers)
        return {"status_code": response.status_code, "response_text": response.text}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
