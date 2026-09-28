import json, sys
tpl, data_file, caption, out = sys.argv[1:5]
d = json.load(open(data_file)); d["caption"] = caption
blob = json.dumps(d, separators=(",", ":")).replace("<", "\\u003c")
open(out, "w").write(open(tpl).read().replace("/*DATA*/", blob))
print(out, len(blob) // 1024, "KB of data")
