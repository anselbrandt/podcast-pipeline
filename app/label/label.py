import argparse
import os
from pathlib import Path

from app.utils import (
    srt_to_transcript,
    transcript_to_srt,
    labelTextTranscript,
    getTextTranscript,
)
from .label_utils import getSpeakerLabels

ROOT = os.getcwd()


def label(input_dir: str, output_dir: str, reference_wav: str, hosts: list[str]):
    try:
        inputDir = Path(input_dir)
        wavs_dir = inputDir / "wavs"
        if not wavs_dir.is_dir():
            raise FileNotFoundError("wavs input directory does not exist")

        output_dir = os.path.join(ROOT, output_dir)
        os.makedirs(output_dir, exist_ok=True)

        srt_file = None
        txt_file = None

        for file in os.listdir(input_dir):
            file_path = os.path.join(input_dir, file)
            if os.path.isfile(file_path):
                if file.endswith(".srt"):
                    srt_file = file_path
                    txt_file = file_path.replace(".srt", ".txt")

        if not srt_file or not txt_file:
            raise FileNotFoundError(
                "srt and txt file must be present in the input directory."
            )

        wav_files = [
            os.path.join(wavs_dir, file)
            for file in os.listdir(wavs_dir)
            if ".wav" in file
        ]
        if not len(wav_files):
            raise FileNotFoundError("wav files must be present in <input dir>/wavs.")

        transcript = srt_to_transcript(srt_file)
        speakerLabels = getSpeakerLabels(reference_wav, wav_files, hosts)
        textTranscript = getTextTranscript(txt_file)
        labeledText = labelTextTranscript(textTranscript, speakerLabels)
        txt_outpath = os.path.join(output_dir, Path(txt_file).name)
        srt_outpath = os.path.join(output_dir, Path(srt_file).name)
        t = open(txt_outpath, "w")
        t.write("\n\n".join(labeledText))
        t.close
        labeled = [
            (idx, start, end, speakerLabels[speaker], speech)
            for idx, start, end, speaker, speech in transcript
        ]
        segments = [
            f"{idx}|{start}|{end}|{speaker}|{speech}"
            for idx, start, end, speaker, speech in labeled
        ]
        srt = transcript_to_srt(labeled)
        f = open(srt_outpath, "w")
        f.write(srt)
        f.close()
        segments_outpath = os.path.join(output_dir, "segments.txt")
        f = open(segments_outpath, "w")
        f.write("\n".join(segments))
        f.close()
    except Exception as error:
        print(error)


def main():
    parser = argparse.ArgumentParser(
        description="Label speaker segments with speaker names."
    )
    parser.add_argument(
        "input_dir", type=str, help="Directory containing input and wavs folder"
    )
    parser.add_argument(
        "output_dir", type=str, help="Directory to save labeled transcripts."
    )
    parser.add_argument(
        "reference_wav", type=str, help="Reference wav file for primary host."
    )
    parser.add_argument("hosts", nargs="+", help="Space separated hosts")

    args = parser.parse_args()

    label(args.input_dir, args.output_dir, args.reference_wav, args.hosts)


if __name__ == "__main__":
    main()
