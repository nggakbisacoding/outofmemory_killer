# Out Of Memory Killer
Out-Of-Memory adalah kejadian ketika nggak ada ruang lagi di ram. Meskipun pagefile kalian segede gaban juga nggak ngaruh, ngeswap kalau gede-gedean ya bikin lambat atau ngefreeze sekalian.<br/>
Semisal chrome kalian sering nggak responsif dan suspectnya karena abis ram, kalian bisa coba pake ini buat terminate program yang memory hogging.

## Usage

On Windows 10, you can open C:\Users\[username]\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup by entering shell:startup after pressing Win+R. Put a .bat file there containing python.exe -u "C:\Users\[username]\Documents\code\OOM_killer\oom_killer.py" to run it on startup.

Untuk proses background tanpa shell maka bisa menggunakan pythonw.exe -u "C:\Users\[username]\Documents\code\OOM_killer\OOM_killer.py" lalu save menggunakan nama .bat save ke C:\Users\[username]\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
