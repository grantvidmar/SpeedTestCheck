import speedtest
import datetime
import time

log_file = "speedtest_log.txt"

def run_speed_test():
    s = speedtest.Speedtest()
    s.get_best_server()
    s.download()
    s.upload()
    return s.results.dict()

time_limit_seconds = 180  # 3 minutes
start_time = time.time()
test_count = 0

with open(log_file, "a") as logfile:
    while time.time() - start_time < time_limit_seconds:
        results = run_speed_test()

        # Format the output
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        download_mbps = round(results["download"] / 1000000, 2)
        upload_mbps = round(results["upload"] / 1000000, 2)
        ping_ms = round(results["ping"], 2)

        log_entry = f"""
--------------------------------
Test {test_count + 1} Results - {timestamp}
--------------------------------
Download: {download_mbps} Mbps
Upload: {upload_mbps} Mbps
Ping: {ping_ms} ms
Server: {results['server']['name']}
Client IP: {results['client']['ip']}
ISP: {results['client']['isp']}
Location: {results['server']['lat']}, {results['server']['lon']} ({results['server']['country']})
Sponsor: {results['server']['sponsor']}
Host: {results['server']['host']}
Share Results: {results.get("share", "Not Available")}
"""
        # Print to console and write to file
        print(log_entry)
        logfile.write(log_entry)

        time.sleep(30)  # Wait for 30 seconds
        test_count += 1

    print(f"\nCompleted {test_count} speed tests. Logs saved to {log_file}")
