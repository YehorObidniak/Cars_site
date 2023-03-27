from fake_useragent import UserAgent


ua = UserAgent()


def getParametersForRequest(i="", domain=""):
    if domain == "Yallamotors":
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-language": "en-US,en;q=0.9,ru;q=0.8,ru-RU;q=0.7",
            "cache-control": "max-age=0",
            # "if-modified-since": "Fri, 27 Jan 2023 18:35:29 GMT",
            "sec-ch-ua": '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "sec-gpc": "1",
            "upgrade-insecure-requests": "1",
            # "referrer": f"https://www.dubicars.com/search?view=&ms=yes&o=&ul=BG&ma=&mo=&b=&set=bu&pf=&pt=160000&emif=&emit=&c=used&yf=&yt=&kf=&kt=160000&eo=&stsd=&cr=USD&cy=&co=&s=&gi=&f=&g=&l=&st=&page={i}",
            "referrerPolicy": "strict-origin-when-cross-origin",
            "body": "null",
            "method": "GET",
            "mode": "cors",
            "credentials": "include",
        }
    elif domain == "Dubizzle":
        headers = {
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9,ru;q=0.8,ru-RU;q=0.7",
            "Connection": "keep-alive",
            "Origin": "https://uae.dubizzle.com",
            # 'Origin': f'https://uae.dubizzle.com',
            "Referer": "https://uae.dubizzle.com",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "User-Agent": f"{ua.random}",
            "content-type": "application/x-www-form-urlencoded",
            "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-gpc": "1",
        }
        link = "https://wd0ptz13zs-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(4.11.0)%3B%20Browser%20(lite)&x-algolia-api-key=6215b7bc0b9a929db64d9fb9ee902648&x-algolia-application-id=WD0PTZ13ZS"
        data = get_data_param(i)
        return headers, link, data
    elif domain == "Dubicars":
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-language": "en-US,en;q=0.9,ru;q=0.8,ru-RU;q=0.7",
            "cache-control": "max-age=0",
            # "if-modified-since": "Fri, 27 Jan 2023 18:35:29 GMT",
            "sec-ch-ua": '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "sec-gpc": "1",
            "upgrade-insecure-requests": "1",
            # "referrer": f"https://www.dubicars.com/search?view=&ms=yes&o=&ul=BG&ma=&mo=&b=&set=bu&pf=&pt=160000&emif=&emit=&c=used&yf=&yt=&kf=&kt=160000&eo=&stsd=&cr=USD&cy=&co=&s=&gi=&f=&g=&l=&st=&page={i}",
            "referrerPolicy": "strict-origin-when-cross-origin",
            "body": "null",
            "method": "GET",
            "mode": "cors",
            "credentials": "include",
        }
        return headers


def get_data_param(num):
    return (
        '{"requests":[{"indexName":"motors.com","query":"","params":"page='
        + str(num)
        + '&attributesToHighlight=%5B%5D&hitsPerPage=200&attributesToRetrieve=%5B%22promoted%22%2C%22is_premium%22%2C%22is_featured_agent%22%2C%22location_list%22%2C%22objectID%22%2C%22name%22%2C%22price%22%2C%22neighbourhood%22%2C%22agent_logo%22%2C%22can_chat%22%2C%22has_whatsapp_number%22%2C%22details%22%2C%22photo_thumbnails%22%2C%22highlighted_ad%22%2C%22absolute_url%22%2C%22id%22%2C%22category_id%22%2C%22uuid%22%2C%22category%22%2C%22has_phone_number%22%2C%22category_v2%22%2C%22photos_count%22%2C%22description%22%2C%22created_at%22%2C%22site%22%2C%22permalink%22%2C%22has_vin%22%2C%22auto_agent_id%22%2C%22is_trusted_seller%22%2C%22show_trusted_seller_logo%22%2C%22trusted_seller_logo%22%2C%22trusted_seller_id%22%2C%22created_at%22%2C%22added%22%2C%22jobs_logo%22%2C%22vas%22%2C%22seller_type%22%2C%22is_verified_user%22%2C%22has_video%22%2C%22cotd_on%22%2C%22is_super_ad%22%5D&filters=(price%3A1%20TO%20100000)%20AND%20(kilometers%20%3C%3D%20160000)%20AND%20(%22seller_type%22%3A%22OW%22)%20AND%20(%22category_v2.slug_paths%22%3A%22motors%2Fused-cars%22)%20AND%20(promoted%3Afalse)"}]}'
    )


# print(get_data_param(3))
