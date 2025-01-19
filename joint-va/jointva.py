import os
from audioldm.pipelines.pipeline_audioldm import AudioLDMPipeline
import torch
import soundfile as sf
from accelerate.utils import set_seed
from audioldm.models.unet import UNet2DConditionModel
from moviepy.editor import VideoFileClip, AudioFileClip
from glob import glob
import argparse
import math
import random

parser = argparse.ArgumentParser()
parser.add_argument("--eval_set_root", type=str, default="eval-set/generative")
parser.add_argument("--out_root", type=str, default="results-bind")
parser.add_argument("--prompt_root", type=str, default="results-bind")
parser.add_argument("--optimize_text", action='store_true', default=False)
parser.add_argument("--double_loss", action='store_true', default=False)
parser.add_argument("--start", type=int, default=0)
parser.add_argument("--end", type=int, default=500)
parser.add_argument("--init_latents", action='store_true', default=False)
parser.add_argument("--seed", type=int, default=30) 

args = parser.parse_args()
# input text -> latent space -> output audio and video
local_model_path = 'ckpt/audioldm-m-full' 
unet = UNet2DConditionModel.from_pretrained(local_model_path, subfolder='unet').to('cuda')
pipe = AudioLDMPipeline.from_pretrained(local_model_path, unet=unet)
pipe = pipe.to("cuda")
os.environ["CUDA_LAUNCH_BLOCKING"] = "1"
os.environ["CUBLAS_WORKSPACE_CONFIG"] = ":16:8"
# torch.use_deterministic_algorithms(True)
torch.use_deterministic_algorithms(True, warn_only=True)

# Enable CUDNN deterministic mode
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False
torch.backends.cuda.matmul.allow_tf32 = False
out_dir = args.out_root
config_seed_dict = {
    '0jZtLuEdjrk_000110':30,
    '0OriTE8vb6s_000150':77,
    '0VHVqjGXmBM_000030':30,
    '1EtApg0Hgyw_000075':30,
    '1PgwxYCi-qE_000220':45,
    'AvTGh7DiLI_000052':56,
    'imD3yh_zKg_000052':30,
    'jy_M41E9Xo_000379':56,
    'L_--bn4bys_000008':30
}
