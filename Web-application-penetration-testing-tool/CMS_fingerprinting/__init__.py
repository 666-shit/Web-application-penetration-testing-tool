import re
import requests
import csv

cms_patterns = {
    'WordPress': 'wp-content|wp-includes|wp-admin|xmlrpc.php',
    'Joomla': 'index.php?option=com_',
    'Drupal': 'sites/all/themes|sites/default/files|sites/all/modules',
    'Magento': 'skin/frontend|js/mage|media/catalog',
    'Shopify': 'cdn.shopify.com|shopify.com/admin/auth/login',
    'Blogger': 'blogger.com|blogspot.com',
    'Typepad': 'typepad.com',
    'Ghost': 'ghost.org/|ghost.io/|ghost.io/ghost/',
    'Squarespace': 'static.squarespace.com/static/|squarespace.com/|squarespace.com/favicon.ico',
    'Wix': 'wix.com|wixpress.com|wixstatic.com',
    'Weebly': 'cdn.weebly.com|weebly.com/weebly/|weeblycloud.com/',
    'Jimdo': 'jimdo.com/|jimstatic.com/|jimdo-template.com/',
    'PrestaShop': 'themes/prestashop',
    'OpenCart': 'index.php?route=common/home',
    'osCommerce': 'catalog/includes/',
    'ZenCart': 'zencart.com/favicon.ico',
    'Discuz': 'forum.php|portal.php',
    'phpwind': 'phpwind.net|pwapp.net',
    'DedeCMS': 'templets|plus|member|dede/',
    'MetInfo': 'metinfo.cn|metinfo.com',
    'EmpireCMS': 'skin/default/images|admin/login.php',
    'Z-blog': 'zb_system/|zb_users/|zb_install/',
    'ThinkPHP': 'ThinkPHP|index.php/index/index/module/',
    'Laravel': 'laravel.com|laravel-admin.org|laravel-admin.cn',
    'Yii': 'Yii Framework|index.php?r=',
    'Flask': 'flask.pocoo.org',
    'Django': 'djangoproject.com|admin/login',
    'Tencent Cloud': 'qcloud.com',
    'Aliyun': 'aliyuncs.com',
    'Baidu Cloud': 'bcebos.com',
    'Huawei Cloud': 'cloud.huawei.com',
    'CSDN': 'csdn.net|scdnimg.cn',
    'Jianshu': 'jianshu.com',
    'Zhihu': 'zhihu.com',
    'Toutiao': 'toutiao.com',
    'Weibo': 'weibo.com',
    'Douban': 'douban.com',
    'Sina': 'sina.com.cn'
}


