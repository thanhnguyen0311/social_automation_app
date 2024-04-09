import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

LDPLAYER_PATH = "E:\LDPlayer\LDPlayer9"
LDCONSOLE_PATH = os.path.join(LDPLAYER_PATH, "ldconsole.exe")
vms_path = os.path.join(LDPLAYER_PATH, "vms")
config_path = os.path.join(LDPLAYER_PATH, "vms", "config")
LOGO_PATH = os.path.join("assets", "img", "logo.png")
pytesseract_PATH = os.path.join("Tesseract-OCR", "tesseract.exe")
LAMNGOCTHANH_PAGEID = "107073257616977"
LAMNGOCTHANH_ACCESSTOKEN = "EAAGDTcgCjZBoBO8ZB6PLcEFNVnMVavES8loHp1zjZA7qoMhfj1r1NZBAFdMUxFZCLWJYLq748GkwfgBJfyOrC91auUDz96OxHs75VZCrXYDEeyTxbIK58UMPhQSlOSSCXkg0t2rWT6ZAppvl04oh5E81cpZCraoZCJDb1zJ5FT7jZAJjZCHZBZCdZC127wjuXLhFUvbC8ZD"
HCSPA_PAGEID = "238210359712854"
HCSPA_PAGEID_ACCESSTOKEN = "EAAGDTcgCjZBoBOZCVvTAQ5jKXxDDHBquHC2fX0icvWG0tKRe8wkmqSVFsGVtzr2wBd4KYx72C3eJYWrZCTzWaVZBiUfB7tvIHmpHEBymYhLfDijXfBZCZCf2yXaNpV4Hebddr6wKBZCUTvhHUHY3lu03LNFa25c4F2OkWZAvVp8Ilqu2TDRKfinUXzmCj8W5VkYZD"


CLONE_LD_DATA = True

SERVER_SOCKET = "ws://luxcoin.hieuchauspa.com/ws/connect/"
account_data_config = {
    'host': '125.212.243.130',
    'user': 'nct031194',
    'password': '272337839',
    'database': 'social_automation',
}


COMMENTS = ['<3', 'ib ah', '<3 <3 <3', 'ib em voi a.', 'can tu van',
            'cần tư vấn', '.', '<3 <3', 'mình cần tư vấn ạ', 'check ib e shop',
            'ib em ạ', ':-O', 'ib', 'ib e', 'wow <3', '.', '.', 'cho xin dia chi ah',
            'ib em', 'ib e nha shop', '(y)', '.']

LNT_COMMENTS = ['còn ko ạ', 'dep qua', 'xinhhh', 'thich qa <3', 'ib e nha tiem',
                'gia bnhiu', 'gia bnhiu vậy tiệm', 'co giao hang ko ạ', 'xin gia',
                'nhiều mẫu đẹp ghê', 'vàng gi vậy ạ', 'vừa mới ghé ^^']

HCSPA_COMMENTS = ['e muốn đặt lịch', 'cần đặt lịch hôm nay', 'xin địa chỉ spa']