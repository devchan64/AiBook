"""Build GIF previews from recorded frame order. Requires Pillow; no inference."""
from pathlib import Path
import argparse
import hashlib
import json
from PIL import Image, ImageDraw


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,required=True)
    parser.add_argument('--output-dir',type=Path,required=True)
    parser.add_argument('--fps',type=int,help='Override playback rate without changing frames')
    args=parser.parse_args()
    record=json.loads((args.root/'result.json').read_text())
    fps=record['fps'] if args.fps is None else args.fps
    if fps<=0:raise ValueError('fps must be positive')
    duration=1000/fps
    if duration%10:raise ValueError('GIF requires a positive frame duration in multiples of 10ms')
    args.output_dir.mkdir(parents=True,exist_ok=False)
    provenance={'fps':fps,'duration_ms':int(duration),'interpolation':False,'loop':0,'outputs':{}}
    for direction,paths in record['frames'].items():
        frames=[]
        for path in paths:
            source=(args.root/path).resolve()
            if not source.is_relative_to(args.root.resolve()):raise ValueError('Path outside input root')
            with Image.open(source) as im:
                if im.size!=(512,512):raise ValueError('Expected 512x512 frame')
                frames.append(im.convert('RGB'))
        if not frames:raise ValueError('Empty sequence')
        output=args.output_dir/f'{direction}.gif'
        frames[0].save(output,save_all=True,append_images=frames[1:],duration=int(duration),loop=0,disposal=2)
        # Six frames remain separate: the contact sheet allows comparison without timing.
        sheet=Image.new('RGB',(512*len(frames),544),'white');draw=ImageDraw.Draw(sheet)
        for i,(frame,number) in enumerate(zip(frames,record['source_frame_numbers'][direction])):
            sheet.paste(frame,(i*512,32));draw.text((i*512+12,10),f'{direction} / source frame {number}',fill='black')
        sheet.save(args.output_dir/f'{direction}-frames.png')
        provenance['outputs'][output.name]={'source_files':paths,'frames':len(frames),'sha256':hashlib.sha256(output.read_bytes()).hexdigest()}
    provenance['code_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (args.output_dir/'stitch-record.json').write_text(json.dumps(provenance,indent=2)+'\n')


if __name__=='__main__':main()
