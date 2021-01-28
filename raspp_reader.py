import xml.etree.ElementTree as ET

def parseRaspp(*argv):
    repositorio = []
    for arquivo in argv:
        root = ET.parse(arquivo).getroot()
        for asset in root.findall('assets'):
            temp = Asset()
            temp.name = asset.get('name')
            temp.id = asset.get('id')
            classification = asset.find('classification')
            for descriptorGroup in classification:
                dg = DescriptorGroup()
                dg.name = descriptorGroup.get('name')
                for value in descriptorGroup.findall('freeeFormValue'):
                    dg.ffv.append(value.get('name'))
                temp.classification.append(dg)
            repositorio.append(temp)
        
    return repositorio

class Asset:
    def __init__(self):
        self.name = ''
        self.id = ''
        self.classification = []
        
    def __repr__(self):
        return self.name
    
class DescriptorGroup:
    def __init__(self):
        self.name = ''
        self.ffv = []