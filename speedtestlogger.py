import speedtest
import csv
import time
import datetime

def run_speed_test():
    global share_url 
    s = speedtest.Speedtest()

    # Select best server based on ping (optional)
    s.get_best_server()

    # Download/Upload speeds
    s.download()
    s.upload()

    # Results
    results_dict = s.results.dict()
    # Share results only if they exist and remove unnecessary share field before writing to csv
    if "share" in results_dict:
        share_url = results_dict.pop("share")

    return results_dict

with open("speedtest_log.csv", "a", newline="") as csvfile:
    fieldnames = ["Timestamp", "Download (Mbps)", "Upload (Mbps)", "Ping (ms)", 
                  "Server Name", "Client IP", "ISP", "Latitude", "Longitude", 
                  "Country", "Sponsor", "Host", "Share Results URL"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    if csvfile.tell() == 0:
        writer.writeheader()

    time_limit_seconds = 3600
    start_time = time.time()
    test_count = 0

    while time.time() - start_time < time_limit_seconds:
        results = run_speed_test()

        # Convert to Mbps and round
        download_mbps = round(results["download"] / 1000000, 2)
        upload_mbps = round(results["upload"] / 1000000, 2)
        ping_ms = round(results["ping"], 2)

        # Display results on screen
        print(f"\nTest {test_count + 1} results:")
        print(f"  Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  Download: {download_mbps} Mbps")
        print(f"  Upload: {upload_mbps} Mbps")
        print(f"  Ping: {ping_ms} ms")
        print(f"  Server: {results['server']['name']}")

        # Create a new dictionary with the correct field names
        csv_data = {
            "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Download (Mbps)": download_mbps,
            "Upload (Mbps)": upload_mbps,
            "Ping (ms)": ping_ms,
            "Server Name": results["server"]["name"],
            "Client IP": results["client"]["ip"],
            "ISP": results["client"]["isp"],
            "Latitude": results["server"]["lat"],
            "Longitude": results["server"]["lon"],
            "Country": results["server"]["country"],
            "Sponsor": results["server"]["sponsor"],
            "Host": results["server"]["host"],
            "Share Results URL": results.get("share", None) 
        }

        writer.writerow(csv_data)  # Write the modified dictionary
        time.sleep(300)
        test_count += 1

    print(f"\nCompleted {test_count} speed tests.")
