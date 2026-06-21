
import praw

from data_models import EvidenceClaim
from query_engine import extract_event_query


# =========================================================
# REDDIT CLIENT
# =========================================================

reddit = praw.Reddit(
    client_id="4hNxpEgMZrRN0FlQ-xfA4w",
    client_secret="tg5C4_6V5biEnZBzhl0lIfhxhxiRUA",
    user_agent="windows:MySentimentExample:v1.0 (by u/Previous-Abies-7216)"
)


# =========================================================
# FETCH POSTS
# =========================================================

def fetch_posts(query: str, limit: int = 13):

    optimized_query = extract_event_query(query)

    print("\n" + "=" * 80)
    print("ORIGINAL CLAIM:")
    print(query)

    print("\nOPTIMIZED SEARCH QUERY:")
    print(optimized_query)

    print("\nSearching Reddit...")
    print("=" * 80)

    results = reddit.subreddit("all").search(
        optimized_query,
        sort="relevance",
        time_filter="all",
        limit=50
    )

    return list(results)


# =========================================================
# POST -> EVIDENCE
# =========================================================

def post_to_evidence(post):

    evidence = []

    # -----------------------------------------
    # POST TITLE
    # -----------------------------------------

    evidence.append(
        EvidenceClaim(
            text=post.title,
            source_type="reddit_post",
            source_id=post.id,
            subreddit=str(post.subreddit)
        )
    )

    # -----------------------------------------
    # POST BODY
    # -----------------------------------------

    if post.selftext:

        body = post.selftext.replace("\n", " ")

        if len(body) > 1000:
            body = body[:1000]

        evidence.append(
            EvidenceClaim(
                text=body,
                source_type="reddit_body",
                source_id=post.id,
                subreddit=str(post.subreddit)
            )
        )

    # -----------------------------------------
    # COMMENTS
    # -----------------------------------------

    try:

        post.comments.replace_more(limit=0)

        comments = sorted(
            post.comments,
            key=lambda c: c.score,
            reverse=True
        )

        shown = 0

        for comment in comments:

            text = comment.body.strip()

            if text in ("[removed]", "[deleted]"):
                continue

            text = text.replace("\n", " ")

            if len(text) > 1000:
                text = text[:1000]

            evidence.append(
                EvidenceClaim(
                    text=text,
                    source_type="reddit_comment",
                    source_id=comment.id,
                    subreddit=str(post.subreddit),
                    parent_id=post.id
                )
            )

            shown += 1

            if shown >= 5:
                break

    except Exception as e:
        print(f"Could not load comments: {e}")

    return evidence


# =========================================================
# BUILD EVIDENCE STREAM
# =========================================================

def build_evidence_stream(query: str):

    posts = fetch_posts(query)

    all_evidence = []

    print(f"\nFound {len(posts)} posts.\n")

    for i, post in enumerate(posts[:10], start=1):
        print(f"{i}. {post.title}")

    print("\n" + "=" * 80)

    for post in posts:

        all_evidence.extend(post_to_evidence(post))

    return all_evidence

