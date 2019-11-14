# encoding: utf-8
import random
from locust import TaskSet, task, HttpLocust
from locust.contrib.fasthttp import FastHttpLocust, FastHttpSession, FastResponse, LocustUserAgent
from geventhttpclient.useragent import UserAgent


request_urls = (
    '/?video=http://s1.origin-cluster/video/1488/xcg2djHckad.m3u8',
    '/?video=http://s1.origin-cluster/video/12/gfhdD32sasd.m3u8',
    '/?video=http://s1.origin-cluster/somevideo/78/xcg2djHckad.m3u8',
    '/?video=http://s1.origin-cluster/video/4664/dgsAsdRRfdfg.m3u8',
    '/?video=http://s1.origin-cluster/video/545/sdr34323FDs.m3u8',
)


class NoRedirectLocustUserAgent(LocustUserAgent):
    response_type = FastResponse
    redirect_resonse_codes = frozenset([])


class NoRedirectFastHttpSession(FastHttpSession):
    def __init__(self, base_url, **kwargs):
        super(NoRedirectFastHttpSession, self).__init__(base_url, **kwargs)
        self.client = NoRedirectLocustUserAgent(max_retries=1, cookiejar=self.cookiejar, **kwargs)


class NoRedirectFastHttpLocust(FastHttpLocust):
    def __init__(self):
        super(NoRedirectFastHttpLocust, self).__init__()
        self.client = NoRedirectFastHttpSession(base_url=self.host)


class UserBehavior(TaskSet):
    @task
    def get_video(self):
        self.client.get(random.choice(request_urls))


class WebsiteUser(NoRedirectFastHttpLocust):
    task_set = UserBehavior
    host = 'http://127.0.0.1:8888'
