import feedparser
import easygui
from datetime import datetime

news_url = "https://rthk.hk/rthk/news/rss/c_expressnews_clocal.xml"
d = feedparser.parse(news_url)
entries = d["entries"]

keyword = easygui.enterbox(
    msg="Enter a keyword to search in the articles:", title="RTHK Keyword Search"
)

if not keyword:
    easygui.msgbox("No keyword entered. Exiting.", title="Cancelled")
else:
    keyword = keyword.strip().lower()
    matches = []

    for entry in entries:
        title = entry.get("title", "").lower()
        summary = entry.get("summary", "").lower()
        description = entry.get("description", "").lower()

        # Safely format the date
        try:
            published = datetime.strptime(
                entry.get("published", ""), "%a, %d %b %Y %H:%M:%S %z"
            ).strftime("%d %b %Y")
        except (ValueError, TypeError):
            published = "No date"

        if keyword in title or keyword in summary or keyword in description:
            # Store the formatted date together with the entry
            matches.append((entry, published))

    if matches:
        result_text = f"Found {len(matches)} article(s) matching '{keyword}':\n\n"
        for i, (m, published) in enumerate(matches, 1):
            result_text += f"{i}. {m.get('title', 'No title')}\n"
            result_text += (
                f"   {m.get('summary', m.get('description', 'No summary'))[:300]}...\n"
            )
            result_text += f"   Link: {m.get('link', 'No link')}\n"
            result_text += f"   Published: {published}\n\n"  # ← now uses the nice date

        easygui.textbox(
            msg="Matching Articles", title=f"Results for '{keyword}'", text=result_text
        )
    else:
        easygui.msgbox(
            f"No articles found containing the keyword '{keyword}'.", title="No Results"
        )
