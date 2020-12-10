# _*_ coding:utf-8 _*_
__author__ = "super.gyk"

from rest_framework.renderers import JSONRenderer


class MyJSONRenderer(JSONRenderer):
    """
    {
        code:0
        msg:'请求成功',
        data:''
    }
    """

    def render(self, data, accepted_media_type=None, renderer_context=None):
        # 返回来的数据中包含了code和mag，可以通过pop拿出来
        if isinstance(data, dict):
            code = data.pop('code', 200)
            msg = data.pop('msg', '请求成功')
        else:
            code = 0
            msg = '请求成功'

        res = {
            'code': code,
            'msg': msg,
            'data': data
        }

        return super().render(res, accepted_media_type=None, renderer_context=None)
