# pyktok ARM64 Compatibility

This document provides instructions for using pyktok on ARM64 architecture (Raspberry Pi 4/5) where the original version fails with SIGILL (Illegal instruction) errors.

## Problem Description

The original pyktok package includes dependencies (Playwright and TikTokApi) that contain pre-compiled binaries optimized for ARMv8.1-A or newer architectures. These binaries use instructions like `ldaddal` that are not supported by the ARMv8-A Cortex-A72 processor in Raspberry Pi 4, causing SIGILL errors.

## Solution

This ARM64-compatible version replaces the problematic dependencies with Selenium-based alternatives that work on ARM64 architecture.

### Key Changes

1. **Replaced Playwright** with Selenium WebDriver
2. **Replaced TikTokApi** with direct web scraping using Selenium
3. **Updated User-Agent** to ARM64-specific string
4. **Added ARM64-specific Chrome options** for better compatibility

## Installation

### Quick Installation

Run the provided installation script:

```bash
./install_arm64.sh
```

### Manual Installation

1. **Install system dependencies:**
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-dev python3-venv chromium-browser chromium-chromedriver wget curl build-essential libssl-dev libffi-dev libxml2-dev libxslt1-dev zlib1g-dev
```

2. **Create virtual environment:**
```bash
python3 -m venv pyktok_arm64_env
source pyktok_arm64_env/bin/activate
```

3. **Install Python packages:**
```bash
pip install --upgrade pip
pip install --no-binary :all: beautifulsoup4 browser-cookie3 numpy pandas requests streamlit selenium webdriver-manager
```

4. **Install pyktok ARM64 version:**
```bash
pip install -e .
```

## Usage

### Basic Usage

```python
# Import the ARM64-compatible version
from pyktok import pyktok_arm64 as pyktok

# Specify browser for cookie extraction
pyktok.specify_browser('chrome')

# Download a single TikTok video
pyktok.save_tiktok('https://www.tiktok.com/@username/video/1234567890', 
                   save_video=True, 
                   metadata_fn='metadata.csv')

# Download multiple videos from a user
pyktok.save_tiktok_multi_page('username', 
                              ent_type='user', 
                              video_ct=10, 
                              save_video=True, 
                              metadata_fn='user_videos.csv')
```

### Available Functions

The ARM64 version provides the same API as the original pyktok with these functions:

- `save_tiktok()` - Download single video and metadata
- `save_tiktok_multi_urls()` - Download multiple videos from URL list
- `save_tiktok_multi_page()` - Download videos from user/hashtag page
- `save_tiktok_comments()` - Download video comments
- `get_video_urls_selenium()` - Get video URLs using Selenium
- `get_comments_selenium()` - Get comments using Selenium
- `get_user_data_selenium()` - Get user data using Selenium

### Browser Requirements

The ARM64 version requires Chrome or Chromium to be installed:

```bash
# On Raspberry Pi OS
sudo apt install chromium-browser chromium-chromedriver

# Or install Chrome manually
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt update
sudo apt install google-chrome-stable
```

## Troubleshooting

### Common Issues

1. **Chrome/Chromium not found:**
   - Ensure Chrome or Chromium is installed
   - Check that chromedriver is in PATH
   - Use `webdriver-manager` to auto-install drivers

2. **Permission errors:**
   - Run with `--no-sandbox` flag (already included)
   - Ensure proper file permissions for download directory

3. **Memory issues:**
   - Use `--disable-dev-shm-usage` flag (already included)
   - Reduce video count for large batches

### Performance Notes

- Selenium-based scraping is slower than Playwright/TikTokApi
- Consider reducing `video_ct` for large batches
- Use `headless=True` for better performance
- Add appropriate sleep delays between requests

## Limitations

1. **Slower performance** compared to original version
2. **More resource intensive** due to browser automation
3. **Limited to basic TikTok scraping** (no advanced API features)
4. **Requires Chrome/Chromium** installation

## Alternative Solutions

If you continue to experience issues:

1. **Use Docker with x86_64 emulation:**
```bash
docker run --platform linux/amd64 -it python:3.10-slim
```

2. **Compile from source:**
```bash
pip install --no-binary :all: playwright
playwright install chromium
```

3. **Use alternative TikTok scraping libraries** that are ARM64 compatible

## Support

For issues specific to ARM64 compatibility, please check:
- Raspberry Pi OS compatibility
- Chrome/Chromium installation
- System memory and resources
- Network connectivity

## License

Same as original pyktok package (BSD License).
