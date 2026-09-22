"""Bounded, local-only media inspection. Does not perform ASR or content analysis."""
import argparse
import json
import math
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def run(args, timeout=60):
    result = subprocess.run(args, capture_output=True, timeout=timeout)
    if result.returncode:
        raise RuntimeError(result.stderr.decode('utf-8', errors='replace')[-1800:])
    return result.stdout


def inspect(source, output, count=12, times=None, audio=False):
    source = Path(source).resolve(strict=True)
    if not source.is_file():
        raise ValueError('Input must be a local file')
    output = Path(output).resolve()
    if output.exists():
        raise ValueError('Output directory already exists; choose a new directory')
    if not 1 <= count <= 120:
        raise ValueError('Frame count must be between 1 and 120')
    ffprobe, ffmpeg = shutil.which('ffprobe'), shutil.which('ffmpeg')
    if not ffprobe or not ffmpeg:
        raise ValueError('ffprobe and ffmpeg must be available on PATH')
    raw = json.loads(run([ffprobe, '-v', 'error', '-show_entries',
        'format=duration:stream=index,codec_type,codec_name,width,height,avg_frame_rate,duration',
        '-of', 'json', str(source)]))
    videos = [s for s in raw.get('streams', []) if s.get('codec_type') == 'video']
    if not videos:
        raise ValueError('No video stream found')
    duration = float(raw.get('format', {}).get('duration') or videos[0].get('duration') or 0)
    if not math.isfinite(duration) or duration <= 0:
        raise ValueError('A finite positive duration is required')
    if times is None:
        # Avoid the exact EOF. Requested times are not frame-accurate timestamps.
        end = max(0, duration - min(0.25, duration / 2))
        times = [end * i / (count - 1) for i in range(count)] if count > 1 else [0.0]
    if not 1 <= len(times) <= 120 or any(not math.isfinite(t) or t < 0 or t >= duration for t in times):
        raise ValueError('Supply 1–120 finite timestamps in [0, duration)')
    output.mkdir(parents=True, exist_ok=False)
    report = {'schema': 'chai.media-evidence.v1', 'source_name': source.name,
              'source_bytes': source.stat().st_size, 'generated_at': datetime.now(timezone.utc).isoformat(),
              'duration_seconds': duration, 'streams': raw.get('streams', []),
              'status': 'extracting', 'coverage': 'sampled_frames_only',
              'audio_understood': False, 'speech_transcribed': False,
              'timestamp_precision': 'requested seek seconds; not verified frame-accurate', 'errors': []}
    frames = []
    try:
        for i, timestamp in enumerate(times):
            name = f'frame_{i:03d}_{timestamp:.3f}s.png'
            run([ffmpeg, '-v', 'error', '-nostdin', '-n', '-ss', str(timestamp),
                 '-i', str(source), '-map', '0:v:0', '-frames:v', '1', str(output / name)])
            if not (output / name).is_file() or not (output / name).stat().st_size:
                raise RuntimeError(f'No frame decoded at {timestamp}')
            frames.append({'requested_seconds': timestamp, 'file': name, 'viewed': False})
        if audio:
            if any(s.get('codec_type') == 'audio' for s in raw.get('streams', [])):
                run([ffmpeg, '-v', 'error', '-nostdin', '-n', '-i', str(source),
                     '-map', '0:a:0', '-t', '900', '-vn', '-ac', '1', '-ar', '16000',
                     '-c:a', 'pcm_s16le', str(output / 'speech-audio.wav')], timeout=60)
                report['audio_export'] = {'file': 'speech-audio.wav', 'start': 0,
                                          'end': min(900, duration), 'truncated': duration > 900}
            else:
                report['audio_export'] = {'status': 'no_audio_stream'}
        report['status'] = 'extracted_not_reviewed'
    except Exception as exc:
        report['status'] = 'partial_extraction'
        report['errors'].append(str(exc))
        raise
    finally:
        (output / 'metadata.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
        (output / 'frames.json').write_text(json.dumps(frames, ensure_ascii=False, indent=2), encoding='utf-8')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input')
    parser.add_argument('--out', required=True)
    parser.add_argument('--count', type=int, default=12)
    parser.add_argument('--times', help='Comma-separated seek times in seconds')
    parser.add_argument('--audio', action='store_true')
    args = parser.parse_args()
    try:
        report = inspect(args.input, args.out, args.count,
                         [float(x) for x in args.times.split(',')] if args.times else None, args.audio)
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as exc:
        parser.exit(1, f'{exc}\n')
    print(json.dumps({'status': report['status'], 'duration_seconds': report['duration_seconds']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
