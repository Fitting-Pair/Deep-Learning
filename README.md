# Deep-Learning
딥러닝 서버 레포지토리입니다.

## Anaconda 환경 세팅 및 프로젝트 초기화

### 1. Anaconda 설치

Anaconda를 설치한 후, 아래 단계를 따라 OpenPose와 SMPLify-X 환경을 설정합니다.

### 2. OpenPose 환경 설정

OpenPose와 관련된 환경을 먼저 설정합니다. SMPLify-X와의 Python 버전 및 라이브러리 호환성 문제를 방지하기 위해서 따로 설정합니다.

#### 2.1. OpenPose 환경 생성 및 설정

```bash
conda create -n openpose python=3.9
conda activate openpose
conda openpose create --file openpose.yaml
```
#### 2.2. OpenPose 설치 및 설정
Colab에서 제공된 코드를 참조하여 OpenPose를 설치 및 설정합니다. 다음 링크에서 설치 가이드를 참고합니다.
https://colab.research.google.com/drive/1OoGEg8doFA3-3f_5XkA895C9xR9nf-ob?usp=sharing#scrollTo=1AL4QpsBUO9p
#### 2.3. OpenPose 테스트
OpenPose가 제대로 설치되었는지 테스트하려면 다음 명령어를 사용합니다:
```bash
./build/examples/openpose/openpose.bin
```
### 3. SMPLify-X 환경 설정
OpenPose 환경 설정이 완료된 후, SMPLify-X 환경을 설정합니다.
```bash
conda create -n openpose python=3.9
conda activate openpose
conda smplifyx create --file smplifyx.yaml
```
#### 3-1. 필요한 라이브러리 설치
```bash
cd /content
pip install chumpy
pip install smplx
```
#### 3-2. smplx 설치
```bash
git clone https://github.com/vchoutas/smplx
cd smplx
python setup.py install
```
#### 3-3. Configer 및 human_body_prior 설치
```bash
pip install git+https://github.com/nghorbani/configer

git clone https://github.com/nghorbani/human_body_prior
cd human_body_prior
python setup.py develop
pip install -r requirements.txt
```
#### 3-4. 프로젝트 설정
```bash
cd Smplify-X-Perfect-Implementation
pip install -r requirements.txt
```
### 4. SMPL Anthropometry 설치 
https://github.com/DavidBoja/SMPL-Anthropometry
SMPL-Anthropometry는 SMPL body 모델의 길이를 측정해주는 유용한 도구입니다.

#### 4.1. 환경 생성 및 활성화
```bash
conda create -n smpla python=3.9
conda activate smpla
````
4.2. 필요한 모듈 설치
requirements.py에 있는 모든 모듈을 설치합니다:
```bash
pip install -r requirements.txt
```
### 5. Model 
smplx, vposer, openpose model을 따로 다운로드 받아서 해당하는 폴더에 넣습니다.
