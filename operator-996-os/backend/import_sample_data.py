"""
One-click sample data importer for demos and testing
Usage: python import_sample_data.py
"""
import requests
import json
from pathlib import Path


def import_sample_events():
    """Import sample behavioral events from sample_events.json into the API."""
    sample_file = Path(__file__).parent / "sample_events.json"
    
    if not sample_file.exists():
        print("❌ Error: sample_events.json not found")
        return
    
    with open(sample_file, 'r') as f:
        data = json.load(f)
    
    api_base = "http://localhost:8000"
    
    # Check if API is available
    try:
        health_response = requests.get(f"{api_base}/health", timeout=5)
        if health_response.status_code != 200:
            print(f"❌ Error: API not responding at {api_base}")
            return
        print(f"✓ Connected to Operator-996 Cognitive OS at {api_base}\n")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: Cannot connect to API at {api_base}")
        print(f"   Make sure the backend is running: docker-compose up -d")
        print(f"   Details: {e}")
        return
    
    imported_count = 0
    failed_count = 0
    
    events = data.get('behavioral_events', [])
    total = len(events)
    
    print(f"📦 Importing {total} behavioral events...\n")
    
    for i, event in enumerate(events, 1):
        try:
            response = requests.post(f"{api_base}/event/add", json=event, timeout=10)
            if response.status_code == 200:
                desc = event['description'][:50] + '...' if len(event['description']) > 50 else event['description']
                print(f"✅ [{i}/{total}] {event['event_type'].upper()}: {desc}")
                imported_count += 1
            else:
                print(f"⚠️  [{i}/{total}] Failed: {event['description'][:40]}... (Status: {response.status_code})")
                failed_count += 1
        except requests.exceptions.RequestException as e:
            print(f"❌ [{i}/{total}] Error: {event['description'][:40]}... ({e})")
            failed_count += 1
    
    print(f"\n{'='*60}")
    print(f"🎉 Successfully imported {imported_count} events!")
    if failed_count > 0:
        print(f"⚠️  Failed to import {failed_count} events")
    print(f"{'='*60}\n")
    
    print("📊 Next steps:")
    print("   🔍 Run pattern detection: POST /patterns/detect")
    print("   🔎 Run anomaly scan: POST /anomalies/detect")
    print("   🌐 Open dashboard: http://localhost:3000")
    print("   📡 API docs: http://localhost:8000/docs")


if __name__ == "__main__":
    import_sample_events()
