from services.youtube_scraper import YouTubeCommentScraper
import json

print('Starting test scrape (free best-effort) for Ola Electric...')
s = YouTubeCommentScraper()
comments = s.scrape_oem_comments('Ola Electric', max_videos=20, comments_per_video=50, target_total=100)
print('\nTOTAL_COLLECTED:', len(comments))
# Print first 10 comments (compact)
print(json.dumps(comments[:10], ensure_ascii=False, indent=2))
