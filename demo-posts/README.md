# Demo posts

24 ready-to-post items for posting live in class. Each post is two files:

- `post-NN.jpg` : the image (a themed photo, so you can see what you are posting)
- `post-NN.txt` : the caption on the first line, then the author and the `image_url` to post

`posts.json` is the same 24 as one machine-readable list.

## Post one, or all, into the running app

The app stores an `image_url` (it does not upload files), so `post.py` sends each item's caption,
author, and image URL to the API.

```bash
# post a single one
python3 post.py 05

# post all 24
python3 post.py all
```

If your backend runs on a different port (port 8000 is often taken), point the helper at it:

```bash
POSTGRAM_API=http://localhost:8001/api  python3 post.py all
```

## Post by hand (to show the flow in class)

Grab any `post-NN.txt`, copy its caption and `image_url`, and either use the app UI or curl:

```bash
curl -X POST http://localhost:8001/api/posts \
  -H 'Content-Type: application/json' \
  -d '{"image_url":"<from the txt>","caption":"<first line of the txt>","author":"<from the txt>"}'
```

## Notes

- Images are from loremflickr (Creative Commons photos from Flickr). They render from the URL in
  each `.txt`, so posting needs an internet connection. The local `.jpg` files are there so you can
  preview and pick without loading anything.
- Captions are varied on purpose (food, travel, pets, work, nature) so the feed looks real.
