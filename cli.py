import requests
# launch with command: uvicorn main_api:app --reload
BASE = "http://127.0.0.1:8000/"

print(requests.get(f"{BASE}/start", json={"mode": "1p"}).json())

while True:
    cmd = input(">> ").strip()

    if cmd == "state":
        print(requests.get(f"{BASE}/state").json())

    elif cmd.startswith("move"):
        _, start, end = cmd.split()
        r = requests.post(f"{BASE}/move", json={"start": start, "end": end})

        print(r.json())

    elif cmd == "quit":
        break