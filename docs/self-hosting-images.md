# Self-hosting the website photos (one-off task)

**Why:** eight pages (Services, News and six articles) load their photos from Unsplash, a third-party website. Self-hosting means the pages no longer depend on it: faster, more private, and the link checker can see problems.

**When:** do this *after* all other changes are uploaded to GitHub, so you start from the latest copy of the site.

You need: a computer with internet access, and Python 3 (free).

## 1. Install Python (once)

- **Windows:** download Python 3 from python.org (Downloads button). In the installer, **tick "Add python.exe to PATH"**, then Install.
- **Mac:** Python 3 is usually present; if not, install from python.org.

Check it worked. Open a terminal (Windows: press the Windows key, type `cmd`, Enter) and type `python --version` (Mac: `python3 --version`). You should see "Python 3.…".

## 2. Get the latest copy of the site

1. Open the repository on GitHub, click the green **Code** button, then **Download ZIP**.
2. Extract it (Windows: right-click, **Extract All**). You get a folder named `jopetnah-corporate-site-main`.

## 3. Open a terminal inside that folder

- **Windows:** open the folder in File Explorer, click the address bar, type `cmd`, press Enter.
- **Mac:** right-click the folder, **New Terminal at Folder**.

## 4. Dry run (changes nothing)

```
python tools/localise_images.py --dry-run
```
(Mac: `python3 tools/localise_images.py --dry-run`.)

You should see `34 distinct image files referenced`, then a list of lines starting `would download`, then `Dry run only: nothing downloaded or changed.` This step reads the website files only, so it works without internet.

If you see "python is not recognized", reinstall Python and tick "Add to PATH", or try `py tools\localise_images.py --dry-run`.

## 5. Real run

```
python tools/localise_images.py
```
It downloads each photo, checks it is a genuine JPEG, saves it in `assets/photos/`, and rewrites the pages that use it. It prints each page it rewrites and ends with a summary such as `Downloaded 34 new file(s) ... 34 of 34 available locally; 8 page(s) rewritten.`

If any photo fails, it says which and leaves that page pointing at Unsplash. Just run the command again when your internet is stable: it is safe to repeat.

## 6. Check locally

Open `services.html` and `news.html` by double-clicking them. The photos should appear.

## 7. Put the changes on GitHub

**Easiest (GitHub Desktop):** install GitHub Desktop, **File, Clone repository**, choose `jopetnah-corporate-site`. Do steps 3 to 5 inside that cloned folder (Repository, **Show in Explorer**). GitHub Desktop then lists the changed files. Type a summary such as `Self-host photos`, click **Commit to main**, then **Push origin**.

**Alternative (web upload):** on GitHub open the `assets` folder, **Add file, Upload files**, drag in the new `photos` folder, and commit. Then go back to the repository root, **Add file, Upload files**, drag in the 8 rewritten pages named in step 5, and commit. Upload the photos *first*, so the pages never point at missing files.

## 8. Confirm

- Actions tab: the new run should be green.
- Open the live Services page. The photos should show.
- Optional: browser developer tools, Network tab: no requests to `images.unsplash.com`.

Afterwards you may remove the Unsplash line from `.lychee.toml`. Expect the repository to grow by a few megabytes. The Unsplash licence allows free use; attribution is not required.
