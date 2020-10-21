import requests


def send_otp(otp_pin, mobile_num):
    url = "https://www.fast2sms.com/dev/bulk"
    message = f"Tagava - Your otp is {otp_pin}"
    payload = "sender_id=TAGAVA&message="+message+"&language=english&route=p&numbers="+mobile_num+""
    headers = {
        'authorization': "ngI4WU5uAtVX82qyTCDE0vfhBjQaFxOwipRNdLoGZ7zKHSM3r1AwfuYCpWQi8G26oec9qy0EF3mrPtvV",
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
        }

    try:
        response = requests.request("POST", url, data=payload, headers=headers)
    except requests.exceptions.RequestException as ex:
        response = None
    except Exception as ex:
        response = None

    return response
