#!/usr/bin/env python3
"""
Extract earthquake information from the last 7 days and plot seismicity on a map.

This script queries the USGS earthquake catalog for events from the past 7 days
and creates a map visualization showing:
- Earthquake locations (scatter plot)
- Magnitude represented by marker size
- Depth represented by color

Usage:
    python scripts/plot_earthquake_map.py

Optional arguments:
    --days DAYS         Number of days to look back (default: 7)
    --min-magnitude M   Minimum magnitude to include (default: 4.0)
    --output FILE       Output file for the map (default: earthquake_map.png)
    --demo              Use synthetic demo data instead of fetching real data

Requirements: obspy, matplotlib, numpy (see requirements.txt)
"""

from obspy import UTCDateTime
from obspy.clients.fdsn import Client
from obspy.clients.fdsn.header import FDSNNoServiceException
import matplotlib.pyplot as plt
import argparse
from datetime import datetime, timedelta
import numpy as np


def fetch_earthquakes(days=7, min_magnitude=4.0, client_name='USGS'):
    """
    Fetch earthquake events from the last N days.
    
    Parameters:
    -----------
    days : int
        Number of days to look back
    min_magnitude : float
        Minimum magnitude threshold
    client_name : str
        FDSN client name (default: 'USGS')
        
    Returns:
    --------
    catalog : obspy.core.event.Catalog
        Catalog of earthquake events
    """
    try:
        client = Client(client_name)
        endtime = UTCDateTime()
        starttime = endtime - days * 24 * 3600
        
        print(f"Fetching earthquakes from {starttime.isoformat()} to {endtime.isoformat()}")
        print(f"Minimum magnitude: {min_magnitude}")
        
        catalog = client.get_events(
            starttime=starttime,
            endtime=endtime,
            minmagnitude=min_magnitude
        )
        print(f"Found {len(catalog)} earthquakes")
        return catalog
    except FDSNNoServiceException as e:
        print(f"FDSN service error: {e}")
        print(f"The {client_name} service may be temporarily unavailable.")
        return None
    except Exception as e:
        print(f"Error fetching events: {e}")
        return None


def extract_earthquake_info(catalog):
    """
    Extract relevant information from earthquake catalog.
    
    Parameters:
    -----------
    catalog : obspy.core.event.Catalog
        Catalog of earthquake events
        
    Returns:
    --------
    dict : Dictionary containing lists of lats, lons, mags, depths, times
    """
    lats = []
    lons = []
    mags = []
    depths = []
    times = []
    
    for event in catalog:
        # Get preferred or first origin
        origin = event.preferred_origin() or (event.origins[0] if event.origins else None)
        if origin is None:
            continue
            
        # Get preferred or first magnitude
        magnitude = event.preferred_magnitude() or (event.magnitudes[0] if event.magnitudes else None)
        if magnitude is None:
            continue
        
        lats.append(origin.latitude)
        lons.append(origin.longitude)
        mags.append(magnitude.mag)
        # Depth in km (ObsPy stores in meters)
        depths.append(origin.depth / 1000.0 if origin.depth else 0)
        times.append(origin.time)
    
    return {
        'latitudes': lats,
        'longitudes': lons,
        'magnitudes': mags,
        'depths': depths,
        'times': times
    }


