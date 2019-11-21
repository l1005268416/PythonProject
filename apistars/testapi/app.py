from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route, Mount, WebSocketRoute
from starlette.staticfiles import StaticFiles
import uvicorn
import xbiquge
import json
from starlette.responses import JSONResponse
from starlette.requests import Request
bqg=xbiquge.biquge()
book=[]
def startup():
    print('Ready to go')


app = Starlette(debug=True, on_startup=[startup])


@app.route('/searchbook/{bookname}')
def searchbook(request):
    bookname = request.path_params['bookname']
    bqkallbook = bqg.getallbook()
    jsonlist = []
    for bqgbook in bqkallbook:
        if bqgbook[1].find(bookname) >= 0:
            aItem = {}
            aItem["url"]=bqgbook[0]
            aItem["bookname"] = bqgbook[1]
            jsonlist.append(aItem)
    return PlainTextResponse(json.dumps(jsonlist, ensure_ascii=False))


@app.route('/bookmulu', methods=['POST'])
async def getmulu(request):
    data = await request.json()
    bookurl=data['bookurl']
    mulu = bqg.getmulu(bookurl)
    jsonlist = []
    for title in mulu:
        aItem = {}
        aItem["url"] = title[0]
        aItem["bookname"] = title[1]
        jsonlist.append(aItem)
    return JSONResponse(jsonlist)


@app.route('/bookzw', methods=['POST'])
async def getzhewen(request):
    data = await request.json()
    zhengwenurl = data['zhengwenurl']
    txt=bqg.gettxt(zhengwenurl)
    return PlainTextResponse(txt)


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)