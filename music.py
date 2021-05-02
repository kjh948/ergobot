import librosa 

# read audio file 
x, sr = librosa.load('Beyonce.mp3')

tempo, beat_times = librosa.beat.beat_track(x, sr=sr, start_bpm=60, units='time')

clicks = librosa.clicks(beat_times, sr=sr, length=len(x))
librosa.output.write_wav("out.wav",x + clicks, sr) 