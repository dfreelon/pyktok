from pathlib import Path
import shutil
import pyktok as pyk
import contextlib


def test_save_tiktok_browser_is_none():
    target_dir = Path(__file__).parent / 'files'  # define where the files will be saved: in tests/files/
    shutil.rmtree(target_dir, ignore_errors=True)  # make sure the 'target_dir' is empty
    target_dir.mkdir()

    # change the current dir to 'target_dir' while executing save_tiktok(),
    # so that the files are saved in 'target_dir' itself.
    with contextlib.chdir(target_dir):
        pyk.specify_browser(None)
        pyk.save_tiktok(
            video_url='https://www.tiktok.com/@tiktok/video/7106594312292453675',
            save_video=True,
            metadata_fn='video_data.csv',
        )

    assert (target_dir / 'video_data.csv').exists()
    assert (target_dir / '@tiktok_video_7106594312292453675.mp4').exists()
