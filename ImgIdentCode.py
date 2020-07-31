# -*- coding: utf-8 -*-
import random
import requests
from hashlib import md5
from concurrent.futures import ThreadPoolExecutor

class ChaojiyingClient(object):
    def __init__(self, username, password, soft_id,proxies):
        self.proxies = proxies
        self.username = username
        password =  password.encode('utf8')
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def post_pic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files, headers=self.headers, proxies=self.proxies)
        return r.json()

    def report_error(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers, proxies=self.proxies)
        return r.json()


class VercodeImgIdent():

    def __init__(self,proxies):

        self.proxies = proxies

        user_agent = [
            'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36',
            'Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
            'Mozilla/5.0 (Windows NT 5.0; rv:21.0) Gecko/20100101 Firefox/21.0',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20130401 Firefox/31.0',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:24.0) Gecko/20100101 Firefox/24.0',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
            'Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB7.0)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
            'Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)',
            'Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999'
        ]
        self.headers = {"User-Agent": random.choice(user_agent)}

    def img_data(self,img_url,type=None,img_data=None):
        """
        获取验证数据
        :param img_url: 要识别的验证码url
        :return:验证码爬取数据
        """

        if type:
            resp = requests.post(url=img_url, headers=self.headers, data=img_data, proxies=self.proxies)
            img_data = resp.content
        else:
            resp = requests.get(url=img_url, headers=self.headers, proxies=self.proxies)
            img_data = resp.content
        return img_data

    def img_data_check(self, image_code, img_data):
        """
        验证码校验
        :param image_code:
        :return: 校验结果与验证码原始数据
        """
        url = 'https://www.xxx.com/CodeCheck.ashx'
        formdata = {
            "CheckType": "vcode",
            "CheckValue": image_code
        }
        check_img_data = requests.post(url=url,headers=self.headers, data=formdata, proxies=self.proxies).text
        img_check_results = {
            "check_result":check_img_data,
            "img_data":img_data
        }
        return img_check_results

def main(img_number):
    # 代理添加
    proxy_host = "xxxx"
    proxy_port = "xxxx"
    proxy_user = "xxxx"
    proxy_pass = "xxxx"
    proxy = f"https://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}"
    proxies = {'http': proxy, 'https': proxy}

    img_url = 'https://www.xxx.com/CAPTCHA.ashx'
    # 实例化验证码识别类
    vercode_img = VercodeImgIdent(proxies)
    # 爬取验证码数据(若是post请求需传参数type='POST',参数为img_data：验证码爬取参数)
    img_data = vercode_img.img_data(img_url)
    user_name = 'xxxx'
    pass_word = 'xxxx'
    task_id = 'xxxx'
    codetype = 'xxxx'
    # 实例化三方平台类
    chaojiying = ChaojiyingClient(user_name,pass_word,task_id,proxies)
    # 三方平台验证码识别
    image = chaojiying.post_pic(img_data,codetype)
    image_code = image.get('pic_str')
    check_data = vercode_img.img_data_check(image_code, img_data)
    if check_data.get('check_result')=='E' and len(image_code)== 4:
        print({"image": image})
        # 保存有效图片以及路径
        with open(f'./ImgData/img_{img_number}_{image_code.upper()}.png', 'wb') as f:
            f.write(check_data.get('img_data'))
    else:
        # 错误返回三方平台
        im_id = image.get('pic_id')
        report_error = chaojiying.report_error(im_id)
        print({"image":image,"report_error_data":report_error})

if __name__ == '__main__':
    img_number = []
    for img_num in range(3):
        img_number.append(img_num)
    with ThreadPoolExecutor(20) as executor:
        executor.map(main, img_number)


























    # # # chaojiying  message
    # # user_name = '15188319982'
    # # pass_word = 'python'
    # # task_id = '906524'
    # # img_status_code = 1004
    #
    # # 代理添加
    # proxy_host = "http-pro.abuyun.com"
    # proxy_port = "9010"
    # proxy_user = "HC3N3H65U90JL44P"
    # proxy_pass = "9DB7EB7B128FF220"
    # img_url = 'https://www.yangming.com/e-service/schedule/CAPTCHA.ashx'
    # # 实例化验证码识别类
    # vercode_img = VercodeImgIdent(proxy_host, proxy_port, proxy_user, proxy_pass)
    # # 爬取验证码数据(若是post请求需传参数type='POST',参数为img_data：验证码爬取参数)
    # img_data = vercode_img.img_data(img_url)
    # # 实例化三方平台类(超级鹰)
    # chaojiying = ChaojiyingClient()
    # # 三方平台验证码识别(超级鹰)
    # image = chaojiying.post_pic(img_data)
    # image_code = image.get('pic_str')
    # check_data = vercode_img.img_data_check(image_code, img_data)
    # if check_data.get('check_result')=='E' and len(image_code)== 4:
    #     print(check_data)
    #     print(image_code)



