#!/usr/bin/env python3
"""Static delivery preview with byte-range support for seeking in the MP4."""
from pathlib import Path
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import argparse, functools, re

DIRECTORY=Path(__file__).resolve().parents[1]


class Handler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Accept-Ranges','bytes')
        super().end_headers()

    def send_head(self):
        self.byte_range=None
        header=self.headers.get('Range')
        path=Path(self.translate_path(self.path))
        if not header or not path.is_file():return super().send_head()
        match=re.fullmatch(r'bytes=(\d*)-(\d*)',header.strip())
        size=path.stat().st_size
        if not match or not any(match.groups()) or size==0:
            self.send_response(416);self.send_header('Content-Range',f'bytes */{size}');self.send_header('Content-Length','0');self.end_headers();return None
        a,b=match.groups()
        if not a:
            amount=int(b);start=max(0,size-amount);end=size-1
        else:
            start=int(a);end=min(size-1,int(b) if b else size-1)
        if start>=size or start>end:
            self.send_response(416);self.send_header('Content-Range',f'bytes */{size}');self.send_header('Content-Length','0');self.end_headers();return None
        stream=path.open('rb');stream.seek(start);self.byte_range=(start,end)
        self.send_response(206);self.send_header('Content-Type',self.guess_type(str(path)))
        self.send_header('Content-Range',f'bytes {start}-{end}/{size}');self.send_header('Content-Length',str(end-start+1));self.end_headers()
        return stream

    def copyfile(self,source,outputfile):
        if self.byte_range is None:return super().copyfile(source,outputfile)
        remaining=self.byte_range[1]-self.byte_range[0]+1
        while remaining>0:
            chunk=source.read(min(65536,remaining))
            if not chunk:break
            outputfile.write(chunk);remaining-=len(chunk)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=3000);args=parser.parse_args()
    handler=functools.partial(Handler,directory=str(DIRECTORY))
    server=ThreadingHTTPServer(('0.0.0.0',args.port),handler)
    print(f'Vivi OOR delivery viewer ready on port {args.port}',flush=True)
    server.serve_forever()


if __name__=='__main__':main()
