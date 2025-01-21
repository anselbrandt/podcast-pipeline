import nemo.collections.asr as nemo_asr

speaker_model = nemo_asr.models.EncDecSpeakerLabelModel.from_pretrained(
    "nvidia/speakerverification_en_titanet_large"
)

reference = "files/reference/john.wav"

sample = "/home/ansel/dev/podcast-pipeline/files/wavs/5_11.934_15.75_Speaker 0.wav"

result = speaker_model.verify_speakers(reference, sample)

print(result)
