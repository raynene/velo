# test_collect.py - 15-MINUTE TEST VERSION
import requests
import time
import json
from datetime import datetime
import os

URL = "https://portail-api-data.montpellier3m.fr/bikestation?limit=1000"
INTERVAL = 300  # 5 minutes for testing (not 20!)
MAX_CYCLES = 3  # Only 3 cycles = 15 minutes total

def main():
    print("🧪 STARTING GITHUB ACTIONS TEST (15 minutes)")
    print("=" * 50)
    
    all_data = []
    start_time = datetime.now()
    
    for cycle in range(MAX_CYCLES):
        try:
            # 1. Fetch data
            response = requests.get(URL, timeout=10)
            parkings = response.json()
            
            # 2. Add timestamp
            current_time = datetime.now()
            for parking in parkings:
                parking['collecte'] = {
                    'timestamp': current_time.isoformat(),
                    'heure': current_time.strftime('%H:%M:%S'),
                    'cycle': cycle + 1,
                    'test': True
                }
            
            # 3. Store
            all_data.extend(parkings)
            
            # 4. Log
            elapsed = (current_time - start_time).total_seconds() / 60
            print(f"✅ Cycle {cycle+1}/{MAX_CYCLES}: {len(parkings)} parkings at {current_time.strftime('%H:%M:%S')} (+{elapsed:.1f} min)")
            
            # 5. Wait (except last cycle)
            if cycle < MAX_CYCLES - 1:
                time.sleep(INTERVAL)
                
        except Exception as e:
            print(f"❌ Error cycle {cycle+1}: {e}")
            time.sleep(30)
    
    # 6. Save results
    if all_data:
        filename = "test_results.json"
        with open(filename, 'w') as f:
            json.dump(all_data, f, indent=2)
        
        print(f"\n💾 TEST SUCCESSFUL!")
        print(f"📊 Saved {len(all_data)} records to '{filename}'")
        print(f"⏱️  Total test duration: {(datetime.now() - start_time).total_seconds()/60:.1f} minutes")
        
        # Also create a simple summary file
        with open('test_summary.txt', 'w') as f:
            f.write(f"GitHub Actions Test - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write(f"Total records: {len(all_data)}\n")
            f.write(f"Parkings found: {len(set([p.get('name', {}).get('value', 'Unknown') for p in all_data]))}\n")
            f.write(f"Status: ✅ SUCCESS\n")
    
    else:
        print("❌ TEST FAILED: No data collected")
    
    return len(all_data)

if __name__ == "__main__":
    main()