def generate_demo_data(days=7, min_magnitude=4.0, num_events=50):
    """
    Generate synthetic earthquake data for demonstration purposes.
    
    Parameters:
    -----------
    days : int
        Number of days to simulate
    min_magnitude : float
        Minimum magnitude
    num_events : int
        Number of synthetic events to generate
        
    Returns:
    --------
    dict : Dictionary containing synthetic earthquake data
    """
    print(f"\nGenerating {num_events} synthetic earthquake events for demonstration...")
    
    np.random.seed(42)  # For reproducibility
    
    # Generate earthquakes clustered around major seismic zones
    # Ring of Fire regions
    zones = [
        {'name': 'Japan', 'lat': 38, 'lon': 140, 'weight': 0.2},
        {'name': 'Indonesia', 'lat': -2, 'lon': 120, 'weight': 0.15},
        {'name': 'Chile', 'lat': -30, 'lon': -71, 'weight': 0.15},
        {'name': 'Alaska', 'lat': 61, 'lon': -150, 'weight': 0.1},
        {'name': 'California', 'lat': 36, 'lon': -120, 'weight': 0.1},
        {'name': 'New Zealand', 'lat': -41, 'lon': 174, 'weight': 0.1},
        {'name': 'Turkey', 'lat': 39, 'lon': 35, 'weight': 0.1},
        {'name': 'Peru', 'lat': -12, 'lon': -77, 'weight': 0.1},
    ]
    
    lats = []
    lons = []
    mags = []
    depths = []
    times = []
    
    for i in range(num_events):
        # Select a zone based on weights
        zone = np.random.choice(zones, p=[z['weight'] for z in zones])
        
        # Add random scatter around zone center
        lat = zone['lat'] + np.random.randn() * 3
        lon = zone['lon'] + np.random.randn() * 5
        
        # Generate magnitude following Gutenberg-Richter law (exponential distribution)
        mag = min_magnitude + np.random.exponential(0.8)
        mag = min(mag, 8.5)  # Cap at reasonable maximum
        
        # Depth generally increases with magnitude
        depth = np.random.exponential(30) + mag * 3
        depth = min(depth, 700)  # Cap at maximum subduction depth
        
        # Random time in the past N days
        time_offset = np.random.uniform(0, days * 24 * 3600)
        time = UTCDateTime() - time_offset
        
        lats.append(lat)
        lons.append(lon)
        mags.append(mag)
        depths.append(depth)
        times.append(time)
    
    print(f"Generated {num_events} synthetic events")
    
    return {
        'latitudes': lats,
        'longitudes': lons,
        'magnitudes': mags,
        'depths': depths,
        'times': times
    }


def plot_seismicity_map(earthquake_data, output_file='earthquake_map.png', days=7):
    """
    Create a map visualization of earthquake seismicity.
    
    Parameters:
    -----------
    earthquake_data : dict
        Dictionary with earthquake data (lats, lons, mags, depths)
    output_file : str
        Output filename for the map
    days : int
        Number of days covered (for title)
    """
    # Use simple matplotlib plotting (cartopy requires internet for map data)
    print("Using simplified matplotlib plotting...")
    fig, ax = plt.subplots(figsize=(15, 10))
    
    # Set up basic lat/lon plot
    ax.set_xlabel('Longitude (°)', fontsize=12)
    ax.set_ylabel('Latitude (°)', fontsize=12)
    ax.set_xlim(-180, 180)
    ax.set_ylim(-90, 90)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_aspect('equal', adjustable='box')
    ax.set_facecolor('lightblue')
    
    # Plot earthquakes
    # Size based on magnitude, color based on depth
    lats = earthquake_data['latitudes']
    lons = earthquake_data['longitudes']
    mags = earthquake_data['magnitudes']
    depths = earthquake_data['depths']
    
    # Scale marker sizes based on magnitude (exponential for visibility)
    sizes = [(10 ** (m - 2)) * 3 for m in mags]
    
    scatter = ax.scatter(
        lons, lats,
        c=depths,
        s=sizes,
        cmap='YlOrRd_r',  # Yellow (shallow) to Red (deep)
        alpha=0.7,
        edgecolors='black',
        linewidths=0.5,
        zorder=5
    )
    
    # Add colorbar for depth
    cbar = plt.colorbar(scatter, ax=ax, orientation='horizontal', pad=0.05, shrink=0.8)
    cbar.set_label('Depth (km)', fontsize=12)
    
    # Add title with statistics
    min_mag = min(mags) if mags else 0
    max_mag = max(mags) if mags else 0
    avg_mag = sum(mags) / len(mags) if mags else 0
    
    title = f'Global Seismicity - Last {days} Days\n'
    title += f'{len(lats)} earthquakes | Magnitude range: {min_mag:.1f}-{max_mag:.1f} (avg: {avg_mag:.1f})'
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    
    # Add legend for magnitude sizes
    legend_sizes = [4.0, 5.0, 6.0, 7.0]
    legend_markers = []
    for mag in legend_sizes:
        size = (10 ** (mag - 2)) * 3
        legend_markers.append(plt.scatter([], [], s=size, c='gray', alpha=0.6, 
                                         edgecolors='black', linewidths=0.5))
    
    legend_labels = [f'M {mag:.1f}' for mag in legend_sizes]
    legend = ax.legend(legend_markers, legend_labels, 
                      scatterpoints=1, title='Magnitude',
                      loc='lower left', frameon=True, fancybox=True)
    
    # Save figure
    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"\nMap saved to: {output_file}")
    
    # Also try to display (if interactive environment)
    try:
        plt.show()
    except Exception:
        # Silently ignore display errors (e.g., no display available)
        pass
    
    plt.close()


