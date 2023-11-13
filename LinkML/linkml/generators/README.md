# LinkML representation generators

| command line | module | Generator name | function | help file |
| -----------  | ------ | -------------  | -------- | --------- |
|  gen-yaml    | [yamlgen.py](https://github.com/linkml/linkml/blob/main/linkml/generators/yamlgen.py) | YamlGenerator | Validate YAML or emit compiled module | [yamlgen help](../../tests/test_scripts/output/genyaml/help) |
|  gen-jsonld-context   | [jsonldcontextgen.py](https://github.com/linkml/linkml/blob/main/linkml/generators/jsonldcontextgen.py) |    ContextGenerator | generate a JSON-LD @context block  | [contextgen help](../../tests/test_scripts/output/gencontext/help) |
|  gen-csv   | [csvgen.py](https://github.com/linkml/linkml/blob/main/linkml/generators/csvgen.py) |    CsvGenerator | generate a csv summary  | [csvgen help](../../tests/test_scripts/output/gencsv/help) |
|  gen-graphviz   | [dotgen.py](https://github.com/linkml/linkml/blob/main/linkml/generators/dotgen.py) |    DotGenerator | generate graphviz representation  | [dotgen help](../../tests/test_scripts/output/gengraphviz/help) |
|  gen-golang   | [golanggen.py](https://github.com/linkml/linkml/blob/main/linkml/generators/golanggen.py) |    GolangGenerator | generate Golang representation  | [golanggen help](../../tests/test_scripts/output/gengolang/help) |
|  gen-golr-views   | [golrgen.py](https://github.com/linkml/linkml/blob/main/linkml/generators/golrgen.py) |    GolrSchemaGenerator | generate a GOLR(?) representation  | [golrgen help](../../tests/test_scripts/output/genglor/help) |
|  gen-graphql   | [graphqlgen.py](https://github.com/linkml/linkml/blob/main/linkml/generators/graphqlgen.py) |    GraphqlGenerator | generate a graphql representation  | [graphql help](../../tests/test_scripts/output/gengraphql/help) |
|  gen-proto  | [protogen.py](https://github.com/linkml/linkml/blob/main/linkml/generators/protogen.py) | ProtoGenerator | generate Protobuf Schema representation | [proto help](../../tests/test_scripts/output/genproto/help) |
|  gen-jsonld | [jsonldgen.py](https://github.com/linkml/linkml/blob/main/linkml/generators/jsonldgen.py) | JSONLDGenerator | generate JSON representation | [jsonld help](../../tests/test_scripts/output/genjsonld/help) |
|  gen-json-schema   | [jsonschemagen.py](https://github.com/linkml/linkml/blob/main/linkml/generators/jsonschemagen.py) |    JsonSchemaGenerator | generate JSON Schema representation  | [jsonschmeagen help](../../tests/test_scripts/output/genjsonschema/help) |
|  gen-markdown   | [markdowngen.py](https://github.com/linkml/linkml/blob/main/linkml/generators/markdowngen.py) |    MarkdownGenerator | generate markdown documentation of the model  | [markdowngen help](../../tests/test_scripts/output/genmarkdown/help) |
|  gen-namespaces | [namespacegen.py](https://github.com/linkml/linkml/blob/main/linkml/generators/namespacegen.py) | NamespaceGenerator | generate namespace manager for URI's in model | [namespacegen help](../../tests/test_scripts/output/gennamespace/help) |
|  gen-owl   | [owlgen.py](https://github.com/linkml/linkml/blob/main/linkml/generators/owlgen.py) |    OwlSchemaGenerator | generate an OWL representation  | [owlgen help](../../tests/test_scripts/output/genowl/help) |
|  gen-plantuml   | [plantumlgen.py](https://github.com/linkml/linkml/blob/main/linkml/generators/plantumlgen.py) |    PlantumlGenerator | generate PlantUML representation via [PlantUML](https://plantuml.com/)  | [plantumlgen help](../../tests/test_scripts/output/genuml/help) | 
|  gen-python   | [pythongen.py](https://github.com/linkml/linkml/blob/main/linkml/generators/pythongen.py) | PythonGenerator | generate python classes for a model  | [pythongen help](../../tests/test_scripts/output/genpython/help) |
|  gen-rdf | [rdfgen.py](https://github.com/linkml/linkml/blob/main/linkml/generators/rdfgen.py) | RDFGenerator | generate RDF representation of model | [rdfgen help](../../tests/test_scripts/output/genrdf/help) |
|  gen-shex   | [shexgen.py](https://github.com/linkml/linkml/blob/main/linkml/generators/shexgen.py) |    ShExGenerator | generate a ShEx model representation  | [shexgen help](../../tests/test_scripts/output/genshex/help) |
|  gen-yuml   | [yumlgen.py](https://github.com/linkml/linkml/blob/main/linkml/generators/yumlgen.py) |    YumlGenerator | generate YUML representation via [YUML](https://yuml.me/)  | [yumlgen help](../../tests/test_scripts/output/genuml/help) | 