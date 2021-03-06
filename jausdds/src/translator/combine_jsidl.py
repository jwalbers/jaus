#!/usr/bin/env python
#
# combine_jsidl.py
#
# $Id$
#
# This utility will incrementally include/expand a set of JSIDL files
# contained in a list of directories, and produce a single JSIDL file
# that is referentially complete.
#
# Copyright 2012, Jim Albers
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
#     * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following disclaimer
# in the documentation and/or other materials provided with the
# distribution.
#     * Neither the name of the copyright owner nor the names of
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# Files generated by the CJSIDL Tools are owned by the owner of the
# input file used when generating them.  This code is not standalone and
# requires a support library to be linked with it.
#
import os
import sys
from lxml import etree
from pprint import pformat
from copy import deepcopy

jaus_ns = '{urn:jaus:jsidl:1.0}'
suffixes = ['.xml']
jsidl_trees = []
ns_alias = {}
typeset_defs = {} # {typeset_id:{ name:<element>, ...} , ...}
constset_defs = {} # {constset_id:{ name:<element>, ...} , ...}
service_typeset_refs = {} #{service_id:{ name:(id,version), ... }, ...}

def stag(c):
    global jaus_ns
    if isinstance(c,etree._Comment):
        return 'comment'
    return c.tag.replace(jaus_ns,'')

def visit(arg, dirname, names):
    global jsidl_trees
    for fn in names:
        base, ext = os.path.splitext(fn)
        if ext in suffixes:
            olddir = os.getcwd()
            os.chdir(dirname)
            print "Combining XML in: " + dirname + os.sep + fn
            try:
                jsidl_trees.append(etree.parse(fn))
            except Exception,e:
                print "Can't parse %s: %s"%(fn,repr(e))
            os.chdir(olddir)

def extract_defs_from_type_set(id,c):
    ns = ns_alias[id]
    for dtsc in c:
        tag = stag(dtsc)
        try:
            name = dtsc.attrib['name']
        except:
            name = '?'
        if tag in ['declared_type_set_ref']:
            # remember this namespace alias. TODO: remember version?
            print "Found type_set_ref: %s %s in %s"%(name,dtsc.attrib['id'],id)
            ns[name] = dtsc.attrib['id']  
        elif tag in ['declared_const_set_ref']:
            # remember this namespace alias. TODO: remember version?
            ns[name] = dtsc.attrib['id']  
        elif tag in ['message_def','fixed_field','record','list',
                     'bit_field','variant','variable_length_string']:
            # Collect type definitions to expand later.
            full_name = id+'.'+name
            if full_name in typeset_defs:
                print "Warning, %s(%s) replacing %s(%s)"% \
                      (full_name,stag(typeset_defs[full_name]),
                       full_name,tag)
            typeset_defs[full_name] = dtsc
        elif tag in ['header', 'footer','comment']:
            pass # explicitly ignore these
        else:
            # Ignore now, add support later.
            print ">>>>>>>>>>>>>>>>>>> Ignoring def %s:%s"%(tag,name)

def extract_defs(element):
    global jaus_ns
    global constset_defs
    global typeset_defs
    if stag(element) == 'declared_const_set':
        constset = element.attrib['id']
        if constset not in constset_defs:
            constset_defs[constset] = {}
        for c in element:
            if isinstance(c,etree._Comment):
                continue
            name = c.attrib['name']
            cs = constset_defs[constset]
            if stag(c) == 'const_def':
                if name in cs:
                    print "Warning, %s(%s) replacing %s(%s)"% \
                          (name,stag(cs[name]),name,stag(c))
                cs[name] = c
    elif stag(element) in ['service_def','declared_type_set']:
        id = element.attrib['id']
        if id not in ns_alias:
            ns_alias[id] = {}
        ns = ns_alias[id]
        # Add a reference to self, useful later for resolving non-qualified names.
        ns['self'] = id
        if stag(element) == 'declared_type_set':
            extract_defs_from_type_set(id,element)
        else:
            for c in element.iterdescendants(tag=jaus_ns+'declared_type_set'):
                extract_defs_from_type_set(id,c)

def get_typedef(ns,s):
    '''Take string w/ ns_alias1.ns_alias2.name and return the element
       that defines it: e.g. mobility.queryClass.QueryAccelerationState
       If there is no alias qualification, use the 'self.' prefix to
       resolve in the current namespace.
       '''
    print "ns = %s, s = %s"%(ns,s)
    if ns not in ns_alias:
        return None
    ns_path = s.split('.')
    if len(ns_path) == 1:
        # push 'default' to front of path
        ns_path.insert(0,'self')
    # Walk ns_path to get ns in which name is defined.
    # Elements i= 0..n-2 are aliases, element n-1 is the
    # type name.
    try:
        for i in range(len(ns_path)-1):
            ns = ns_alias[ns][ns_path[i]]
        # Fully qualified name.
        fqn = ns+'.'+ns_path[-1]
        print 'Resolving %s'%(fqn)
        if fqn in typeset_defs:
            return (typeset_defs[fqn],ns)
        else:
            raise Exception('%s: Not defined'%fqn)
    except Exception, e:
        print "Can't resolve %s(%s): %s"%(ns,s,repr(e))
        return (None,None)

