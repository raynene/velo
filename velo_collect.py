


# velo_collect.py - VÉLO VERSION
import requests
import time
import json
from datetime import datetime
import os

# ONLY THIS LINE CHANGES:
URL = "https://portail-api-data.montpellier3m.fr/bikestation?limit=1000"  # ← VÉLO API
INTERVAL = 300  # 5 minutes
MAX_CYCLES = 3  # 15 minutes total

def main():
    print("🚲 STARTING VÉLO PARKING COLLECTION")
    print("=" * 50)
    
    all_data = []
    start_time = datetime.now()
    
    for cycle in range(MAX_CYCLES):
        try:
            # Fetch VÉLO data
            response = requests.get(URL, timeout=10)
            velo_parkings = response.json()
            
            # Add timestamp
            current_time = datetime.now()
            for parking in velo_parkings:
                parking['collecte'] = {
                    'timestamp': current_time.isoformat(),
                    'heure': current_time.strftime('%H:%M:%S'),
                    'cycle': cycle + 1,
                    'test': True
                }
            
            all_data.extend(velo_parkings)
            
            elapsed = (current_time - start_time).total_seconds() / 60
            print(f"✅ Cycle {cycle+1}/{MAX_CYCLES}: {len(velo_parkings)} vélo parkings at {current_time.strftime('%H:%M:%S')} (+{elapsed:.1f} min)")
            
            if cycle < MAX_CYCLES - 1:
                time.sleep(INTERVAL)
                
        except Exception as e:
            print(f"❌ Error cycle {cycle+1}: {e}")
            time.sleep(30)
    
    if all_data:
        filename = "velo_results.json"
        with open(filename, 'w') as f:
            json.dump(all_data, f, indent=2)
        
        print(f"\n💾 VÉLO COLLECTION SUCCESSFUL!")
        print(f"📊 Saved {len(all_data)} records to '{filename}'")
        
        # VÉLO summary file
        with open('velo_summary.txt', 'w') as f:
            f.write(f"Vélo Parking Test - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write(f"Total records: {len(all_data)}\n")
            f.write(f"Vélo parkings found: {len(set([p.get('name', {}).get('value', 'Unknown') for p in all_data]))}\n")
            f.write(f"Status: ✅ SUCCESS\n")
    
    else:
        print("❌ VÉLO COLLECTION FAILED: No data collected")
    
    return len(all_data)

if __name__ == "__main__":
    main()
    main()
