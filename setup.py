import os, torch, torchvision, torchaudio

def run_in_terminal(command_list: list) -> None:
    for command_str in command_list:
        os.system(command_str)

def install_requirements(GPU_integration: bool = False) -> None:
    run_in_terminal([
        "pip install -r requirements.txt", # downloads YOLO v5 required packages
        "python data/TACO/download_script.py" # downloads TACO images (NOTE: FCPS wifi results in a connection error) and generates YOLO v5 annotations
    ])

    if GPU_integration: # NOTE: for GPU-PyTorch integration (optional), install CUDA-11.7.0 and cuDNN-8.6.0 (https://youtu.be/hHWkvEcDBO0?t=205)
        run_in_terminal([ 
            "pip uninstall torch", # remove torch-1.13.0+cpu (default installation is CPU only)
            "pip3 install torch==1.13.0+cu117 torchvision==0.14.0+cu117 torchaudio===0.13.0+cu117 -f https://download.pytorch.org/whl/cu117/torch_stable.html",
        ])

install_requirements()

print(f"PyTorch: {torch.__version__}\t TorchVision: {torchvision.__version__}\t TorchAudio: {torchaudio.__version__}\n" +\
      f"CUDA enabled: {torch.cuda.is_available()}\t CuDNN enabled: {torch.backends.cudnn.enabled}\n")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def compile_model(pretrained: bool = False) -> None:
    if pretrained:
        model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
        # TODO: finish this
    else:
        run_in_terminal([
            "python train.py --img 640 --batch 16 --epochs 10 --data TACO.yaml --weights yolov5s.pt --name trash_classifier --cache disk",
            "python detect.py --weights runs/train/trash_classifier/weights/best.pt --img 640 --conf 0.4 --source data/TACO/images/test"
        ])

compile_model()
