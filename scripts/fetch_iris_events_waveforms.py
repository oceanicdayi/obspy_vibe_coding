#!/usr/bin/env python3
"""
Fetch recent events from IRIS FDSN and download waveform data.

功能：
- 查詢最近 N 天（預設 5 天）規模大於某值（預設 5.0）的地震事件
- 列出事件讓使用者選擇（也支援 `--select all`）
- 針對選定事件下載波形資料（預設使用 IRIS），並可選擇僅下載台灣區域（bounding box）的觀測站波形

使用：
    python scripts/fetch_iris_events_waveforms.py

需求：`obspy`（見 requirements.txt）
"""
from obspy import UTCDateTime
from obspy.clients.fdsn import Client
import argparse
import os
import sys
from datetime import timedelta


TW_BBOX = dict(minlatitude=21.5, maxlatitude=25.5, minlongitude=119.0, maxlongitude=123.5)


def find_events(client, days=5, min_magnitude=5.0):
    endtime = UTCDateTime()
    starttime = endtime - days * 24 * 3600
    print(f"Searching events from {starttime.isoformat()} to {endtime.isoformat()} (M>{min_magnitude})")
    events = client.get_events(starttime=starttime, endtime=endtime, minmagnitude=min_magnitude)
    return events


def pick_origin(event):
    # choose preferred origin (first one)
    if len(event.origins) > 0:
        return event.origins[0]
    return None


def pick_magnitude(event):
    if len(event.magnitudes) > 0:
        return event.magnitudes[0]
    return None


def list_events(events):
    if len(events) == 0:
        print("No events found.")
        return
    print("Found events:")
    for i, ev in enumerate(events):
        mag = pick_magnitude(ev)
        org = pick_origin(ev)
        magv = mag.mag if mag is not None else "?"
        timev = org.time.isoformat() if org is not None else "?"
        lat = getattr(org, 'latitude', '?')
        lon = getattr(org, 'longitude', '?')
        depth = getattr(org, 'depth', '?')
        print(f"[{i}] time={timev} M={magv} lat={lat} lon={lon} depth(m)={depth}")


def download_for_event(client, event, out_dir, tw_only=False, before=60, after=600, max_files=0, saved_count=0, channels_prefix=('BHZ','BHN','BHE')):
    org = pick_origin(event)
    if org is None:
        print("Event has no origin, skipping.")
        return []
    t0 = org.time
    starttime = t0 - before
    endtime = t0 + after

    if not os.path.isdir(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    # get stations inventory
    if tw_only:
        inv = client.get_stations(starttime=starttime, endtime=endtime, level='response', **TW_BBOX)
    else:
        inv = client.get_stations(starttime=starttime, endtime=endtime, level='response')

    saved_files = []
    for net in inv:
        for sta in net:
            station_code = sta.code
            network_code = net.code
            location = None
            # collect channel codes to try
            channel_codes = set()
            for ch in sta.channels:
                channel_codes.add(ch.code)

            for ch in sorted(channel_codes):
                # optional: limit to channels starting with BH (broadband)
                if not ch.startswith('BH'):
                    continue
                try:
                    st = client.get_waveforms(network_code, station_code, '', ch, starttime, endtime)
                    if len(st) == 0:
                        continue
                    fname = os.path.join(out_dir, f"{event.resource_id.id.replace(':','_')}_{network_code}.{station_code}.{ch}.mseed")
                    st.write(fname, format='MSEED')
                    saved_files.append(fname)
                    saved_count += 1
                    if max_files and saved_count <= max_files:
                        print(f"Saved {fname} ({saved_count}/{max_files})")
                    else:
                        print(f"Saved {fname} ({saved_count})")
                    # stop if we've reached the requested total
                    if max_files and saved_count >= max_files:
                        return saved_files, saved_count
                except Exception as e:
                    # network/station may not have data for that time/channel
                    # keep going
                    continue

    return saved_files, saved_count


def main():
    parser = argparse.ArgumentParser(description='Fetch IRIS events and download waveforms (optional TW bounding box).')
    parser.add_argument('--days', type=int, default=5, help='Lookback window in days')
    parser.add_argument('--min-magnitude', type=float, default=5.0, help='Minimum magnitude')
    parser.add_argument('--tw-only', action='store_true', help='Only download stations within Taiwan bounding box')
    parser.add_argument('--before', type=int, default=60, help='Seconds before origin to start waveform')
    parser.add_argument('--after', type=int, default=600, help='Seconds after origin to end waveform')
    parser.add_argument('--out', default='data', help='Output folder')
    parser.add_argument('--select-all', action='store_true', help='Automatically select all found events')
    parser.add_argument('--first-only', action='store_true', help='Automatically select only the first found event')
    parser.add_argument('--max-files', type=int, default=0, help='Maximum number of waveform files to download in total (0 = unlimited)')
    parser.add_argument('--no-waveforms', action='store_true', help='Only list found events and exit; do not download waveforms')
    args = parser.parse_args()

    client = Client('IRIS')
    events = find_events(client, days=args.days, min_magnitude=args.min_magnitude)
    if len(events) == 0:
        print('No events found. Exiting.')
        sys.exit(0)

    list_events(events)

    if args.no_waveforms:
        print('No-waveforms mode enabled: not downloading any waveform files. Exiting.')
        sys.exit(0)

    if args.select_all:
        indices = list(range(len(events)))
    elif args.first_only:
        indices = [0]
        print('Selected first event only (index 0).')
    else:
        sel = input('Select event index (comma separated), or "all": ').strip()
        if sel.lower() in ('all', 'a'):
            indices = list(range(len(events)))
        else:
            try:
                indices = [int(x) for x in sel.split(',') if x.strip()!='']
            except Exception:
                print('Invalid selection. Exiting.')
                sys.exit(1)

    os.makedirs(args.out, exist_ok=True)

    downloaded = []
    saved_count = 0
    for idx in indices:
        if idx < 0 or idx >= len(events):
            print(f'Skipping invalid index {idx}')
            continue
        ev = events[idx]
        print(f"Downloading waveforms for event {idx}...")
        files, saved_count = download_for_event(client, ev, out_dir=args.out, tw_only=args.tw_only, before=args.before, after=args.after, max_files=args.max_files, saved_count=saved_count)
        downloaded.extend(files)
        # stop if we've reached max-files
        if args.max_files and saved_count >= args.max_files:
            print(f"Reached max-files limit ({args.max_files}). Stopping.")
            break

    if len(downloaded) == 0:
        print('No waveform files were downloaded. Consider widening time window or disabling --tw-only.')
    else:
        print(f'Downloaded {len(downloaded)} files into {args.out}')


if __name__ == '__main__':
    main()
