#!/usr/bin/env python
#
# Copyright 2011, Jim Albers
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

jaus_ns = '{urn:jaus:jsidl:1.1}'
suffixes = ['.xml']
jsidl_trees = []
ns_aliases = {}
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
                print "ERROR Can't parse %s: %s"%(fn,repr(e))
            os.chdir(olddir)

def extract_defs_from_type_set(id,c):
    global ns_aliases
    aliases = ns_aliases[id]
    print "Extracting defs from typeset: %s"%id
    for dtsc in c:
        tag = stag(dtsc)
        try:
            name = dtsc.attrib['name']
        except:
            name = '?'
        if tag in ['declared_type_set_ref']:
            # remember this namespace alias. TODO: remember version?
            print "Found type_set_ref: %s %s in %s"%(name,dtsc.attrib['id'],id)
            aliases[name] = dtsc.attrib['id']  
        elif tag in ['declared_const_set_ref']:
            # remember this namespace alias. TODO: remember version?
            aliases[name] = dtsc.attrib['id']  
        elif tag in ['message_def','fixed_field','variable_field','bit_field',
                     'variable_length_string',
                     'record','list','variant','sequence']:
            # Collect type definitions to expand later.
            full_name = id+'.'+name
            if full_name in typeset_defs:
                print "WARN, %s(%s) replacing %s(%s)"% \
                      (full_name,stag(typeset_defs[full_name]),
                       full_name,tag)
            typeset_defs[full_name] = dtsc
            print "Added typeset def for tag: %s, name:%s"%(tag,full_name)
        elif tag in ['header', 'footer','comment']:
            pass # explicitly ignore these
        else:
            # Ignore now, add support later.
            print "ERROR, >>>>>>>>>>>>>>>>>>> Ignoring def %s:%s"%(tag,name)

def extract_defs(element):
    global ns_aliases
    global jaus_ns
    global constset_defs
    global typeset_defs
    if stag(element) == 'declared_const_set':
        constset = element.attrib['id']
        if constset not in constset_defs:
            constset_defs[constset] = {}
        cs = constset_defs[constset]
        for c in element:
            # Each child of declared_const_set.
            if isinstance(c,etree._Comment):
                continue
            name = c.attrib['name']
            if stag(c) == 'const_def':
                if name in cs:
                    oldc = cs[name]
                    print "WARN, existing %s(%s) replaced by %s(%s)"% \
                          (name,stag(oldc),name,stag(c))
                cs[name] = c
    elif stag(element) in ['service_def','declared_type_set']:
        id = element.attrib['id']
        if id not in ns_aliases:
            ns_aliases[id] = {}
        aliases = ns_aliases[id]
        # Add a reference to self, useful later for resolving non-qualified names.
        aliases['self'] = id
        if stag(element) == 'declared_type_set':
            extract_defs_from_type_set(id,element)
        else:
            for c in element.iterdescendants(tag=jaus_ns+'declared_type_set'):
                extract_defs_from_type_set(id,c)

def get_typedef(ns_id,s):
    '''Take string w/ ns_alias1.ns_alias2.name and return the element
       that defines it: e.g. mobility.queryClass.QueryAccelerationState
       If there is no alias qualification, use the 'self.' prefix to
       resolve in the current namespace.
       '''
    global ns_aliases
    global typeset_defs
    print "get_typedef: ns = %s, s = %s"%(ns_id,s)
    if ns_id not in ns_aliases:
        return (None,None)
    ns_path = s.split('.')
    if len(ns_path) == 1:
        # push 'self' to front of path
        ns_path.insert(0,'self')
    # Walk ns_path to get ns in which name is defined.
    # Elements i= 0..n-2 are aliases, element n-1 is the
    # type name.
    aliases = ns_aliases[ns_id]
    next_ns_id = ns_id
    print "%s\n%s"%(pformat(ns_path),pformat(aliases))
    for i in range(len(ns_path)-1):
        if ns_path[i] in aliases:
            # This ns_path component defines an alias in next_ns_id
            # so move to next referenced ns_id and get its aliases.
            next_ns_id = aliases[ns_path[i]]
        else:    
            print "ERROR, Can't resolve %s within %s"%(s,ns_id)
            print "ERROR, ns %s has no ref %s defined in it."%(next_ns_id,ns_path[i])
            return (None,None)
        if next_ns_id in ns_aliases:
            aliases = ns_aliases[next_ns_id]
        else:
            aliases = {}  # If this was last iteration, don't need.
        print "%s -> \n%s"%(next_ns_id,pformat(aliases))

    # Now should have final set of aliases to look at.
    # Substitute full namespace id for s.
    fqn = next_ns_id+'.'+ns_path[-1]
    print fqn
    if fqn in typeset_defs:
        print 'Resolved %s'%(fqn)
        return (typeset_defs[fqn],next_ns_id)
    else:
        print "ERROR, No typeset_def for: %s"%fqn
        return (None,None)

