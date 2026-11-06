import feedparser
import easygui
import requests
from datetime import datetime

# Category options (using the active rthk9 RSS host)
categories = {
    "本地新聞": "https://rthk9.rthk.hk/rthk/news/rss/c_expressnews_clocal.xml",
    "大中華新聞": "https://rthk9.rthk.hk/rthk/news/rss/c_expressnews_greaterchina.xml",
    "國際新聞": "https://rthk9.rthk.hk/rthk/news/rss/c_expressnews_cinternational.xml",
    "財經新聞": "https://rthk9.rthk.hk/rthk/news/rss/c_expressnews_cfinance.xml",
    "體育新聞": "https://rthk9.rthk.hk/rthk/news/rss/c_expressnews_csport.xml",
}

# Pretend to be a standard web browser so RTHK does not block the request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

while True:
    # Step 1: Choose a category
    choice = easygui.choicebox(
        msg="請選擇要查看的新聞類別：",
        title="RTHK 新聞分類",
        choices=list(categories.keys()),
    )

    if not choice:
        easygui.msgbox("沒有選擇任何類別，程式結束。", title="已取消")
        break

    news_url = categories[choice]

    # Fetch the RSS XML with browser headers before parsing
    try:
        response = requests.get(news_url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        d = feedparser.parse(response.content)
        entries = d.get("entries", [])
    except requests.RequestException as e:
        easygui.msgbox(f"無法連線至 RTHK 伺服器：\n{e}", title="連線錯誤")
        continue

    if not entries:
        easygui.msgbox(f"「{choice}」目前沒有新聞。", title="沒有內容")
        continue

    # Create a numbered list of titles for the menu
    titles_list = [
        f"{i}. {entry.get('title', '無標題')}" for i, entry in enumerate(entries, 1)
    ]

    # Pad list if there is only 1 item (easygui.choicebox requires >= 2 choices)
    if len(titles_list) == 1:
        titles_list.append(" ")

    while True:
        # Step 2: Show only titles and let user click one
        selected_title = easygui.choicebox(
            msg=f"【{choice}】共有 {len(entries)} 則新聞，請點擊標題查看詳情（按 Cancel 返回分類）：",
            title=f"RTHK - {choice}",
            choices=titles_list,
        )

        # If user clicks Cancel or selects the blank padding item, go back
        if not selected_title or not selected_title.strip():
            break

        # Extract the index from the selected string (e.g., "1. Title" -> index 0)
        selected_index = int(selected_title.split(".")[0]) - 1
        entry = entries[selected_index]

        title = entry.get("title", "無標題")
        summary = entry.get("summary", entry.get("description", "無摘要"))
        link = entry.get("link", "無連結")

        # Safely format the date
        try:
            published = datetime.strptime(
                entry.get("published", ""), "%a, %d %b %Y %H:%M:%S %z"
            ).strftime("%d %b %Y %H:%M")
        except (ValueError, TypeError):
            published = "無日期"

        # Step 3: Show all info for the clicked title
        detail_text = (
            f"標題：{title}\n"
            f"發布時間：{published}\n"
            f"連結：{link}\n"
            f"{'-' * 40}\n\n"
            f"{summary}"
        )

        easygui.textbox(msg="新聞詳細內容：", title=title, text=detail_text)
