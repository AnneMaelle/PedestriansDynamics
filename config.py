import os

neighborhood = "Moore"
nbPeds = 250
width = 32
height = 32
image_name = '1exit_2large.tif'
image_path = os.path.join(os.path.curdir, 'ressources', image_name)
delta_DFF = 0.1
delta_decay_DFF = delta_DFF/4
decay_rate_DFF = 1
diffusion_rate_DFF = 0.1
delta_diffusion_DFF = delta_DFF/2
max_dff_value = 0.9
kappaS = 2
kappaD = 0.5

