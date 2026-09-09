import sys, glob
from PIL import Image, ImageDraw, ImageFont
files = sorted(glob.glob('assets/raw/portrait/s*.png'))[:10]
cols, rows = 5, 2
tw, th = 324, 576
sheet = Image.new('RGB', (cols*tw+ (cols+1)*10, rows*th + (rows+1)*10 + rows*30), (12,16,20))
f = ImageFont.truetype('assets/fonts/DejaVuSans-Bold.ttf', 20)
d = ImageDraw.Draw(sheet)
for i, fp in enumerate(files):
    im = Image.open(fp).convert('RGB'); im.thumbnail((tw,th), Image.LANCZOS)
    r, c = divmod(i, cols)
    x = 10 + c*(tw+10); y = 10 + r*(th+40)
    sheet.paste(im, (x,y))
    d.text((x, y+th+6), fp.split('/')[-1].replace('.png',''), font=f, fill=(0,229,255))
sheet.save('livrables/validation/planche_salve1_9x16.jpg', quality=90)
print('OK', len(files))
