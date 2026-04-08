from curl_cffi import requests
import json

def test():
    url = "https://ap-mc.klikindomaret.com/assets-klikidmcore/api/get/customer/api/webapp/profile"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
        "apps": "{\"app_version\":\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36\",\"device_class\":\"browser|browser\",\"device_family\":\"none\",\"device_id\":\"856666c8-840b-4cc1-8c91-77eaa6badc85\",\"os_name\":\"Windows\",\"os_version\":\"10\"}",
        "authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJjdXN0LTE1ODA0ODEyQGtsaWtpbmRvbWFyZXQuY29tIiwiaXNFbXBsb3llZSI6ImZhbHNlIiwiZXh0ZXJuYWxDdXN0b21lcklkIjoiZTg3MDExYWQtZjJjMi00NGVjLWFmMzQtMmVkZDBiYmEzZDExIiwibmJmIjoxNzc1MzgxMjA4LCJzY29wZSI6Im1vYmlsZSIsImN1c3RvbWVySWQiOiIxNTgwNDgxMiIsImlzRHJhZnQiOiJmYWxzZSIsImV4cCI6MTc3NTM4NDgwOCwic2lkIjoiOWZjNGQ5YjktMTRiNS00YjRmLWIzYjUtYTgwOGQyYTA5NzA3IiwidXNlcm5hbWUiOiJjdXN0LTE1ODA0ODEyQGtsaWtpbmRvbWFyZXQuY29tIn0.R5p5Reh_LjX5MTNuB3mfG0VZqiIH5NVuGlZsbzAp0Z_tDtxEf4Y2jUihA_gWZoe51RTQOS8tT7KPbUoaQQ1p5QwUqJLHCiRBXrd0CUDykEVSNlvcJ5o1fo_GkRmK1E2Ab8groB8XqLMM3J1CrK0QsUKEfT3HHosKhY_aAfWYum0UloC8Y2eKYlCAvNPBBfRC93U-GiLqcpY0IlPpYGO74MJyU7fiEUfFHRSC3xC9fiPHRUfgxroRKFN51-KIPsZV34CB5X8faelmsRNDQLzc0K84NkZmhbYCCv9y53QNGHsz4Qm-7Z9e-eBLi1OUKa4k-FhQ2GqKjw-sqnh7M8OBOWWK_KvFSIcF00a6ml7kEaoquY3u_CINgOiJXWUTShuDac7UBzV0_eIHVOPtEyX6RnvtD5NgB1GFe-43cR4EM8fLf8Ft3lSbE26kYJVctpDX58uH-nHqeban23fpRcwcaQQJD3FECQQhIiU-yjrx7h-OMba9h_P--goJKldvTCmQv_IY3CDTCl1EHf9YaCQ6oOTQsCzSepE74kCAtMuJa3FZ-G-MWHBh40iQBdhv3CukXhSzudzMdJkMcDSzdMPgwPDL6QmO5iBnClZjM6uvvQ6Yj7WL82uFbdD4I3ZvV1DP6kdkAFOlp9niLCpCxNtfjCwiuEP-VkIyN5nsxPFnC_w",
        "if-none-match": "\"ivlz2xbq1ot0\"",
        "page": "/search",
        "priority": "u=1, i",
        "sec-ch-ua": "\"Chromium\";v=\"146\", \"Not-A.Brand\";v=\"24\", \"Google Chrome\";v=\"146\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "x-aws-waf-token": "93bd1439-6b05-424e-8972-6b532bb261d4:GgoAsPFG7tgeAAAA:HiX2dbAr67OVRMe+aiyUZ7syI6UtVQAsgrSKJiRjSKcWDqbJWDSBEWIkK3Ac1D45EHISuxTz46T9ovo8jm/qBAguzqohnZU0lgCpUGVqDJptEmM/BXY6e9CBtI9o0I2pLML0QaoL1F+rxtivqkfKzhI3mW96uYuPSUEbQfvWOL74xiiN5bP0olTTJNtKNH6CcZRzy3ZyXoSpIRaKILWliOyU7rUjbvfbX/kDYnt2jetBqlXp5IQD7yNzcz1C8Mbl3yi75uUq5mZf3+kA",
        "x-correlation-id": "f0bbc4a2-2f62-439e-8c78-eae1f864a489",
        "Referer": "https://www.klikindomaret.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
    }

    # Impersonate chrome
    resp = requests.get(url, headers=headers, impersonate="chrome")
    print("Status:", resp.status_code)
    print("Response:", resp.text[:500])

if __name__ == "__main__":
    test()
