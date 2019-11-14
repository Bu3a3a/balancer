import random
from urllib.parse import urlparse
from sanic import Sanic
from sanic import response
from sanic.exceptions import InvalidUsage

import settings as default_settings

app = Sanic()
app.config.from_object(default_settings)


variants = [default_settings.CDN_A_HOST]*default_settings.CDN_A_WEIGHT + \
           [default_settings.CDN_B_HOST]*default_settings.CDN_B_WEIGHT + \
           [default_settings.ORIGIN_HOST]*default_settings.ORIGIN_WEIGHT


@app.route("/")
async def balance(request):
    vurl = request.args.get('video')
    if not vurl:
        raise InvalidUsage('A query string parameter "video" WAS NOT FOUND!')

    cdn_host = random.choice(variants)
    if cdn_host == ' ':
        return response.redirect(vurl)

    vurl_parsed = urlparse(vurl)
    redirect_url = f'{vurl_parsed.scheme}://{cdn_host}/{vurl_parsed.netloc.split(".")[0]}{vurl_parsed.path}'
    return response.redirect(redirect_url)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888, workers=8)