def expand(ns,element):
    global constset_defs
    global typeset_defs
    replacements = []
    for c in element.iterdescendants():
        if 'name' in c.attrib:
            name = c.attrib['name']
            # Don't expand declared_message_defs.
            if stag(c) in ['declared_message_def','declared_fixed_field','declared_list',
                           'declared_sequence', 'declared_variant',
                           'declared_record','declared_variable_length_string']:
                # TODO: Add all 'declared_' types here.
                # print "Looking at %s %s"%(name,stag(c))
                realname = c.attrib['name']
                if 'optional' in c.attrib:
                    realoptional = c.attrib['optional']
                else:
                    realoptional = 'false'
                ref = c.attrib['declared_type_ref']
                new_element, new_element_ns = get_typedef(ns,ref)
                if new_element is not None:
                    # print "Replacing %s:%s with %s:%s"%(stag(c),name,stag(new_element),new_element.attrib['name'])
                    replacements.append( (c,new_element,new_element_ns,realname,realoptional) )

    # Now do replacements after the depth-first traversal
    for oldchild,newelt,newns,realname,realoptional in replacements:
        # Need to replace w/ deepcopy, can't share elements between trees.
        newchild = deepcopy(newelt)
        newchild.attrib['name'] = realname
        newchild.attrib['optional'] = realoptional
        oldchild.getparent().replace(oldchild,newchild)
        # Also need to merge the defining ns aliases with parent's
        ns_alias[ns].update(ns_alias[newns])

def fix_type_set_refs(root):
    """Make sure all the qualified names we've sucked up in this service have
    declared_type_set_ref elements at the beginning of the <declared_type_set/> element"""
    pass

def move_message_element_defs_to_type_set(root):
    type_set_node = None
    ns = root.tag[0:root.tag.find('}')+1]
    sys.stderr.write("Using xmlns=%s\n"%ns)
    looking_at_message_set = False
    type_set_node = None
    for c in root.iterdescendants():
        if type(c.tag) != type(''):
            # comment or other kind of node
            continue
        cstag = c.tag.replace(ns,'')
        if cstag == 'declared_type_set' >= 0:
            type_set_node = c
        elif cstag == 'message_set' >= 0:
            looking_at_message_set = True
        elif looking_at_message_set:
            if cstag in ['record','variant','sequence','list']:
                # Move this typedef to typeset and replace w/
                # a declared_type_set_ref.
                name = c.attrib['name'][0].lower()+c.attrib['name'][1:]
                type_ref = c.attrib['name']
                dc = etree.Element('declared_'+cstag,attrib={'name':name,
                                                             'declared_type_ref':type_ref,
                                                             'optional':'false'})
                c.getparent().replace(c,dc)
                type_set_node.append(c)


def output_combined(tree):
    r = tree.getroot()
    name = r.attrib['name']
    f = file(name+'Combined.xml','wb')
    move_message_element_defs_to_type_set(r)
    fix_type_set_refs(r)
    f.write(etree.tostring(tree,pretty_print=True))
    f.close()

def print_usage():
    print "python combine_jsidl.py dir [dir]*"
    print "    provide a list of directories containing JSIDL XML files that you wish to combine."

def main():
    global jsidl_trees
    global ns_alias
    global typeset_defs
    global constset_defs
    jsidl_trees = []
    ns_alias = {}
    typeset_defs = {}
    constset_defs = {}
    if len(sys.argv[1:]) == 0:
        print_usage()
        sys.exit(1)
    print "Combining JSIDL XML files in: %s"%(sys.argv[1:])
    for dir in sys.argv[1:]:
        os.path.walk(dir,visit,0)
    # extract definitions
    for tree in jsidl_trees:
        r = tree.getroot()
        if stag(r) in ['service_def', 'declared_const_set', 'declared_type_set']:
            extract_defs(r)
    # expand references, twice to pick up cascading references.
    for tree in jsidl_trees:
        r = tree.getroot()
        if stag(r) in ['service_def']:
            ns = r.attrib['id']
            # Need to expand at least 4 times to get full nesting of
            # type refs resolved.
            # TODO: smarter way to determine when all refs are resolved.
            expand(ns,r)
            expand(ns,r)
            expand(ns,r)
            expand(ns,r)
            expand(ns,r)
    for tree in jsidl_trees:
        r = tree.getroot()
        if stag(r) == 'service_def':
            # Need to add any inherited typedef references.
            # print "Looking at %s %s"%(stag(r),r.attrib['name'])
            output_combined(tree)
    
if __name__=='__main__':
    main()
