import yt_dlp

def list_formats(url):
    print("\n🔍 Fetching available formats...\n")
    ydl_opts = {'quiet': True}
    formats_list = []

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        print(f"🎬 Title: {info['title']}\n")
        formats = info.get('formats', [])

        print("{:<5} {:<10} {:<10} {:<8} {}".format("No", "Format ID", "Ext", "Res", "Note"))
        print("-" * 50)
        for i, f in enumerate(formats):
            resolution = f.get('height') or 'audio'
            note = f.get('format_note') or ''
            print("{:<5} {:<10} {:<10} {:<8} {}".format(
                i, f['format_id'], f['ext'], resolution, note
            ))
            formats_list.append((f['format_id'], f['ext'], resolution))

    return formats_list

def download_selected_format(url, format_id):
    ydl_opts = {
        'format': format_id,
        'outtmpl': '%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
    }

    print("\n⬇️  Downloading selected format...\n")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def main():
    print("🎥 YouTube Downloader with Format Selection\n")
    url = input("📎 Enter YouTube video URL: ").strip()

    formats = list_formats(url)

    print("\n✅ You can choose any of the above formats to download.")
    try:
        choice_index = int(input("🔢 Enter the format number to download: "))
        format_id = formats[choice_index][0]
    except (ValueError, IndexError):
        print("❌ Invalid choice. Exiting.")
        return

    download_selected_format(url, format_id)
    print("\n✅ Download complete!")

if __name__ == "__main__":
    main()
