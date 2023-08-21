import os, subprocess, sys, time  # nosec

import psutil  # python -m pip install psutil


MIN_BYTES_FREE = 0.36e9  # Windows 10 and/or Chrome appear to fill the disk rather than put free RAM below 20 MB of 12 GB. 128 MB is also hard to hit. 250e6 works. 404e6 for Mint Cinnamon. 550e6 for Windows 10 when MsMpEng is hogging all resources. 1e9 for temporary blackouts with 100% pagefile use by memcompression instead of nonresponsive Chrome with 16 - 1.1 GB RAM.
KILL_UNTIL_BYTES_FREE = 1.4e9  # Kill until
MAX_BYTES_PROCESS = 390e6  # Kills tabs bigger than this. TODO: Don't kill focused tab.

# Lowercase list of process names that don't need confirmation to be killed.
HIT_LIST = [
	"procmon64",
	"chrome",
	"chromium",
	"firefox",
	"web content",
	"isolated web co",
	"microsoftedgecp",
	"msedge",
	"msmpeng",
	"node",
	"python",
	"python3",
]


def kill(pid):
	if os.name == "nt":
		print(
			subprocess.check_output(["TASKKILL", "/PID", str(pid), "/T", "/F"])  # nosec
		)  # /Tree /Force. /IM image didn't work though all child processes were named the same.
	else:
		os.kill(
			pid, 15
		)  # 15 is SIGTERM according to https://en.wikipedia.org/wiki/Signal_(IPC) which is friendlier than SIGKILL (9). On Windows this is just the exit code for the process.


def main(verbose=True):
	lines = __doc__.splitlines()
	print(lines[0], lines[-1])
	print(
		f"Watching {HIT_LIST}\nIf free RAM < {MIN_BYTES_FREE/1e9:,.2f} GB, kill until {KILL_UNTIL_BYTES_FREE/1e9:,.2f} GB free."
	)

	while True:
		time.sleep(4)
		try:
			ram_free = psutil.virtual_memory().available
			if verbose or ram_free < MIN_BYTES_FREE:
				print(f"\n{time.ctime()}   {ram_free / 1e9:,.2f} GB free:")
				if psutil.disk_usage('/').free < 1e9:
					print("WARNING: Less than 1 GB HDD free. Check downloads.")
				proc_data = [
					(
						p.memory_info().rss,
						p.pid,
						p.name().split(".")[0].lower(),
						p.parent() and p.parent().name().split(".")[0].lower() or None,
					)
					for p in psutil.process_iter()
				]
				proc_data.sort(reverse=True)
				print(
					"   ".join(f"{p[2]} {p[0] / 1e6:,.2f} MB" for p in proc_data[:5])
				)
				if ram_free >= MIN_BYTES_FREE:
					continue
				if "pcdrmemory" in " ".join(p[2] for p in proc_data):
					print("Allowing pcdrmemory test.")
					continue
				skipped = []
				for rss, pid, name, parent in proc_data:
					if (
						# rss > MAX_BYTES_PROCESS and
						ram_free < KILL_UNTIL_BYTES_FREE
						and name in HIT_LIST
					):
						if parent != name and name not in skipped: # and name in ("chrome", "firefox", "msedge"):
							print("Skipping main", name)
							skipped.append(name)
							continue
						print(
							f"\7Killing {rss/1e6:,.2f} MB {name} {pid} of {parent} on {time.ctime()}"
						)
						kill(pid)
						time.sleep(4)
						ram_free = psutil.virtual_memory().available
						print(f"Free RAM: {ram_free / 1e9:,.2f} GB")
		except Exception as ex:
			print(type(ex).__name__, ex, f"on line {sys.exc_info()[2].tb_lineno}")


if __name__ == "__main__":
	try:
		main("verbose" in sys.argv)
	except KeyboardInterrupt:
		pass  # Normal user exit by Ctrl+Break or Ctrl+C.
