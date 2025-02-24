from datetime import timedelta


def timeToSeconds(time):
    hhmmss = time.split(",")[0]
    ms = time.split(",")[1]
    hh = hhmmss.split(":")[0]
    mm = hhmmss.split(":")[1]
    ss = hhmmss.split(":")[2]
    seconds = timedelta(
        hours=int(hh), minutes=int(mm), seconds=int(ss), milliseconds=int(ms)
    )
    return seconds.total_seconds()


def srt_to_transcript(filepath):
    srt = open(filepath, encoding="utf-8-sig").read().replace("\n\n", "\n").splitlines()
    grouped = [srt[i : i + 3] for i in range(0, len(srt), 3)]
    transcript = [
        (
            idx,
            timeToSeconds(times.split(" --> ")[0]),
            timeToSeconds(times.split(" --> ")[1]),
            speech.split(": ")[0],
            speech.split(": ")[1],
        )
        for idx, times, speech in grouped
        if timeToSeconds(times.split(" --> ")[1])
        > timeToSeconds(times.split(" --> ")[0])
    ]
    return transcript


def srt_to_lines(file):
    with open(file, "r") as f:
        srt = f.read().strip().replace("\n\n", "\n").splitlines()
    entries = [srt[i : i + 3] for i in range(0, len(srt), 3)]
    lines = [line for idx, timestamp, line in entries]
    return lines


def srt_to_text(file):
    with open(file, "r") as f:
        srt = f.read().strip().replace("\n\n", "\n").splitlines()
    entries = [srt[i : i + 3] for i in range(0, len(srt), 3)]
    lines = [line for idx, timestamp, line in entries]
    text = "\n".join(lines)
    return text


def secondsToTime(seconds):
    result = timedelta(seconds=seconds)
    string = (
        str(timedelta(seconds=result.seconds))
        + ","
        + str(int(result.microseconds / 1000))
    )
    return string


def transcript_to_srt(transcript):
    lines = [
        f"{idx}\n{secondsToTime(start)} --> {secondsToTime(end)}\n{speaker}: {speech}"
        for idx, start, end, speaker, speech in transcript
    ]
    return "\n\n".join(lines)


def labelTextTranscript(textTranscript, labels):
    labeled = []
    for line in textTranscript:
        speaker = line.split(":")[0]
        if not line.split(":")[1].isspace() and len(line.split(":")) > 1:
            labeled.append(line.replace(speaker, labels[speaker]))
    return labeled


def getTextTranscript(filepath):
    file = open(filepath, encoding="utf-8-sig").read().splitlines()

    lines = [line.rstrip() for line in file if line != ""]
    return lines


def parse_subtitle(line):
    idx, timestamp, dialogue = line
    start = timestamp.split(" --> ")[0]
    end = timestamp.split(" --> ")[1]
    speaker = dialogue.split(": ")[0]
    speech = dialogue.split(": ")[1]
    return (idx, timeToSeconds(start), timeToSeconds(end), speaker, speech)


def merge_srt(filepath):
    srt = open(filepath, encoding="utf-8-sig").read().replace("\n\n", "\n").splitlines()
    grouped = [srt[i : i + 3] for i in range(0, len(srt), 3)]
    merged = []
    idx, start, end, speaker, speech = parse_subtitle(grouped[0])
    prev_idx = None
    prev_start = None
    prev_end = None
    prev_speaker = None
    prev_speech = None
    for line in grouped:
        idx, start, end, speaker, speech = parse_subtitle(line)
        if speaker != prev_speaker:
            if prev_speech is not None:
                merged.append(
                    (prev_idx, prev_start, prev_end, prev_speaker, prev_speech)
                )
            prev_idx = idx
            prev_start = start
            prev_end = end
            prev_speaker = speaker
            prev_speech = speech
        elif speaker == prev_speaker:
            prev_end = end
            prev_speech = f"{prev_speech} {speech}"
    merged.append((prev_idx, prev_start, prev_end, prev_speaker, prev_speech))
    return merged
