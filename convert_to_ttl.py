# convert_to_ttl.py
from rdflib import Graph

def convert_xml_to_ttl(input_file, output_file):
    g = Graph()
    g.parse(input_file, format='xml')
    g.serialize(destination=output_file, format='turtle')
    print(f"File berhasil dikonversi ke {output_file}")

if __name__ == "__main__":
    convert_xml_to_ttl('data/Cacarakan.xml', 'data/cacarakan.ttl')