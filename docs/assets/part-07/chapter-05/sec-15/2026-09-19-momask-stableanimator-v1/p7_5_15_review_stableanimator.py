"""Assemble every generated frame for visual review; no automatic quality verdict."""
import argparse
import hashlib
import json
from pathlib import Path

import imageio.v2 as imageio
import numpy as np
from PIL import Image, ImageDraw

parser = argparse.ArgumentParser()
parser.add_argument('name')
args = parser.parse_args()
folder = Path(__file__).resolve().parent / args.name
plan = json.loads((folder / 'plan.json').read_text())
paths = sorted((folder / 'output/animated_images').glob('frame_*.png'),
               key=lambda p: int(p.stem.split('_')[-1]))
assert len(paths) == len(plan['source_frames']) == 32
grid = Image.new('RGB', (8 * 256, 4 * 288), 'white')
draw = ImageDraw.Draw(grid)
hashes = {}
with imageio.get_writer(str(folder / 'preview-20fps.mp4'), fps=20, codec='libx264') as writer:
    for i, path in enumerate(paths):
        im = Image.open(path).convert('RGB')
        assert im.size == (512, 512)
        writer.append_data(np.asarray(im))
        x, y = i % 8 * 256, i // 8 * 288
        grid.paste(im.resize((256, 256)), (x, y + 32))
        draw.text((x + 5, y + 6), f'output {i} / motion {plan["source_frames"][i]}', fill='black')
        hashes[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
grid.save(folder / 'all-frames.jpg', quality=93)
(folder / 'frame-hashes.json').write_text(json.dumps(hashes, indent=2) + '\n')
print(folder / 'all-frames.jpg')
