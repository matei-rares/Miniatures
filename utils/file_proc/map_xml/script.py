import sys
import xml.etree.ElementTree as ET
import csv
import io


# if len(sys.argv) < 2:
#     print("Usage: python your_script.py <name_of_csv_file.csv>")
#     sys.exit(1)

#THIS FILE NEEDS TO BE PLACED IN sw.com.classic_templates_gen2\tools\ExportedDoorsSpecificationTool
#NAME_OF_CSV_FILE = sys.argv[1]   # TODO: we need to choose the correct csv file
NAME_OF_CSV_FILE = "correct_input.csv"


#This script read the XSD
#C:\projects\icas\sw.com.classic_templates_gen2\tools\ExportedDoorsSpecificationTool\tools\xsd\ExportedDoorsSpecification.xsd
#takes the attributes from it and maps them to the data rows from the csv file line >2
#C:\projects\icas\sw.com.classic_templates_gen2\tools\ExportedDoorsSpecificationTool\cfg\input\{component_name}.csv 
#and save it to an xml file
#C:\projects\icas\sw.com.classic_templates_gen2\tools\ExportedDoorsSpecificationTool\cfg\input\ExportedDoorsSpecification.xml



xsd_file_path = r"ExportedDoorsSpecification.xsd"
csv_file_path = f"{NAME_OF_CSV_FILE}"
output_file_path = r"ExportedDoorsSpecification.xml"




xsd_attributes=[]
attributes_dict = {}

# xsd_file_path = "correct_xsd.xsd"
# csv_file_path = "correct_input.csv"
# output_file_path = "output_test.xml"

def parse_xsd(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    for attribute in root.findall(".//{http://www.w3.org/2001/XMLSchema}attribute"):
        name = attribute.get("name")  
        xsd_attributes.append(name)  

        attr_type = attribute.get("type")#.replace("xs:","")  
        if name and attr_type:  
            attributes_dict[name] = attr_type

    # for name, attr_type in attributes.items():
    #     print(f"{name}: {attr_type}")    


parse_xsd(xsd_file_path)
print(xsd_attributes)


def csv_to_dict_array(file_path):
    dict_array = []
    with open(file_path, "r", newline="", encoding="UTF-16") as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=xsd_attributes) # we use the attributes extracted from XSD to define the headers of the columns aka the keys of the a dictionary
        next(reader, None)  # skip the header row in the CSV
        for row in reader:
            dict_array.append(row)
    return dict_array


array_of_dicts = csv_to_dict_array(csv_file_path)



ns = "http://www.w3.org/2003/XInclude"
ET.register_namespace("cool", ns)
root = ET.Element("{%s}REQ" % ns)

requirements = ET.SubElement(root, "REQUIREMENTS")


for i, entry in enumerate(array_of_dicts):
    ET.SubElement(requirements, "REQUIREMENT", entry)


xml_buffer = io.BytesIO()
tree = ET.ElementTree(root)
ET.indent(tree, space="\t", level=0)
tree.write(xml_buffer, encoding="UTF-8", xml_declaration=True)

xml_str = (
    xml_buffer.getvalue().decode("UTF-8")
    .replace("&#13;&#10;", "&#xA;")
    .replace("&#09;", "\t")
    .replace(" />", "/>")
    .replace('?xml version=\'1.0\' encoding=\'UTF-8\'?','?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?')
    .replace('<cool:REQ xmlns:cool=\"http://www.w3.org/2003/XInclude\">','<ns1:REQ xmlns:ns1=\"http://www.w3.org/2003/XInclude\">')
    .replace('</cool:REQ>','</ns1:REQ>')
    )

with open(output_file_path, "w", encoding="utf-8") as f:
    f.write(xml_str)


