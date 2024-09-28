import sys,os
import argparse
import json
import numpy as np
# 모듈 경로 추가
module_path = "/home/aoa8432/smplifyx/content/SMPL-Anthropometry"
if module_path not in sys.path:
    sys.path.append(module_path)
# 작업 디렉토리 변경
os.chdir(module_path)
# 모듈 임포트
from measure import generate_json
from measurement_definitions import SMPLXMeasurementDefinitions, STANDARD_LABELS

def convert_to_serializable(data):
    if isinstance(data, np.float32):
        return float(data)
    elif isinstance(data, dict):
        return {k: convert_to_serializable(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_to_serializable(i) for i in data]
    else:
        return data
        
def main(obj_path):
    json_data = generate_json(obj_path)
    serializable_data = convert_to_serializable(json_data)
    print(json.dumps(serializable_data))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OBJ to JSON Script")
    parser.add_argument('--obj', type=str, required=True, help="Path to the OBJ file")
    args = parser.parse_args()
    main(args.obj)