def print_summary(earthquake_data):
    """Print a summary of the earthquake data."""
    if not earthquake_data['magnitudes']:
        print("\nNo earthquake data to summarize.")
        return
    
    print("\n" + "="*60)
    print("EARTHQUAKE SUMMARY")
    print("="*60)
    print(f"Total events: {len(earthquake_data['magnitudes'])}")
    print(f"Magnitude range: {min(earthquake_data['magnitudes']):.1f} - {max(earthquake_data['magnitudes']):.1f}")
    print(f"Average magnitude: {sum(earthquake_data['magnitudes'])/len(earthquake_data['magnitudes']):.2f}")
    print(f"Depth range: {min(earthquake_data['depths']):.1f} - {max(earthquake_data['depths']):.1f} km")
    print(f"Average depth: {sum(earthquake_data['depths'])/len(earthquake_data['depths']):.1f} km")
    
    # Show top 5 largest earthquakes
    if len(earthquake_data['magnitudes']) > 0:
        print("\nTop 5 largest earthquakes:")
        # Create list of tuples and sort by magnitude
        events = list(zip(
            earthquake_data['magnitudes'],
            earthquake_data['latitudes'],
            earthquake_data['longitudes'],
            earthquake_data['depths'],
            earthquake_data['times']
        ))
        events.sort(reverse=True)
        
        for i, (mag, lat, lon, depth, time) in enumerate(events[:5], 1):
            print(f"  {i}. M{mag:.1f} - Lat: {lat:.2f}°, Lon: {lon:.2f}°, "
                  f"Depth: {depth:.1f} km - {time.isoformat()}")
    print("="*60 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description='Extract and plot earthquake information from the last N days'
    )
    parser.add_argument(
        '--days', type=int, default=7,
        help='Number of days to look back (default: 7)'
    )
    parser.add_argument(
        '--min-magnitude', type=float, default=4.0,
        help='Minimum magnitude to include (default: 4.0)'
    )
    parser.add_argument(
        '--output', type=str, default='earthquake_map.png',
        help='Output file for the map (default: earthquake_map.png)'
    )
    parser.add_argument(
        '--client', type=str, default='USGS',
        help='FDSN client to use (default: USGS)'
    )
    parser.add_argument(
        '--demo', action='store_true',
        help='Use synthetic demo data instead of fetching real data'
    )
    
    args = parser.parse_args()
    
    print("="*60)
    print("EARTHQUAKE SEISMICITY MAPPER")
    print("="*60)
    
    earthquake_data = None
    
    if args.demo:
        # Use synthetic data
        earthquake_data = generate_demo_data(
            days=args.days,
            min_magnitude=args.min_magnitude,
            num_events=50
        )
    else:
        # Fetch real earthquake catalog
        catalog = fetch_earthquakes(
            days=args.days,
            min_magnitude=args.min_magnitude,
            client_name=args.client
        )
        
        if catalog is None:
            print("\n" + "="*60)
            print("Failed to fetch earthquake data from the server.")
            print("This could be due to:")
            print("  - Network connectivity issues")
            print("  - Temporary service outage")
            print("  - Firewall or proxy restrictions")
            print("\nYou can try:")
            print("  1. Run with --demo flag to see synthetic data")
            print("  2. Try a different client with --client IRIS")
            print("  3. Check your internet connection")
            print("="*60)
            return
        
        if len(catalog) == 0:
            print("No earthquakes found. Try adjusting parameters or use --demo mode.")
            return
        
        # Extract earthquake information
        earthquake_data = extract_earthquake_info(catalog)
    
    # Print summary
    print_summary(earthquake_data)
    
    # Create map
    print("Creating seismicity map...")
    plot_seismicity_map(earthquake_data, output_file=args.output, days=args.days)
    
    print("\nDone!")


if __name__ == '__main__':
    main()
