import yaml
import json
import io



class jsonyaml():
    def __init__(self):
        self.data = None
        self.datatype = None

    def load(self, fname):
        with io.open(fname, "r") as f:
            if ".json" in fname:
                self.data = json.load(f)
                self.datatype = "json"

            elif ".yaml" in fname:
                self.data = yaml.safe_load(f)
                self.datatype = "json"

    def save(self, outfile):
        if not self.datatype == None:
            with io.open(outfile, "w") as out:
                if self.datatype == "json":
                    yaml.dump(self.data, out, default_flow_style=False, allow_unicode=True, indent=4)

                elif self.datatype == "yaml":
                    json.dump(self.data, out, indent=4)

        else:
            print("jsonyaml: No file loaded."); exit()

    def getdata(self):
        if not self.datatype == None:
            return self.data
            
        else:
            print("jsonyaml: No file loaded."); exit()

    def convert(self, infile, outfile):
        self.load(infile)
        self.save(outfile)

#converter = jsonyaml()

#converter.convert("dandere2x_linux.json", "dandere2x_linux.yaml")
