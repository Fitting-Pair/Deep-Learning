#!/bin/zsh

# Conda 초기화 (한 번만 실행)
if ! grep -q "conda initialize" ~/.zshrc; then
    conda init zsh
    source ~/.zshrc
fi

# 가상환경 이름과 실행할 명령어를 인수로 받습니다.
ENV_NAME=$1
shift
COMMAND=$@

# 가상환경 활성화
source ~/.zshrc
conda activate $ENV_NAME

# 명령어 실행
$COMMAND

# 가상환경 비활성화
conda deactivate
