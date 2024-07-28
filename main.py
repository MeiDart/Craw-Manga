import requests
from bs4 import BeautifulSoup
from model.DetailChaper import DetailChapter
import os
from concurrent.futures import ThreadPoolExecutor
import datetime
import unicodedata

#constant
BANG_XOA_DAU = str.maketrans(
    "ÁÀẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬĐÈÉẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴáàảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵ",
    "A"*17 + "D" + "E"*11 + "I"*5 + "O"*17 + "U"*11 + "Y"*5 + "a"*17 + "d" + "e"*11 + "i"*5 + "o"*17 + "u"*11 + "y"*5
)

#method
def get_html_beautiful_soup(url: str) -> BeautifulSoup:
    req = requests.get(url)
    return BeautifulSoup(req.content, 'html.parser')

def get_img_urls(soup: BeautifulSoup) -> list:
    img_urls = []
    raw_html_tag_img = soup.select('.reading-detail .page-chapter img ')
    for image in raw_html_tag_img:
        if 'data-src' in image.attrs:
            img_urls.append(image['data-src'])
        elif 'src' in image.attrs:  
            img_urls.append(image['src'])
    return img_urls

def format_string_to_router(txt: str) -> str:
    if not unicodedata.is_normalized("NFC", txt):
        txt = unicodedata.normalize("NFC", txt)
    txt = txt.translate(BANG_XOA_DAU).lower()
    txt = '-'.join(txt.split()) 
    return txt
    
def download_image(session, img_url, folder_path, idx):
    res = session.get(img_url)
    with open(f'{folder_path}/{idx+1}.jpg', 'wb') as f:
        f.write(res.content)

def download_one_chapter(detail_chapter: DetailChapter, session, name_manga: str) -> None:
    soup = get_html_beautiful_soup(detail_chapter.link)
    img_urls = get_img_urls(soup)
    folder_path = f'E:/Data Manga/{name_manga}/{detail_chapter.chapter_number}'
    os.makedirs(folder_path, exist_ok=True)
    
    with ThreadPoolExecutor(max_workers=8) as executor:
        for idx, img_url in enumerate(img_urls):
            executor.submit(download_image, session, img_url, folder_path, idx)

def download_all_chapters(detail_chapters: list['DetailChapter'], name_manga: str) -> None:
    with requests.Session() as session:
        with ThreadPoolExecutor(max_workers=8) as executor:
            for detail_chapter in detail_chapters:
                executor.submit(download_one_chapter, detail_chapter, session, name_manga)

# Handle
url = 'https://nettruyenviet.com/truyen-tranh/ajin'



link_chapters = []
soup = get_html_beautiful_soup(url)
chapters = soup.select('.list-chapter > nav #desc li .chapter a ')
raw_name = soup.select_one('.title-detail').get_text()
formated_name = format_string_to_router(raw_name)

print(formated_name)

for chapter in chapters:
    chapter_number = chapter.text.split()[1]
    chapter_link = chapter['href']
    link_chapters.append(DetailChapter(chapter_number, chapter_link))

if link_chapters:
    print(f'start download at {datetime.datetime.now()}')
    download_all_chapters(link_chapters, formated_name)
    print(f'done at {datetime.datetime.now()}')
