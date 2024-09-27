import sys,os
import argparse
import json

# 모듈 경로 추가
module_path = "/root/smplifyx/content/SMPL-Anthropometry"
if module_path not in sys.path:
    sys.path.append(module_path)
# 작업 디렉토리 변경
os.chdir(module_path)
# 모듈 임포트
from measure import generate_json
from measurement_definitions import SMPLXMeasurementDefinitions, STANDARD_LABELS
def main(obj_path):
    # OBJ to JSON 변환 명령어 실행
    json_data = generate_json(obj_path)
    print(json.dumps(json_data))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OBJ to JSON Script")
    parser.add_argument('--obj', type=str, required=True, help="Path to the OBJ file")
    args = parser.parse_args()
    main(args.obj)
