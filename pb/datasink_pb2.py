# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: proto/datasink.proto
# Protobuf Python Version: 5.29.0-rc3
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '-rc3',
    'proto/datasink.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x14proto/datasink.proto\x12\x14HikStreamPluginsDump\"\x8e\x01\n\x0c\x44\x61tasinkDump\x12<\n\x0e\x64\x61tasinkConfig\x18\x01 \x02(\x0b\x32$.HikStreamPluginsDump.DatasinkConfig\x12@\n\x10\x64\x61tasinkMetaData\x18\x02 \x02(\x0b\x32&.HikStreamPluginsDump.DatasinkMetaData\"&\n\x0e\x44\x61tasinkConfig\x12\x14\n\x0cpipelineName\x18\x01 \x02(\t\"\xb1\x01\n\x10\x44\x61tasinkMetaData\x12\r\n\x05index\x18\x01 \x02(\x05\x12\x11\n\tmediaType\x18\x02 \x02(\r\x12\x11\n\tframeType\x18\x03 \x02(\r\x12\x11\n\ttimeStamp\x18\x04 \x02(\r\x12\r\n\x05\x61larm\x18\x05 \x02(\r\x12\x11\n\tframeData\x18\x06 \x01(\x0c\x12\x1b\n\x13\x62\x61\x63kgroundImageData\x18\x07 \x01(\x0c\x12\x16\n\x0e\x61larmImageData\x18\x08 \x01(\x0c\x42\x30\n\x1e\x63om.hikvision.bsp.parser.protoB\x0e\x44\x61tasinkDumpPB')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'proto.datasink_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\036com.hikvision.bsp.parser.protoB\016DatasinkDumpPB'
  _globals['_DATASINKDUMP']._serialized_start=47
  _globals['_DATASINKDUMP']._serialized_end=189
  _globals['_DATASINKCONFIG']._serialized_start=191
  _globals['_DATASINKCONFIG']._serialized_end=229
  _globals['_DATASINKMETADATA']._serialized_start=232
  _globals['_DATASINKMETADATA']._serialized_end=409
# @@protoc_insertion_point(module_scope)