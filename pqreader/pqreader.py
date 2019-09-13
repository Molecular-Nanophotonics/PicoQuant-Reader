# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 17:08:31 2019

@author: Martin Fränzl
"""

import numpy as np


def thd_reader(filename):
    """
    Load data from a PicoQuant .thd file.
    """
    with open(filename, 'rb') as f:

        # Read the header common to all file types
        metadata = read_header(f)
        
        # Interactive mode specific header
        intmode_dtype = np.dtype([
                ('CurveIndex',        'int32' ),
                ('TimeOfRecording',   'int32' ),
                ('BoardSerial',       'int32' ),
                ('CFDZeroCross',      'int32' ),
                ('CFDDiscrMin',       'int32' ),
                ('SyncLevel',         'int32' ),
                ('CurveOffset',       'int32' ),
                ('RoutingChannel',    'int32' ),
                ('SubMode',           'int32' ),
                ('MeasMode',          'int32' ),
                ('P1',                'f4'    ),
                ('P2',                'f4'    ),
                ('P3',                'f4'    ),
                ('RangeNo',           'int32' ),
                ('Offset',            'int32' ),
                ('AcquisitionTime',   'int32' ),
                ('StopAfter',         'int32' ),
                ('StopReason',        'int32' ),
                ('SyncRate',          'int32' ),
                ('CFDCountRate',      'int32' ),
                ('TDCCountRate',      'int32' ),
                ('IntegralCount',     'int32' ),
                ('Resolution',        'f4'    ),
                ('ExtDevices',        'int32' ),
                ('reserved',          'int32' )])
        intmode = np.fromfile(f, intmode_dtype, count=1)

        metadata.update(dict(intmode=intmode))
         
        # The remainings are all T3 records
        hist = np.fromfile(f, dtype='uint32', count=4096)
        bins = 1e-9*intmode['Resolution']*np.arange(0, 4096)
        
        return hist, bins, metadata
    
    
def read_header(f):
    
    header_dtypes = np.dtype([
            ('Ident',             'S16'   ),
            ('FormatVersion',     'S6'    ),
            ('CreatorName',       'S18'   ),
            ('CreatorVersion',    'S12'   ),
            ('FileTime',          'S18'   ),
            ('CRLF',              'S2'    ),
            ('Comment',           'S256'  ),
            ('NumberOfChannels',  'int32' ),
            ('NumberOfCurves',    'int32' ),
            ('BitsPerChannel',    'int32' ), # Bits in each T3 record
            ('RoutingChannels',   'int32' ),
            ('NumberOfBoards',    'int32' ),
            ('ActiveCurve',       'int32' ),
            ('MeasurementMode',   'int32' ),
            ('SubMode',           'int32' ),
            ('RangeNo',           'int32' ),
            ('Offset',            'int32' ),
            ('AcquisitionTime',   'int32' ), # ms
            ('StopAt',            'int32' ),
            ('StopOnOvfl',        'int32' ),
            ('Restart',           'int32' ),
            ('DispLinLog',        'int32' ),
            ('DispTimeAxisFrom',  'int32' ),
            ('DispTimeAxisTo',    'int32' ),
            ('DispCountAxisFrom', 'int32' ),
            ('DispCountAxisTo',   'int32' ),])
    header = np.fromfile(f, dtype=header_dtypes, count=1)
    
    if header['FormatVersion'][0] != b'6.0':
        raise IOError(("Format '%s' not supported. "
                       "Only valid format is '6.0'.") % \
                       header['FormatVersion'][0])
    
    dispcurve_dtypes = np.dtype([
            ('DispCurveMapTo', 'int32'),
            ('DispCurveShow',  'int32')])
    dispcurve = np.fromfile(f, dispcurve_dtypes, count=8)

    param_dtypes = np.dtype([
            ('ParamStart', 'f4'),
            ('ParamStep',  'f4'),
            ('ParamEnd',   'f4')])
    param = np.fromfile(f, param_dtypes, count=3)

    repeat_dtypes = np.dtype([
            ('RepeatMode',      'int32'),
            ('RepeatsPerCurve', 'int32'),
            ('RepeatTime',      'int32'),
            ('RepeatWaitTime',  'int32'),
            ('ScriptName',      'S20'  )])
    repeat = np.fromfile(f, repeat_dtypes, count=1)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Hardware information header
    hardware_dtypes = np.dtype([
            ('HardwareIdent',       'S16'  ),
            ('HardwareVersion',     'S8'   ),
            ('BoardSerial',         'int32'),
            ('CFDZeroCross',        'int32'),
            ('CFDDiscriminatorMin', 'int32'),
            ('SYNCLevel',           'int32'),
            ('CurveOffset',         'int32'),
            ('Resolution',          'f4'   )])
    hardware = np.fromfile(f, hardware_dtypes, count=1)
    
    metadata = dict(header = header, 
                    dispcurve = dispcurve,
                    param = param,
                    repeat = repeat,
                    hardware = hardware)
    
    return metadata
    


def t3r_reader(filename):
    """
    Load raw T3 records and metadata from a T3R file.
    
    Arguments:
        filename (string): the path of the .t3r file to be read.
    Returns:
        A tuple of timestamps, detectors, nanotimes (integer arrays) and a
        dictionary with metadata containing at least the keys
        'timestamps_unit' and 'nanotimes_unit'.
    """
    with open(filename, 'rb') as f:
        
        # Read the header common to all file types
        metadata = read_header(f)
        
        # Time tagging mode specific header
        ttmode_dtypes = np.dtype([
                ('TTTRGlobclock',    'int32' ),
                ('ExtDevices',       'int32' ),
                ('Reserved1',        'int32' ),
                ('Reserved2',        'int32' ),
                ('Reserved3',        'int32' ),
                ('Reserved4',        'int32' ),
                ('Reserved5',        'int32' ),
                ('SyncRate',         'int32' ),
                ('AverageCFDRate',   'int32' ),
                ('StopAfter',        'int32' ),
                ('StopReason',       'int32' ),
                ('NumberOfRecords',  'int32' ),
                ('SpecHeaderLength', 'int32' )])
        ttmode = np.fromfile(f, ttmode_dtypes, count=1)

        # Special header for imaging
        imgheader = np.fromfile(f, dtype='int32', count=ttmode['SpecHeaderLength'][0])

        metadata.update(dict(ttmode = ttmode,
                             imgheader = imgheader))
        
        metadata.update({'timetag_unit':  100e-9,
                         'nanotime_unit': metadata['hardware']['Resolution']*1e-9})
    
        # The remainings are all T3 records
        t3records = np.fromfile(f, dtype='uint32', count=ttmode['NumberOfRecords'][0])
     
        # Process the T3R record
        detectors, timetags, nanotimes = process_t3records(t3records)
    
        return timetags, detectors, nanotimes, metadata   



def process_t3records(t3records):
    """
    Decode t3records from .T3R files.
    """
    #reserved_bits = 1
    valid_bits = 1
    route_bits = 2
    data_bits = 12
    timetag_bits = 16
                      
    valid = np.bitwise_and(np.right_shift(t3records, timetag_bits + data_bits + route_bits), 2**valid_bits - 1).astype('uint8')
    route = np.bitwise_and(np.right_shift(t3records, timetag_bits + data_bits), 2**route_bits - 1).astype('uint8')
    data  = np.bitwise_and(np.right_shift(t3records, timetag_bits), 2**data_bits - 1).astype('uint16')
    timetags = np.bitwise_and(t3records, 2**timetag_bits - 1).astype('uint64')
    
    # Correct for overflows     
    correct_overflow(timetags, valid, overflow = 2**timetag_bits)
    
    # Delete overflow events  
    data = np.delete(data, np.where(valid==0)[0])
    timetags = np.delete(timetags, np.where(valid==0)[0])
    
    return route, timetags, data


def correct_overflow(timetags, valid, overflow):
    """
    Correct timetags for overflow.
    """
    overflow_idx = np.where(valid==0)[0]
    for i, (idx1, idx2) in enumerate(zip(overflow_idx[:-1], overflow_idx[1:])):
        timetags[idx1:idx2] += (i + 1)*overflow
    timetags[idx2:] += (i + 2)*overflow


