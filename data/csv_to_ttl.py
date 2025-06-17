import csv
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS, DCTERMS, XSD

def csv_to_turtle(input_csv, output_ttl):
    # Initialize RDF Graph
    g = Graph()
    
    # Define namespaces
    ns = Namespace("http://contoh.org/ontology#")
    lexinfo = Namespace("http://www.lexinfo.net/ontology/2.0/lexinfo#")
    
    # Bind prefixes
    g.bind("", ns)
    g.bind("rdf", RDF)
    g.bind("rdfs", RDFS)
    g.bind("dcterms", DCTERMS)
    g.bind("lexinfo", lexinfo)
    g.bind("xsd", XSD)
    
    # Add manuscript declaration
    manuscript = ns.naskahSunda02
    g.add((manuscript, RDF.type, ns.Manuskrip))
    g.add((manuscript, DCTERMS.title, Literal("Carita Parahiyangan", lang="su")))
    g.add((manuscript, DCTERMS.alternative, Literal("Carita Parahyangan", lang="su")))
    g.add((manuscript, DCTERMS.creator, Literal("Anonim")))
    g.add((manuscript, DCTERMS.language, Literal("su")))
    g.add((manuscript, ns.ditulisMenggunakan, ns.AksaraCacarakan))
    g.add((manuscript, ns.periode, Literal("Abad ke-16")))
    g.add((manuscript, ns.lokasiPenyimpanan, Literal("Naskah koleksi pribadi")))
    
    # Add Aksara Cacarakan declaration
    g.add((ns.AksaraCacarakan, RDF.type, ns.SistemTulisan))
    g.add((ns.AksaraCacarakan, RDFS.label, Literal("Aksara Cacarakan", lang="id")))
    g.add((ns.AksaraCacarakan, ns.merupakanVarianDari, ns.AksaraJawa))
    
    # Process CSV file
    with open(input_csv, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Create URIs for each resource
            baris_uri = ns[row['id'].replace("-", "_")]
            aksara_uri = ns[f"aksara_{row['id'].replace('-', '_').lower()}"]
            translit_uri = ns[f"translit_{row['id'].replace('-', '_').lower()}"]
            terjemah_uri = ns[f"terjemah_{row['id'].replace('-', '_').lower()}"]
            
            # Add baris naskah triples
            g.add((baris_uri, RDF.type, ns.BarisNaskah))
            g.add((baris_uri, ns.isFromManuscript, manuscript))
            g.add((baris_uri, ns.mengandungAksara, aksara_uri))
            g.add((baris_uri, ns.hasTransliteration, translit_uri))
            g.add((baris_uri, ns.hasTranslation, terjemah_uri))
            g.add((baris_uri, ns.urutan, Literal(row['id'].split("-")[1][1:], datatype=XSD.integer)))
            g.add((baris_uri, DCTERMS.identifier, Literal(row['id'])))
            
            # Add aksara triples
            g.add((aksara_uri, RDF.type, ns.TeksAksara))
            g.add((aksara_uri, RDF.value, Literal(row['aksara'], lang="su-x-cacarakan")))
            g.add((aksara_uri, lexinfo.script, ns.AksaraCacarakan))
            g.add((aksara_uri, ns.jumlahKarakter, Literal(len(row['aksara']), datatype=XSD.integer)))
            
            # Add transliterasi triples
            g.add((translit_uri, RDF.type, ns.Transliterasi))
            g.add((translit_uri, RDF.value, Literal(row['transliterasi'], lang="su-Latn")))
            g.add((translit_uri, ns.menggunakanAturan, Literal("Aturan Transliterasi Cacarakan-Latin 2025")))
            
            # Add terjemahan triples
            g.add((terjemah_uri, RDF.type, ns.Terjemahan))
            g.add((terjemah_uri, RDF.value, Literal(row['terjemahan'], lang="id")))
            g.add((terjemah_uri, ns.keBahasa, Literal("id")))
            g.add((terjemah_uri, ns.dariBahasa, Literal("su")))
    
    # Serialize to Turtle format
    with open(output_ttl, 'w', encoding='utf-8') as ttlfile:
        ttlfile.write(g.serialize(format='turtle', encoding='utf-8').decode('utf-8'))

if __name__ == "__main__":
    # Example usage:
    csv_to_turtle('data.csv', 'output.ttl')
    print("Turtle files generated successfully!")