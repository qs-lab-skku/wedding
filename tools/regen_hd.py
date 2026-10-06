#!/usr/bin/env python3
"""photos/full/ 을 원본에서 고해상도(긴 변 2400px, q87)로 재생성한다.

원본 위치(노트북의 Dropbox 동기화 폴더):
  <SRC>/1/DSC_NNNN.JPG  →  photos/full/p1_NNNN.jpg
  <SRC>/2/DSC_NNNN.JPG  →  photos/full/p2_NNNN.jpg

사용법 (리포 루트에서):
  python3 tools/regen_hd.py "~/Dropbox/Personal/본식아이폰스냅사진/261003 광명 라까사호텔 송승욱,루밍님 아이폰"

- 기존 photos/full/ 의 367개 파일명을 기준으로 해당 원본만 찾아 교체한다.
- 썸네일(photos/thumb/)은 그대로 둔다. 파일명이 같으므로 사이트 코드 수정 불필요.
"""
import sys, glob, os
from PIL import Image, ImageOps

LONG_SIDE = 2400
QUALITY = 87

def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    src_root = os.path.expanduser(sys.argv[1])
    fulls = sorted(glob.glob('photos/full/p*_*.jpg'))
    if not fulls:
        sys.exit('photos/full/ 이 비어 있습니다. 리포 루트에서 실행하세요.')
    done, missing = 0, []
    for f in fulls:
        base = os.path.basename(f)              # p1_1873.jpg
        cam, num = base[1], base[3:7]           # '1', '1873'
        src = None
        for ext in ('JPG', 'jpg', 'JPEG', 'jpeg'):
            cand = os.path.join(src_root, cam, f'DSC_{num}.{ext}')
            if os.path.exists(cand):
                src = cand
                break
        if not src:
            missing.append(base)
            continue
        im = ImageOps.exif_transpose(Image.open(src))
        if max(im.size) > LONG_SIDE:
            im.thumbnail((LONG_SIDE, LONG_SIDE), Image.LANCZOS)
        im.convert('RGB').save(f, quality=QUALITY, progressive=True, optimize=True)
        done += 1
        if done % 50 == 0:
            print(f'{done}/{len(fulls)}...')
    print(f'완료: {done}장 교체')
    if missing:
        print(f'원본을 못 찾은 파일 {len(missing)}개: {missing[:10]}')
        sys.exit(1)

if __name__ == '__main__':
    main()
