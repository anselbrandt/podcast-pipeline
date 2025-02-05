import os
import argparse
from pathlib import Path
from pydub import AudioSegment
from app.utils.transcript import srt_to_transcript

ROOT = os.getcwd()


def split(input_dir: Path | str):
    try:
        output_dir = os.path.join(input_dir, "wavs")
        os.makedirs(output_dir, exist_ok=True)

        srt_file, mp3_file = None, None

        for file in os.listdir(input_dir):
            file_path = os.path.join(input_dir, file)
            if os.path.isfile(file_path):
                if file.endswith(".srt"):
                    srt_file = file_path
                elif file.endswith(".mp3"):
                    mp3_file = file_path

        if not srt_file or not mp3_file:
            raise FileNotFoundError(
                "Both .srt and .mp3 files must be present in the input directory."
            )

        transcript = srt_to_transcript(srt_file)
        audio = AudioSegment.from_file(mp3_file, format="mp3")
        duration = len(audio)
        segments = []

        for idx, start, end, speaker, speech in transcript:
            start_ms = int(start * 1000)
            end_ms = int(end * 1000)
            if start_ms < duration and end_ms < duration:
                segment = audio[start_ms:end_ms]
                output_path = os.path.join(
                    output_dir, f"{idx}_{start}_{end}_{speaker}.wav"
                )
                segments.append(f"{idx}|{start}|{end}|{speaker}|{speech}")
                segment.export(output_path, format="wav")

        segments_filepath = os.path.join(input_dir, Path(srt_file).stem + ".csv")

        f = open(segments_filepath, "w")
        f.write("\n".join(segments))
        f.close()

    except Exception as error:
        print(error)


def main():
    parser = argparse.ArgumentParser(
        description="Split MP3 files into segments using SRT timestamps."
    )
    parser.add_argument(
        "input_dir", type=str, help="Directory containing input .srt and .mp3 files."
    )

    args = parser.parse_args()

    split(args.input_dir)


if __name__ == "__main__":
    main()
