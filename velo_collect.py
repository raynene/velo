# velo_collect.py - FIXED VERSION
import requests
import time
import json
from datetime import datetime

URL = "https://portail-api-data.montpellier3m.fr/bikestation?limit=1000"
INTERVAL = 300
MAX_CYCLES = 3

def main():
    print("🚲 STARTING VÉLO PARKING COLLECTION")
    print("=" * 50)
    
    all_data = []
    start_time = datetime.now()
    
    for cycle in range(MAX_CYCLES):
        try:
            # Fetch vélo data
            response = requests.get(URL, timeout=10)
            
            # VÉLO API MIGHT RETURN DIFFERENT FORMAT!
            # Try different parsing approaches:
            if response.status_code == 200:
                try:
                    # Try parsing as JSON array
                    parkings = response.json()
                    
                    # If it's a single object, wrap it in a list
                    if isinstance(parkings, dict):
                        parkings = [parkings]
                    
                    # Add timestamp to EACH parking record
                    current_time = datetime.now()
                    for parking in parkings:
                        if isinstance(parking, dict):
                            parking['collecte'] = {
                                'timestamp': current_time.isoformat(),
                                'heure': current_time.strftime('%H:%M:%S'),
                                'cycle': cycle + 1
                            }
                            all_data.append(parking)
                    
                    elapsed = (current_time - start_time).total_seconds() / 60
                    print(f"✅ Cycle {cycle+1}/{MAX_CYCLES}: {len(parkings)} vélo parkings at {current_time.strftime('%H:%M:%S')} (+{elapsed:.1f} min)")
                    
                except Exception as e:
                    print(f"⚠️ JSON parsing error: {e}")
                    print(f"Raw response: {response.text[:200]}...")
            else:
                print(f"❌ HTTP Error: {response.status_code}")
            
            if cycle < MAX_CYCLES - 1:
                time.sleep(INTERVAL)
                
        except Exception as e:
            print(f"❌ Error cycle {cycle+1}: {type(e).__name__}: {e}")
            time.sleep(30)
    
    if all_data:
        filename = "velo_results.json"
        with open(filename, 'w') as f:
            json.dump(all_data, f, indent=2)
        
        print(f"\n💾 VÉLO COLLECTION SUCCESSFUL!")
        print(f"📊 Saved {len(all_data)} records to '{filename}'")
        
        # Count unique vélo stations
        unique_stations = len(set([p.get('id', '') for p in all_data if isinstance(p, dict)]))
        
        with open('velo_summary.txt', 'w') as f:
            f.write(f"Vélo Parking Test - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write(f"Total records: {len(all_data)}\n")
            f.write(f"Unique vélo stations: {unique_stations}\n")
            f.write(f"Status: ✅ SUCCESS\n")
        
        return len(all_data)
    
    else:
        print("❌ VÉLO COLLECTION FAILED: No data collected")
        
        # Create empty files to avoid workflow crash
        with open('velo_results.json', 'w') as f:
            json.dump([], f)
        
        with open('velo_summary.txt', 'w') as f:
            f.write("Vélo Parking Test - FAILED\n")
            f.write("Status: ❌ NO DATA COLLECTED\n")
            f.write("Check API format or connectivity\n")
        
        return 0

if __name__ == "__main__":
    main()