def expand(ns_id,element):
    global ns_aliases
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
                print 'Expanding %s %s'%(stag(c),realname)
                if 'optional' in c.attrib:
                    realoptional = c.attrib['optional']
                else:
                    realoptional = 'false'
                try:
                    ref = c.attrib['declared_type_ref']
                except:
                    print "ERROR, No typeref for %s in node: %s"%(ns_id,name)
                    continue
                new_element, new_element_ns = get_typedef(ns_id,ref)
                if new_element is None:
                    print "ERROR, No typedef for ns_id: %s, ref: %s"%(ns_id,ref)
                else:
                    print "Replacing %s:%s with %s:%s"%(stag(c),name,stag(new_element),new_element.attrib['name'])
                    replacements.append( (c,new_element,new_element_ns,realname,realoptional) )

    # Now do replacements after the depth-first traversal
    for oldchild,newelt,newns_id,realname,realoptional in replacements:
        # Need to replace w/ deepcopy, can't share elements between trees.
        newchild = deepcopy(newelt)
        newchild.attrib['name'] = realname
        newchild.attrib['optional'] = realoptional
        oldchild.getparent().replace(oldchild,newchild)
        # Also need to merge the defining ns aliases with parent's
        ns_aliases[ns_id].update(ns_aliases[newns_id])
        print "Upated aliases for %s: %s"%(ns_id,pformat(ns_aliases[ns_id]))

def fix_type_set_refs(root):
    """Make sure all the qualified names we've sucked up in this service have
    declared_type_set_ref elements at the beginning of the <declared_type_set/> element"""
    # $$$$$$$$$$$$$$$
    pass

def move_message_element_defs_to_type_set(root):
    type_set_node = None
    ns = root.tag[0:root.tag.find('}')+1]
    # sys.stderr.write("Using xmlns=%s\n"%ns)
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
                if type_set_node is not None:
                    type_set_node.append(c)


def output_combined(tree):
    r = tree.getroot()
    name = r.attrib['name']
    f = file(name+'Combined.xml','wb')
    move_message_element_defs_to_type_set(r)
    fix_type_set_refs(r)
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write(etree.tostring(tree,pretty_print=True))
    f.close()

def main():
    global jsidl_trees
    global ns_aliases
    global typeset_defs
    global constset_defs
    jsidl_trees = []
    ns_aliases = {}
    typeset_defs = {}
    constset_defs = {}
    print "Combining JSIDL XML files in: %s"%(sys.argv[1:])
    for dir in sys.argv[1:]:
        os.path.walk(dir,visit,0)
    # extract definitions
    for tree in jsidl_trees:
        r = tree.getroot()
        if stag(r) in ['service_def', 'declared_const_set', 'declared_type_set']:
            extract_defs(r)
    # expand references
    # Need to expand at least 4 times to get full nesting of
    # typerefs resolved.
    for tree in jsidl_trees:
        r = tree.getroot()
        if stag(r) in ['service_def']:
            ns = r.attrib['id']
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