# cms识别模块
def cms_identification(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        for cms, pattern in cms_patterns.items():
            if re.search(pattern, content, re.IGNORECASE):
                return cms
        return '未知CMS'
    else:
        return '请求失败'


# 版本扫描模块
def version_identification(url, cms):
    if cms == 'WordPress':
        response = requests.get(url + '/readme.html')
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            version = re.search(r'WordPress (\d+\.\d+\.\d+)', content)
            if version:
                return version.group(1)

        response = requests.get(url + '/wp-includes/version.php')
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            version = re.search(r'\$wp_version\s*=\s*\'(\d+\.\d+\.\d+)\'', content)
            if version:
                return version.group(1)

        response = requests.get(url + '/wp-admin/admin-ajax.php?action=get-wp-version')
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            version = re.search(r'(\d+\.\d+\.\d+)', content)
            if version:
                return version.group(1)

        return '未知版本'

    elif cms == 'Joomla':
        response = requests.get(url + '/administrator/manifests/files/joomla.xml')
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            version = re.search(r'<version>(\d+\.\d+\.\d+)</version>', content)
            if version:
                return version.group(1)

        response = requests.get(url + '/libraries/cms/version/version.php')
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            version = re.search(r'\$RELEASE\s*=\s*\'(\d+\.\d+\.\d+)\'', content)
            if version:
                return version.group(1)

        return '未知版本'

    elif cms == 'Drupal':
        response = requests.get(url + '/CHANGELOG.txt')
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            version = re.search(r'Drupal (\d+\.\d+\.\d+)', content)
            if version:
                return version.group(1)

        return '未知版本'

    else:
        return '未知CMS'


# 漏洞扫描模块
def vulnerability_scanner(url, cms, version):
    if cms == 'WordPress':
        # 发起一个 GET 请求，请求的是 url + '/wp-content/plugins/akismet/readme.txt' 这个路径对应的文本文件。
        # 这个文件在 WordPress 的 Akismet 插件中存在，并且可以用于识别当前安装的插件的版本号和发布信息等。
        # 如果请求响应码为 200，则表示请求成功，继续判断版本号。
        if version != '未知版本':
            response = requests.get(url + '/wp-content/plugins/akismet/readme.txt')
            if response.status_code == 200:
                content = response.content.decode('utf-8')
                if version in content:
                    return '可能存在插件漏洞'
                else:
                    return '无插件漏洞'
            else:
                return '请求失败'
        else:
            return '未知版本'
    elif cms == 'Joomla':
        if version != '未知版本':
            response = requests.get(url + '/administrator/components/com_contenthistory/history.xml')
            if response.status_code == 200:
                content = response.content.decode('utf-8')
                if version in content:
                    return '可能存在插件漏洞'
                else:
                    return '无插件漏洞'
            else:
                return '请求失败'
        else:
            return '未知版本'
    elif cms == 'Drupal':
        if version != '未知版本':
            response = requests.get(url + '/user/login')
            if response.status_code == 200:
                content = response.content.decode('utf-8')
                if 'Drupal ' + version in content:
                    return '可能存在插件漏洞'
                else:
                    return '无插件漏洞'
            else:
                return '请求失败'
        else:
            return '未知版本'
    else:
        return '未知CMS'


# 插件扫描模块
def plugin_scanner(url):
    response = requests.get(url + '/wp-content/plugins/')
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        plugins = re.findall(r'<a href="(.+?)"', content)
        if plugins:
            return plugins
        else:
            return '未找到插件'
    else:
        return '非WordPress网站'


# 目录扫描模块
def directory_scanner(url):
    response = requests.get(url)
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        directories = re.findall(r'<a href="(.+?)/"', content)
        if directories:
            return directories
        else:
            return '网站没有目录'
    else:
        return '未知错误'


# 结果输出模块
def result_output(url, cms, version, vulnerability, plugins, directories):
    print('URL: ', url)
    print('CMS: ', cms)
    print('版本: ', version)
    print('漏洞: ', vulnerability)
    print('插件(仅对WordPress): ', plugins)
    print('目录: ', directories)


def save_to_csv(url, cms, version, vulnerability, plugins, directories):
    with open('CMS_fingerprinting/result.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # writer.writerow(['URL', 'CMS', 'Version', 'Vulnerability', 'Plugins', 'Directories'])
        writer.writerow([url, cms, version, vulnerability, plugins, directories])


def main():
    while True:
        print("[MENU] cms指纹扫描")
        print("[INFO] 输入示例：https://www.lsbin.com/0000.html#")
        url = input('[INPUT] 输入URL(输入0返回上一级): ')
        pattern = r'^https?://[\w-]+(\.[\w-]+)+([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?$'
        match = re.match(pattern, url)
        if url == '0':
            break

        elif not match:
            print("[ERROR] URL 格式有误，请重新输入！")
            continue

        else:
            print("[+] 正在扫描...")
            cms = cms_identification(url)
            version = version_identification(url, cms)
            vulnerability = vulnerability_scanner(url, cms, version)
            plugins = plugin_scanner(url)
            directories = directory_scanner(url)
            result_output(url, cms, version, vulnerability, plugins, directories)
            save_to_csv(url, cms, version, vulnerability, plugins, directories)
            print(f"[INFO] 网站{url}扫描完毕")


# if __name__ == '__main__':
#     main()
