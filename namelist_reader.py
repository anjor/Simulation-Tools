#!/usr/bin/python
''' A Fortran 90 namelist reader '''

import re
def namelist(File):
    ''' Returns the Fortran namelist as a dict '''
    
    nml = find_groups_in_namelist(File)
    
    for gr in nml:
        print 'Looking for ', gr
        nml[gr] = find_objects_in_group(gr, File)

    return nml

def find_groups_in_namelist(File):
    ''' Finds all groups in the namelist '''
    
    nml = {}
    for line in File:
        match = re.search('&', line)
        if match:
            nml[line.strip()[1:]] = None

    return nml

def find_objects_in_group(gr, File):
    ''' Finds all objects in a given group '''

    group_members = {}
    grname = '&' + gr
    InGroup = False
    for line in File:
        if line == grname:
            InGroup = True
        elif line == '/':
            InGroup = False
        elif InGroup:
            obj = line.split('=')
            group_members[obj[0].strip()] = return_correct_type(obj[1])
    return group_members

def return_correct_type(s):
    try:
        return int(s)
    except:
        try:
            return float(s)
        except:
            return s.lower()

def remove_comments(File):
    uncommented_text = []
    for line in File:
        comm_loc = line.find('!')
        if comm_loc == -1:
            uncommented_text.append(line)
        elif comm_loc == 0:
            pass
        else:
            uncommented_text.append(line[:comm_loc])

    return uncommented_text

if __name__ == '__main__':
    
    filename = 'test.in'
    f = open(filename, 'r')
    nml_text = remove_comments([line.strip() for line in f])
    f.close()

    print namelist(nml_text)

