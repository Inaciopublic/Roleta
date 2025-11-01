import os
import re
import sys
import time
import argparse
import requests

try:
    import mss
    from PIL import Image
    import pytesseract
except ImportError:
    print("Missing dependencies. Please run: pip install -r requirements.txt")
    sys.exit(1)


def grab_screenshot(region=None, out_path="screenshot.png"):
    """Capture a screenshot of either the full screen or a defined region."""
    with mss.mss() as sct:
        monitor = region if region else sct.monitors[1]
        img = sct.grab(monitor)
        Image.frombytes("RGB", img.size, img.rgb).save(out_path)
    return out_path


def ocr_numbers(image_path, whitelist_digits=True):
    """Run OCR on the image and return the most likely numeric string and raw text."""
    custom_oem_psm_config = r"--oem 3 --psm 6"
    if whitelist_digits:
        custom_oem_psm_config += " -c tessedit_char_whitelist=0123456789"

    text = pytesseract.image_to_string(Image.open(image_path), config=custom_oem_psm_config)

    candidates = re.findall(r"\d[\d\.,]*", text)
    normalized = []
    for candidate in candidates:
        digits_only = re.sub(r"[^\d]", "", candidate)
        if digits_only:
            normalized.append(digits_only)

    best = max(normalized, key=len) if normalized else None
    return best, text.strip()


def post_to_webhook(webhook_url, value, meta=None, timeout=10):
    """Send the captured value to the n8n webhook as JSON."""
    payload = {"value": value, "meta": meta or {}}
    response = requests.post(webhook_url, json=payload, timeout=timeout)
    response.raise_for_status()

    if response.headers.get("content-type", "").startswith("application/json"):
        return response.json()
    return {"status_code": response.status_code}


def main():
    parser = argparse.ArgumentParser(
        description="Capture screen, OCR numbers, send to n8n webhook."
    )
    parser.add_argument(
        "--webhook",
        help="n8n Webhook URL (POST). If omitted, will use WEBHOOK_URL env var.",
        default=os.getenv("WEBHOOK_URL"),
    )
    parser.add_argument(
        "--region",
        nargs=4,
        type=int,
        metavar=("LEFT", "TOP", "WIDTH", "HEIGHT"),
        help="Optional region to capture (pixels). Example: --region 100 200 600 300",
    )
    parser.add_argument(
        "--cooldown",
        type=float,
        default=0.0,
        help="Optional seconds to wait before capture (e.g., to hover menus)",
    )
    parser.add_argument(
        "--image", default="screenshot.png", help="Output image filename"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Only print OCR result, do not POST"
    )
    args = parser.parse_args()

    if not args.webhook and not args.dry_run:
        print("ERROR: Webhook URL not provided. Use --webhook or set WEBHOOK_URL env var.")
        sys.exit(2)

    if args.cooldown > 0:
        time.sleep(args.cooldown)

    region = None
    if args.region:
        left, top, width, height = args.region
        region = {"left": left, "top": top, "width": width, "height": height}

    path = grab_screenshot(region=region, out_path=args.image)
    value, raw_text = ocr_numbers(path)

    print("Raw OCR text:")
    print(raw_text)
    print("\nDetected number:", value if value else "(none)")
    meta = {
        "raw_text": raw_text,
        "image_path": os.path.abspath(path),
        "region": region,
        "platform": sys.platform,
    }

    if not args.dry_run and value:
        try:
            response = post_to_webhook(args.webhook, value, meta=meta)
            print("Posted to webhook. Response:", response)
        except Exception as exc:
            print("Failed to POST to webhook:", exc)
            sys.exit(3)
    elif not args.dry_run and not value:
        print("No numeric value detected; nothing posted.")
        sys.exit(4)


if __name__ == "__main__":
    main()
