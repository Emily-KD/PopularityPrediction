"""
This example run script shows how to run the Instagram.com scraper defined in ./instagram.py
It scrapes product data and product search and saves it to ./results/

To run this script set the env variable $SCRAPFLY_KEY with your scrapfly API key:
$ export $SCRAPFLY_KEY="your key from https://scrapfly.io/dashboard"
"""
from pathlib import Path
from loguru import logger as log
import asyncio
import json
import instagram
import argparse


async def run(username):

    output = Path(__file__).parent / f"results/{username}"
    output.mkdir(exist_ok=True)

    # enable scrapfly cache?
    instagram.BASE_CONFIG["cache"] = True
    instagram.BASE_CONFIG["debug"] = True

    print(f"running Instagram scrape for @{username} and saving results to ./results directory")

    try: 
        user = await instagram.scrape_user(username)
        output.joinpath(f"{username}_user.json").write_text(
            json.dumps(user, indent=2, ensure_ascii=False), encoding="utf-8")

        post_video = await instagram.scrape_post("https://www.instagram.com/p/Cs9iEotsiGY/")
        output.joinpath(f"{username}_video-post.json").write_text(
            json.dumps(post_video, indent=2, ensure_ascii=False), encoding='utf-8')

        post_multi_image = await instagram.scrape_post("https://www.instagram.com/p/Csthn7EO99u/")
        output.joinpath(f"{username}_multi-image-post.json").write_text(
            json.dumps(post_multi_image, indent=2, ensure_ascii=False), encoding='utf-8')

        # scrape_user_posts requires the profile username
        posts_all = []
        async for post in instagram.scrape_user_posts(username, max_pages=1000):
            posts_all.append(post)

        log.success(f"scraped {len(posts_all)} posts for @{username}")
        output.joinpath(f"{username}_all-user-posts.json").write_text(
            json.dumps(posts_all, indent=2, ensure_ascii=False), encoding='utf-8')
        
    except Exception as e:
        log.error(f"error scraping @{username}: {str(e)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="scrape an Instagram account using Scrapfly")
    parser.add_argument("--username", type=str, required=True, help="Instagram username to scrape")
    args = parser.parse_args()

    asyncio.run(run(args.username))
